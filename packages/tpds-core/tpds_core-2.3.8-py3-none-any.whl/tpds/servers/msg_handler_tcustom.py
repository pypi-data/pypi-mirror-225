import cryptoauthlib as cal
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox
from tpds.secure_element import ECC608A
from tpds.secure_element.constants import Constants

from tpds.helper import log


def trust_custom_write_config(config_data, addr=0xC0):
    log("Loading Configuration to TrustCUSTOM part")
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.setWindowTitle("TrustCUSTOM - Write Config")
    msg_box.setTextFormat(Qt.RichText)
    display_msg = "<font color=#0000ff><b>ECC6608 TrustCustom Load Configuration" "</b></font><br>"
    try:
        device = ECC608A(address=addr)
        log(f"Device details: {device.get_device_details()}")
        if device.is_config_zone_locked():
            display_msg += "<br>Cannot be written as Configuration is locked.<br>"
            msg_box.setIcon(QMessageBox.Warning)
        else:
            config_data = config_data.replace("\n", "").replace(" ", "")[32:]
            log(f"Configuration data: {config_data}")
            device.load_config_zone(bytearray.fromhex(config_data))
            display_msg += """<br>Loading completed!<br>"""
    except BaseException as e:
        display_msg += f"""<br>Writing Configuration failed with '{e}'.<br>"""
        msg_box.setIcon(QMessageBox.Warning)

    msg_box.setText(display_msg)
    msg_box.exec_()


def trust_custom_read_config(addr=0xC0):
    log("Reading Configuration from TrustCUSTOM part")
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.setWindowTitle("TrustCUSTOM - Read Config")
    msg_box.setTextFormat(Qt.RichText)
    display_msg = "<font color=#0000ff><b>ECC6608 TrustCustom Read Configuration" "</b></font><br>"
    config_data = ""

    try:
        device = ECC608A(address=addr)
        log(f"Device details: {device.get_device_details()}")
        config_data = bytearray(128)
        assert (
            cal.atcab_read_bytes_zone(
                Constants.ATCA_CONFIG_ZONE, 0, 0, config_data, len(config_data)
            )
            == cal.Status.ATCA_SUCCESS
        ), "Reading Config zone failed."
        config_data = config_data.hex().upper()
        display_msg += """<br>Reading completed!<br>"""

    except BaseException as e:
        display_msg += f"""<br>Reading configuration failed with '{e}'.<br>"""
        msg_box.setIcon(QMessageBox.Warning)

    msg_box.setText(display_msg)
    msg_box.exec_()

    return config_data
