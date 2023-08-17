import ctypes
import glob
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile

from PySide6.QtCore import QDir, Slot
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from tpds.output_grabber.library_output_grabber import LibraryOutputGrabber

from tpds.helper import checkIfProcessRunning, log, make_dir
from tpds.settings import TrustPlatformSettings

try:
    import cryptoauthlib_ta as cal
except (ModuleNotFoundError, ImportError):
    import cryptoauthlib as cal

from tpds.proto_provision import TA100Provision

try:
    from tpds.ta_attribute_parser import attributes
except Exception as e:
    log(e)

from tpds.tp_utils.tp_utils import add_to_zip_archive

from tpds.usecase_collector.collector import Collector

shared_lib_resp_status = {
    "00": "Success",
    "01": "Json Validation Failed",
    "02": "Xml Validation Failed",
}

ta_handles_json_str = None


def get_ta_handles_json():
    return ta_handles_json_str


def ta_appJSON(args):
    global ta_handles_json_str
    ta_handles_json_str = args[0]
    return {"response": ta_handles_json_str, "status": "OK"}


def get_ta_appJSON(args):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.setWindowTitle("TA Configurator")

    global ta_handles_json_str
    attr_dict = {}

    if ta_handles_json_str:
        h_json_obj = json.loads(ta_handles_json_str)
        h_list = h_json_obj["TA100Attributes"]["HandleList"]
        for handle in h_list:
            attr_dict.update({handle["attrib"]: attributes.attribute_info(handle["attrib"])})
        log(attr_dict)
    else:
        conf = TrustPlatformSettings()
        ta_config_dir = os.path.join(conf.settings.conda_path, "TA_Configurator")
        if os.path.exists(ta_config_dir):
            if not checkIfProcessRunning("TaConfigurator.UI"):
                msg_box.setText(
                    (
                        """<font color=#0000ff><b>Close the current webview and relaunch page
                    to open TA Configurator Application</b></font><br>"""
                    )
                )
            else:
                msg_box.setText(
                    (
                        """<font color=#0000ff><b>TA Handle data is not available</b></font><br>
                    <br>Populate handles data in TA Configurator Application
                    and send to TPDS by clicking on Export -> Secure
                    Provisioning using TPDS <br>"""
                    )
                )
        else:
            msg_box.setText(
                (
                    """<font color=#0000ff><b>The required package is
                    not available.</b></font><br>"""
                )
            )
        msg_box.exec_()
    if ta_handles_json_str:
        return {"response": [h_json_obj, attr_dict], "status": "ta_jsonstr"}
    else:
        return {"response": "no_change", "status": "OK"}


@Slot(str)
def ta_open_app_handle(args):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.setWindowTitle("TA Configurator")

    conf = TrustPlatformSettings()
    ta_config_dir = os.path.join(conf.settings.conda_path, "TA_Configurator")
    if os.path.exists(ta_config_dir):
        cmd = [
            os.path.join(ta_config_dir, "TaConfigurator.UI.exe"),
            "-config",
            os.path.join(ta_config_dir, "sample.taconfig"),
        ]
        if checkIfProcessRunning("TaConfigurator.UI"):
            msg_box.setText(
                (
                    """<font color=#0000ff><b>Application is already running!</b></font><br>
                <br>It is advised to run only one instance of the application.
                Use the one that is alreay open! Otherwise, close application
                and Webview to relaunch again.<br>"""
                )
            )
            msg_box.exec_()
        else:
            subprocess.Popen(cmd)
    else:
        log(f"{ta_config_dir} is unavailable to launch the application")
        msg_box.setText(
            (
                """<font color=#0000ff><b>Supported package is not available.</b></font><br>
            <br>Visit Microchip Direct or contact Microchip Sales team to get
            the package. <br>"""
            )
        )
        msg_box.exec_()


@Slot(str, str)
def ta_provisioningXML_handle(xml_type, handles_json_str):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.setWindowTitle("Production Provisioning Zip")

    display_msg = ""
    curr_dir = os.getcwd()
    dir_path = os.path.join(
        os.path.join(getattr(Collector().get("ta100_config", {}), "_root", ""), "assets")
    )
    shared_lib_path = os.path.join(dir_path, "XML_GenerationLibrary", sys.platform)
    prov_attr_file = os.path.join(dir_path, "XML_GenerationLibrary", "Provisioning_Attributes.json")

    if sys.platform == "win32":
        shared_lib_ext = ".dll"
    elif sys.platform == "linux":
        shared_lib_ext = ".so"
    elif sys.platform == "darwin":
        shared_lib_ext = ".dylib"

    shared_lib = glob.glob(os.path.join(shared_lib_path, "*" + shared_lib_ext))
    dependency_shared_lib = []
    for lib in shared_lib:
        if lib.split("\\")[-1].split(".")[0] != "ConfigValidate":
            dependency_shared_lib.append(lib.split("\\")[-1])

    for dll in dependency_shared_lib:
        log(os.path.join(shared_lib_path, dll))

    # Shared library name platform specific
    if sys.platform == "win32":
        shared_lib_name = "ConfigValidate" + shared_lib_ext
    else:
        # Linux & Mac lib will be prefixed
        shared_lib_name = "libConfigValidate" + shared_lib_ext
    log(os.path.join(dir_path, shared_lib_name))

    try:
        lib = ctypes.cdll.LoadLibrary(os.path.join(shared_lib_path, shared_lib_name))
        with open(prov_attr_file, "w") as temp_file:
            temp_file.write(handles_json_str)
        time_stamp = datetime.now().strftime("%m%d%H%M%S")
        xml_tag_name = "Proto"
        if xml_type == "prod_xml":
            xml_tag_name = "Prod"

        downloads_path = os.path.join(str(QDir.homePath()), "Downloads", "TPDS_Downloads")
        make_dir(downloads_path)
        os.chdir(downloads_path)

        encryption_keys = None
        if xml_type == "prod_xml":
            dlg = QFileDialog(None, caption="Select Encryption Key(s) File", filter="*.zip")
            result = dlg.exec()
            if result == QDialog.Accepted:
                encryption_keys = dlg.selectedFiles()[0]

            else:
                display_msg = (
                    "Encryption Key(s) File is MUST for " "Producing Secure Provisioning Packet"
                )
                raise ValueError("")

        json_schema = str.encode(
            os.path.join(dir_path, "XML_GenerationLibrary", "ta100_json_schema.json")
        )
        xml_schema = str.encode(
            os.path.join(dir_path, "XML_GenerationLibrary", "TA100_Config_1.0.xsd")
        )
        json_file = str.encode(prov_attr_file)
        shared_lib_resp_buff = ctypes.create_string_buffer(500)

        lib_capture_output = LibraryOutputGrabber(sys.stdout, True)
        lib_capture_output.start()
        if encryption_keys:
            with ZipFile(encryption_keys) as zf:
                for file_name in zf.namelist():
                    if ".pem" in file_name:
                        xml_out = f"TA100_ProvXML_{time_stamp}_{xml_tag_name}.ENC.xml"
                        key = zf.read(file_name)
                        xml_file = os.path.join(downloads_path, xml_out).replace("\\", "/")
                        lib.generate_provisioning_xml(
                            json_schema,
                            json_file,
                            str.encode(xml_file),
                            key,
                            xml_schema,
                            shared_lib_resp_buff,
                        )
                        if (
                            shared_lib_resp_status.get(shared_lib_resp_buff.value.decode("UTF-8"))
                            != "Success"
                        ):
                            display_msg = shared_lib_resp_status.get(
                                shared_lib_resp_buff.value.decode("UTF-8")
                            )
                            lib_capture_output.stop()
                            log(lib_capture_output.capturedtext)
                            raise RuntimeError("")
                    else:
                        display_msg = f"Unknown key file:{file_name}"
                        raise ValueError("")
        else:
            xml_file = os.path.join(
                downloads_path, f"TA100_ProvXML_{time_stamp}_{xml_tag_name}.xml"
            ).replace("\\", "/")
            lib.generate_provisioning_xml(
                json_schema,
                json_file,
                str.encode(xml_file),
                str.encode("e"),
                xml_schema,
                shared_lib_resp_buff,
            )
            if shared_lib_resp_status.get(shared_lib_resp_buff.value.decode("UTF-8")) != "Success":
                display_msg = shared_lib_resp_status.get(shared_lib_resp_buff.value.decode("UTF-8"))
                raise RuntimeError("")

        lib_capture_output.stop()
        log(lib_capture_output.capturedtext)

        zip_list = glob.glob("*.xml")
        zip_file = f"TA100_ProvXML_{time_stamp}_{xml_tag_name}.zip"
        add_to_zip_archive(zip_file, zip_list)
        for file in zip_list:
            os.remove(file) if os.path.exists(file) else None
        path_link = os.path.join(downloads_path, zip_file).replace("\\", "/")
        display_msg = (
            f"<font color=#0000ff>"
            f"<b>Provisioning Package is saved.</b></font><br><br>"
            f"""Package: <a href='{path_link}'>"""
            f"""{os.path.basename(path_link)}</a><br>"""
        )

    except BaseException as e:
        display_msg += f"{e}"
        msg_box.setIcon(QMessageBox.Critical)

    finally:
        os.remove(prov_attr_file) if os.path.exists(prov_attr_file) else None
        os.chdir(curr_dir)
        msg_box.setText(display_msg)
        msg_box.exec_()


@Slot(str)
def ta_proto_provisioning_handle(id):
    log("Provisioning ta-Prototype board")
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setStandardButtons(QMessageBox.Ok)
    global ta_handles_json_str
    provision_data = json.loads(ta_handles_json_str)
    interface_type = provision_data["TA100Attributes"]["IoType"]
    i2c_addr = provision_data["TA100Attributes"]["ConfigurationMemory"]["attrib"][32:34]

    try:
        cfg = cal.cfg_ateccx08a_kithid_default()
        if interface_type == "I2CInterface":
            cfg.cfg.atcahid.dev_interface = int(cal.ATCAKitType.ATCA_KIT_I2C_IFACE)
            cfg.cfg.atcahid.dev_identity = int(i2c_addr, 16)
        else:
            cfg.cfg.atcahid.dev_interface = int(cal.ATCAKitType.ATCA_KIT_SPI_IFACE)
            cfg.cfg.atcahid.dev_identity = 0
        cfg.devtype = 0x10
        provision = TA100Provision(cfg)
        provision_info = provision.provision_device(ta_handles_json_str)
        status_msg = ""
        for handle_status in provision_info.get("handles_status"):
            status_msg += "" if not handle_status.get("status").strip() else f"{handle_status}\n"
        if len(status_msg):
            display_msg = "Proto provisioning is completed with the following observations...\n\n"
            display_msg += status_msg
        else:
            display_msg = "Proto provisioning is completed!\n\n"
    except BaseException as e:
        display_msg = f"Proto Provisioning has failed with {e}"
        msg_box.setIcon(QMessageBox.Critical)
    finally:
        log(display_msg)
        msg_box.setText(display_msg)
        msg_box.exec_()


@Slot(list)
def ta_uno_appJSON(xml_type, json_str):
    global ta_handles_json_str
    ta_handles_json_str = json_str
    if xml_type == "proto_xml" or xml_type == "prod_xml":
        ta_provisioningXML_handle(xml_type, ta_handles_json_str)
    elif xml_type == "proto_provision":
        ta_proto_provisioning_handle(0)
    # else:
    #     status = "Invalid arg parameter"

    # return {
    #     "response": "",
    #     "status": status
    # }


ta_config_file_json_str = ""


@Slot(str)
def ta_uno_config_handle(config_file):
    global ta_config_file_json_str
    conf = TrustPlatformSettings()
    config_file = os.path.join(conf.settings.conda_path, "TA_Configurator", "SampleConfig.taconfig")

    config_info = {}
    if os.path.exists(config_file):
        config_info.update({"title": Path(config_file).name})
        config_info.update({"content": Path(config_file).read_text("'utf-8-sig'")})
    ta_config_file_json_str = json.dumps(config_info)


def ta_uno_get_config(args):
    return {"response": ta_config_file_json_str, "status": "OK"}
