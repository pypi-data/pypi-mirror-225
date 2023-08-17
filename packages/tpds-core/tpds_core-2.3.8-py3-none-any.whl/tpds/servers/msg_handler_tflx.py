import os
from zipfile import ZipFile

from PySide6.QtCore import QDir, Qt, Slot
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from tpds.proto_provision import ProtoProvisioning
from tpds.tp_utils.tp_keys import TPAsymmetricKey

from tpds.helper import log

from .tflx_provisioning_xml_ui import TflxProvisioningXml

tflex_dialog = None


@Slot(str)
def tflx_provisioningXML_handle(config_string):
    global tflex_dialog
    tflex_dialog = TflxProvisioningXml(config_string=config_string)
    return None


@Slot(str)
def tflx_proto_provisioning_handle(id):
    log("Provisioning tflx-Prototype board")
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setStandardButtons(QMessageBox.Ok)
    display_msg = ""

    try:
        xml_file_in = signer_ca_key = device_ca_key = None
        dialog = QFileDialog(None, caption="Select Proto Provisioning Package", filter="*.zip")
        result_b = dialog.exec()
        if result_b == QDialog.Accepted:
            zip_package = dialog.selectedFiles()[0]
            if os.path.exists(zip_package):
                log("Reading from zip package")
                with ZipFile(zip_package) as zf:
                    for file_name in zf.namelist():
                        name, extn = os.path.splitext(file_name)
                        if extn == ".xml" and ".ENC" not in name:
                            xml_file_in = zf.extract(file_name)
                            log(xml_file_in)
                            break
            if xml_file_in is None:
                display_msg = "XML file is not found in the uploaded Zip package"
                raise ValueError("")

            cakey_msg_box = QMessageBox()
            cakey_msg_box.setIcon(QMessageBox.Question)
            cakey_msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            cakey_msg_box.setWindowTitle("CA Keys Selection")
            cakey_msg_box.setTextFormat(Qt.RichText)
            cakey_msg_box.setText(
                (
                    """<font color=#0000ff><b>CA Keys</b></font><br>
                <br>It is required to sign certificate with its CA
                key. <br><br>Select<br>
                - <b>Yes</b>, if CA keys are available and willing to upload.<br>
                - <b>No</b>, if CA keys are unavailable or not willing to
                upload. Tool generates a key and uses it for signing.<br>"""
                )
            )
            reply = cakey_msg_box.exec_()
            if reply == QMessageBox.Yes:
                log("Getting Root Key")
                cert_dlg = QFileDialog(None, caption="Select your Root Key", filter="*.key")
                cert_file = cert_dlg.exec()
                if cert_file == QDialog.Accepted:
                    signer_ca_key = cert_dlg.selectedFiles()[0]
                    log("Getting signer Key")
                    cert_dlg = QFileDialog(None, caption="Select your Signer Key", filter="*.key")
                    cert_file = cert_dlg.exec()
                    if cert_file == QDialog.Accepted:
                        device_ca_key = cert_dlg.selectedFiles()[0]

            log("Provisioning the prototype board")
            provision = ProtoProvisioning(id, xml_file_in)
            log(f"Device details: {provision.element.get_device_details()}")
            provision.provision_non_cert_slots()

            if signer_ca_key is None:
                signer_ca_key = os.path.join(
                    str(QDir.homePath()), "Downloads", "TPDS_Downloads", "proto_root.key"
                )
                key = TPAsymmetricKey()
                key.get_private_pem(signer_ca_key)

            if device_ca_key is None:
                device_ca_key = os.path.join(
                    str(QDir.homePath()), "Downloads", "TPDS_Downloads", "proto_signer.key"
                )
                key = TPAsymmetricKey()
                key.get_private_pem(device_ca_key)

            provision.provision_cert_slots(signer_ca_key=signer_ca_key, device_ca_key=device_ca_key)
            display_msg = "Prototype board provisioning completed!"
        else:
            display_msg = "Prototype board provisioning canceled!"

    except BaseException as e:
        display_msg += f"{e}"
        msg_box.setIcon(QMessageBox.Critical)

    finally:
        if xml_file_in:
            os.remove(xml_file_in) if os.path.exists(xml_file_in) else None
        msg_box.setText(display_msg)
        msg_box.exec_()
