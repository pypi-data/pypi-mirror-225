import glob
import json
import os
from datetime import datetime
from pathlib import Path

import cryptoauthlib as cal
from PySide6.QtCore import QDir, Qt, Slot
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from tpds.certs.tflex_certs import TFLEXCerts
from tpds.proto_provision.ecc204_provision import ECC204Provision
from tpds.tp_utils.tp_keys import TPAsymmetricKey
from tpds.tp_utils.tp_utils import add_to_zip_archive

from tpds.helper import log, utils


def ecc204_tflxauth_certs(
    cert_data, root_key=None, signer_key=None, device_sn=None, device_public_key=None
):
    """ """
    if cert_data.get("cert_type") != "custCert":
        return None

    certs = TFLEXCerts(device_name="ECC204")
    certs.build_root(
        key=root_key,
        org_name=cert_data.get("signer_ca_org"),
        common_name=cert_data.get("signer_ca_cn"),
        validity=int(cert_data.get("s_cert_expiry_years")),
    )
    certs.build_signer_csr(
        key=signer_key,
        org_name=cert_data.get("s_cert_org"),
        common_name=cert_data.get("s_cert_cn"),
        signer_id="FFFF",
    )
    certs.build_signer(validity=int(cert_data.get("s_cert_expiry_years")))
    certs.build_device(
        device_sn=device_sn,
        device_public_key=device_public_key,
        org_name=cert_data.get("d_cert_org"),
        validity=int(cert_data.get("d_cert_expiry_years")),
    )

    return certs


@Slot(str)
def tflex_ecc204_json_handle(config_string):
    """ """
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.setTextFormat(Qt.RichText)
    display_msg = ""

    data = json.loads(config_string)
    cert_data = data.get("slot_info")[1]
    if cert_data.get("cert_type") != "custCert":
        display_msg = (
            "<font color=#0000ff>"
            "<b>Provisioning Package Generation.</b></font><br><br>"
            "Currently Provisioning package generation is only for Custom PKI purpose. "
            "Please use the “Provision Prototype Samples” button if you only need to "
            "generate a private key / provision a symmetric key<br>"
        )
    else:
        curr_dir = os.getcwd()
        zip_file_list = []
        device_name = "ECC204"
        try:
            certs_zip_dir = os.path.join(str(QDir.homePath()), "Downloads", "TPDS_Downloads")
            utils.make_dir(certs_zip_dir)
            time_stamp = datetime.now().strftime("%m%d%H%M%S")
            certs_zip_f = f"{device_name}_{time_stamp}.zip"
            os.chdir(certs_zip_dir)

            certs = ecc204_tflxauth_certs(cert_data, device_sn=cert_data.get("d_cert_cn"))
            certs.save_tflex_c_definitions()
            certs_txt = (
                certs.root.get_certificate_in_text()
                + "\n\n"
                + certs.signer.get_certificate_in_text()
                + "\n\n"
                + certs.device.get_certificate_in_text()
            )
            Path("custom_certs.txt").write_text(certs_txt)
            Path("root.crt").write_bytes(certs.root.get_certificate_in_pem())
            Path("signer.crt").write_bytes(certs.signer.get_certificate_in_pem())
            Path("device.crt").write_bytes(certs.device.get_certificate_in_pem())

            for extn in ["*.c", "*.h", "*.crt", "*.txt"]:
                zip_file_list.extend(glob.glob(extn))
            add_to_zip_archive(certs_zip_f, zip_file_list)

            certs_zip_f = os.path.join(certs_zip_dir, certs_zip_f).replace("\\", "/")
            display_msg = (
                "<font color=#0000ff>"
                "<b>Provisioning Package is saved.</b></font><br><br>"
                f"""Package: <a href='{certs_zip_f}'>"""
                f"""{certs_zip_f}</a><br>"""
            )

        except BaseException as e:
            display_msg = f"Provisioning Package process failed with:\n{e}"
            msg_box.setIcon(QMessageBox.Critical)

        finally:
            for file in zip_file_list:
                os.remove(file) if os.path.exists(file) else None
            os.chdir(curr_dir)

    msg_box.setText(display_msg)
    msg_box.exec_()


@Slot(str)
def tflxecc204_proto_prov_handle(config_str):
    """ """
    data = json.loads(config_str)

    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setStandardButtons(QMessageBox.Ok)
    log("Provisioning ECC204")
    display_msg = "<font color=#0000ff><b>Proto provisioning observations:</b></font><br><br>"

    try:
        cfg = cal.cfg_ateccx08a_kithid_default()
        cfg.cfg.atcahid.dev_identity = 0x66
        cfg.devtype = cal.get_device_type_id("ECC204")
        if data.get("interface") == "i2c":
            cfg.cfg.atcahid.dev_interface = int(cal.ATCAKitType.ATCA_KIT_I2C_IFACE)
        else:
            cfg.cfg.atcahid.dev_interface = int(cal.ATCAKitType.ATCA_KIT_SWI_IFACE)

        ecc204_test_config = bytes.fromhex(
            """
            8F F3 19 8B A3 3A E2 B2  58 00 01 00 00 00 00 00
            0F 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
            00 00 00 00 FF FF FF FF  FF FF FF FF FF FF FF FF
            33 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00"""
        )
        ecc204_proto_provision = ECC204Provision(cfg)
        ecc204_proto_provision.element.load_tflx_test_config(ecc204_test_config)

        device_public_key = bytearray()
        assert (
            cal.atcab_get_pubkey(0, device_public_key) == cal.Status.ATCA_SUCCESS
        ), "Reading Public Key failed"
        device_sn = bytearray()
        assert (
            cal.atcab_read_serial_number(device_sn) == cal.Status.ATCA_SUCCESS
        ), "Reading Serial number failed"

        signer_ca_key = device_ca_key = certs = None
        cert_data = data.get("slot_info")[1]
        if cert_data.get("cert_type") == "custCert":
            ca_key_msg_box = QMessageBox()
            ca_key_msg_box.setIcon(QMessageBox.Question)
            ca_key_msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            ca_key_msg_box.setWindowTitle("CA Keys Selection")
            ca_key_msg_box.setTextFormat(Qt.RichText)
            ca_key_msg_box.setText(
                (
                    """<font color=#0000ff><b>CA Keys</b></font><br>
                <br>It is required to sign certificate with its CA
                key. <br><br>Select<br>
                - <b>Yes</b>, if CA keys are available and willing to upload.<br>
                - <b>No</b>, if CA keys are unavailable or not willing to
                upload. Tool generates a key and uses it for signing.<br>"""
                )
            )
            reply = ca_key_msg_box.exec_()
            if reply == QMessageBox.Yes:
                log("Getting root Key")
                cert_dlg = QFileDialog(None, caption="Select your Root Key", filter="*.key")
                cert_file = cert_dlg.exec()
                if cert_file == QDialog.Accepted:
                    signer_ca_key = cert_dlg.selectedFiles()[0]
                    log("Getting signer Key")
                    cert_dlg = QFileDialog(None, caption="Select your Signer Key", filter="*.key")
                    cert_file = cert_dlg.exec()
                    if cert_file == QDialog.Accepted:
                        device_ca_key = cert_dlg.selectedFiles()[0]

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

            log("Generating custom certificates for device")
            if cert_data.get("d_cert_cn") != "sn0123030405060708EE":
                device_sn = cert_data.get("d_cert_cn")
            certs = ecc204_tflxauth_certs(
                cert_data,
                root_key=signer_ca_key,
                signer_key=device_ca_key,
                device_sn=device_sn,
                device_public_key=device_public_key,
            )

        slot_info = data.get("slot_info")
        for slot in slot_info:
            slot_msg = ""
            if slot.get("key_load_config") not in ["cert", "no_load"] and slot.get("data"):
                ecc204_proto_provision.perform_slot_write(
                    int(slot.get("slot_id")), bytes.fromhex(slot.get("data"))
                )
                slot_msg = "User data loaded."
            elif certs and slot.get("key_load_config") == "cert":
                ecc204_proto_provision.provision_cert_slot(
                    certs.root.certificate, certs.signer.certificate, certs.device.certificate
                )
                slot_msg = "Certs data loaded."
            else:
                slot_msg = "Pregenerated." if slot.get("slot_id") == 0 else "Skipped."
            display_msg += (
                f"""Slot{int(slot.get('slot_id'))} ({slot.get('slot_type')}): {slot_msg}<br>"""
            )
        display_msg += "<br>Prototype board provisioning completed!"

    except BaseException as e:
        display_msg += f"<br>Prototyping device failed with:{e}"
        msg_box.setIcon(QMessageBox.Critical)

    finally:
        msg_box.setText(display_msg)
        log(display_msg)
        msg_box.exec_()
