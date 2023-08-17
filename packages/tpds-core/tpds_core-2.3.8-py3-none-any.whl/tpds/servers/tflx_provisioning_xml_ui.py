import glob
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile

from cryptography.hazmat.primitives import serialization
from PySide6.QtCore import QDir, Qt, Slot
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)
from tpds.cert_tools.cert_utils import get_CSR_CN, is_key_file_password_protected
from tpds.cert_tools.sign_csr import SignCSR
from tpds.tp_utils.tp_utils import add_to_zip_archive
from tpds.xml_handler.ecc_xml_encryption import ECCXMLEncryption
from tpds.xml_handler.xml_processing import XMLProcessing

from tpds.helper import LogFacility, make_dir


class TflxProvisioningXml(QDialog):
    """
    TrustFlex provisional XML Dialog to get all the user input for processing
    """

    def __init__(self, parent=None, config_string=None):
        """
        Init class
        """
        super(TflxProvisioningXml, self).__init__(parent)
        self._log = LogFacility()

        # Config string
        self.config_string = config_string
        # Init UI
        self.setup_UI()
        # Setup signals/slots
        self.setup_singals_slots()

        # Reset paths
        self.encryption_key_lineedit.setText("")
        self.csr_zip_lineedit.setText("")
        self.ca_key_lineedit.setText("")

        # Show UI for production XML only,
        # for proto XML just process the data directly
        try:
            xml_type = json.loads(config_string).get("xml_type")
            cert_type = json.loads(config_string).get("slot_info")[12].get("cert_type")
            if xml_type == "prod_xml":
                if cert_type != "custCert":
                    # Disable all csr and ca key data
                    self.csr_zip_lineedit.setEnabled(False)
                    self.csr_zip_button.setEnabled(False)
                    self.ca_key_lineedit.setEnabled(False)
                    self.ca_key_button.setEnabled(False)
                self.show()
            else:
                self.process_data()
        except BaseException:
            QMessageBox.warning(self, "Error", "Invalid config : xml_type not found")
            self.close()

    def setup_UI(self):
        """
        Function to setup UI
        """
        # Set Window title
        self.setWindowTitle("Provisioning Package Generator")
        # Setting the minimum size
        self.setMinimumSize(500, 200)
        # Label for encryption key choosing
        self.encryption_key_label = QLabel()
        self.encryption_key_label.setText(
            """Encryption Key - Load encryption keys .zip file provided by Microchip"""
        )
        # Label for csr_zip choosing
        self.csr_zip_label = QLabel()
        self.csr_zip_label.setText("""\nCSR ZIP - Load CSRs zip file provided by Microchip""")
        # Label for CA_Key choosing
        self.ca_key_label = QLabel()
        self.ca_key_label.setText(
            """\nCA Key (optional) - Load CA Key to sign CSRs.
            If Key is provided, tool signs the CSRs and generates final package.
            If Key is not provided, tool generates Sign CSR package to sign CSRs offline.
                    Refer to readme.md in the .zip file for signing instructions."""
        )
        # QlineEdit for encryption key file name
        self.encryption_key_lineedit = QLineEdit()
        # QlineEdit for csr zip file name
        self.csr_zip_lineedit = QLineEdit()
        # QlineEdit for ca key file name
        self.ca_key_lineedit = QLineEdit()
        # Button for choosing encryption key
        self.encryption_key_button = QPushButton()
        self.encryption_key_button.setMinimumWidth(80)
        self.encryption_key_button.setText("Select")
        # Button for choosing csr zip
        self.csr_zip_button = QPushButton()
        self.csr_zip_button.setMinimumWidth(80)
        self.csr_zip_button.setText("Select")
        # Button for choosing ca key
        self.ca_key_button = QPushButton()
        self.ca_key_button.setMinimumWidth(80)
        self.ca_key_button.setText("Select")
        # Label for OK close buttons
        self.ok_close_label = QLabel()
        self.ok_close_label.setText("")
        # Window OK button
        self.ok_button = QPushButton()
        self.ok_button.setText("OK")
        # Window Cancel button
        self.cancel_button = QPushButton()
        self.cancel_button.setText("Cancel")
        # Define Layout
        ok_close_spacer = QSpacerItem(200, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # Setup Hlayouts for individual horizontal items
        enc_H = QHBoxLayout()
        enc_H.addWidget(self.encryption_key_lineedit)
        enc_H.addWidget(self.encryption_key_button)
        csr_H = QHBoxLayout()
        csr_H.addWidget(self.csr_zip_lineedit)
        csr_H.addWidget(self.csr_zip_button)
        ca_H = QHBoxLayout()
        ca_H.addWidget(self.ca_key_lineedit)
        ca_H.addWidget(self.ca_key_button)
        ok_close_H = QHBoxLayout()
        ok_close_H.addSpacerItem(ok_close_spacer)
        ok_close_H.addWidget(self.ok_button)
        ok_close_H.addWidget(self.cancel_button)
        # Combine and fit all widgets in Vertical Layout
        vlay = QVBoxLayout()
        vlay.addWidget(self.encryption_key_label)
        vlay.addLayout(enc_H)
        vlay.addWidget(self.csr_zip_label)
        vlay.addLayout(csr_H)
        vlay.addWidget(self.ca_key_label)
        vlay.addLayout(ca_H)
        vlay.addWidget(self.ok_close_label)
        vlay.addLayout(ok_close_H)
        # Set Layout
        self.setLayout(vlay)

    def setup_singals_slots(self):
        # Setup slots for file select buttons
        self.encryption_key_button.clicked.connect(self.encryption_file_callback)
        self.csr_zip_button.clicked.connect(self.csr_zip_file_callback)
        self.ca_key_button.clicked.connect(self.ca_key_file_callback)
        # Setup slot for close button
        self.cancel_button.clicked.connect(self.close_app)
        # Setup slot for OK button
        self.ok_button.clicked.connect(self.process_data)

    @Slot()
    def close_app(self):
        # Close signal called from cancel button
        self.close()

    @Slot()
    def encryption_file_callback(self):
        # Callback for encryption key select button
        file_name = QFileDialog.getOpenFileName(
            None, caption="Select Encryption Key(s) File", filter="*.zip"
        )
        if file_name[0] is not None:
            self.encryption_key_lineedit.setText(file_name[0])
        else:
            pass

    @Slot()
    def csr_zip_file_callback(self):
        # Callback for CSR ZIP select button
        file_name = QFileDialog.getOpenFileName(
            None, caption="Select CSRs zip file", filter="*.zip"
        )
        if file_name[0] is not None:
            self.csr_zip_lineedit.setText(file_name[0])
        else:
            pass

    @Slot()
    def ca_key_file_callback(self):
        # Callback for CA key select button
        file_name = QFileDialog.getOpenFileName(
            None, caption="Select CA Key for CSR signing", filter="*.key"
        )
        if file_name[0] is not None:
            self.ca_key_lineedit.setText(file_name[0])
        else:
            pass

    @Slot()
    def process_data(self):
        # Fetch file paths from lineedits
        enc_key_file = self.encryption_key_lineedit.text()
        csr_zip_file = self.csr_zip_lineedit.text()
        ca_key_file = self.ca_key_lineedit.text()

        # Locals
        curr_dir = os.getcwd()
        zip_file_list = []
        working_file = xml_file = ""
        config_string = self.config_string

        # Setup msg box
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setTextFormat(Qt.RichText)

        try:
            self._log.log("Loading json str")
            part_number = json.loads(config_string).get("part_number")
            time_stamp = datetime.now().strftime("%m%d%H%M%S")
            provisioning_zip_file = f"{part_number}_{time_stamp}"
            xml_file = f"{part_number}_{time_stamp}.xml"
            xml_type = json.loads(config_string).get("xml_type")
            cert_type = json.loads(config_string).get("slot_info")[12].get("cert_type")

            encryption_rsa_keys = ""
            if xml_type == "prod_xml":
                encryption_rsa_keys = enc_key_file
                assert os.path.exists(encryption_rsa_keys), "Enc Key is must for Production package"
                provisioning_zip_file = f"{part_number}_{time_stamp}_Prod.zip"
            else:
                self._log.log("No encryption for Proto XML")
                provisioning_zip_file = f"{part_number}_{time_stamp}_Proto.zip"

            common_name = "AB-CD_Single_Signer"
            if xml_type == "prod_xml" and cert_type == "custCert":
                csr_zip = csr_zip_file
                assert csr_zip and os.path.exists(
                    csr_zip
                ), "CSR zip is missing for production package"

                with ZipFile(csr_zip_file, "r") as zip_file:
                    file_name = zip_file.namelist()[0]
                    with open(file_name, "wb") as tempFile:
                        tempFile.write(zip_file.read(file_name))
                    common_name = get_CSR_CN(file_name)
                    os.remove(file_name)

                common_name = common_name.split()[-1]
                common_name = common_name[:2] + "-" + common_name[2:] + "_Single_Signer"

            # Removed single_signer: Provisioning team have requested not to add this tag now....
            # if cert_type == "custCert":
            #     config_string = json.loads(config_string)
            #     config_string['single_signer'] = common_name
            #     config_string = json.dumps(config_string)

            self._log.log("Setting output directory")
            provisioning_zip_dir = os.path.join(str(QDir.homePath()), "Downloads", "TPDS_Downloads")
            make_dir(provisioning_zip_dir)
            os.chdir(provisioning_zip_dir)

            self._log.log("Processing configurator string")
            xml = XMLProcessing(json.loads(config_string).get("base_xml"))
            xml.update_with_user_data(config_string)
            xml.save_root(xml_file)
            for extn in ["*.c", "*.h", "*.crt", "*.txt"]:
                zip_file_list.extend(glob.glob(extn))

            self._log.log("Processing CSRs")
            ca_key = csr_zip = sign_csr_zip = signed_crt_zip = None
            if xml_type == "prod_xml" and cert_type == "custCert":
                self._log.log("CustomPKI and Production XML is selected by user")
                csr_zip = csr_zip_file
                ca_key = ca_key_file
                if ca_key and os.path.exists(ca_key) and csr_zip and os.path.exists(csr_zip):
                    self._log.log("Processing CSR signing request")
                    ca_key_password = None
                    if is_key_file_password_protected(ca_key):
                        self._log.log("Processing ca_key password")
                        tB, accept = QInputDialog.getText(
                            None,
                            "Key Password",
                            ("CA Key is Protected with Password. " "Provide password here"),
                        )
                        if accept:
                            ca_key_password = tB.encode("utf-8")
                    self._log.log("Reading CSRs zip file")
                    with ZipFile(csr_zip) as zf:
                        for file_name in zf.namelist():
                            with open(file_name, "wb") as kf:
                                kf.write(zf.read(file_name))
                            obj = SignCSR(file_name)
                            obj.sign_csr("signer.crt", ca_key, ca_key_password)
                            os.remove(file_name)
                            file_name = Path(file_name).stem.replace("_CSR", "") + ".cer"
                            Path(file_name).write_bytes(
                                obj.signer_crt.public_bytes(encoding=serialization.Encoding.DER)
                            )
                        ca_cert_zip_list = glob.glob("*.cer")
                        signed_crt_zip = f"{part_number}_{time_stamp}_ca_cert.zip"
                        add_to_zip_archive(signed_crt_zip, ca_cert_zip_list)
                        for file in ca_cert_zip_list:
                            os.remove(file)
                else:
                    self._log.log("Generating sign_CSR zip for offline processing")
                    sign_csr_zip = f"{part_number}_{time_stamp}_sign_csr.zip"
                    shutil.copy(
                        os.path.join(os.path.dirname(__file__), "..", "certs", "sign_csr.zip"),
                        sign_csr_zip,
                    )
                    z = ZipFile(sign_csr_zip, "a")
                    z.write("signer.crt")
                    z.close()
            else:
                self._log.log("No CSR processing for non CustomPKI-ProdXML")

            working_file = "current_key.xml"
            if os.path.exists(encryption_rsa_keys):
                self._log.log("Reading encryption keys zip file")
                with ZipFile(encryption_rsa_keys) as zf:
                    for file_name in zf.namelist():
                        site_codes = [
                            "ASEK",
                            "ASES",
                            "COSP",
                            "COSD",
                            "MTAI",
                            "UTAC",
                            "AIC",
                            "MPHL",
                        ]
                        xml_matches = [match for match in site_codes if match in file_name]
                        if len(xml_matches):
                            xml_out = f"{part_number}_{xml_matches[0]}.ENC.xml"
                        else:
                            raise ValueError(f"Unknown key file:{file_name}")

                        with open(working_file, "wb") as kf:
                            kf.write(zf.read(file_name))
                        xml = ECCXMLEncryption(xml_file, working_file, xml_out)
                        xml.perform_encryption()
            else:
                self._log.log("No XML encryption is taken place")

            self._log.log("Archive Provisioning files to Zip")
            zip_file_list.extend(
                glob.glob("*.ENC.xml")
            ) if xml_type == "prod_xml" else zip_file_list.extend(glob.glob("*.xml"))
            add_to_zip_archive(provisioning_zip_file, zip_file_list)

            path_link = os.path.join(provisioning_zip_dir, provisioning_zip_file).replace("\\", "/")
            display_msg = (
                f"<font color=#0000ff>"
                f"<b>Provisioning Package is saved.</b></font><br><br>"
                f"""Package: <a href='{path_link}'>"""
                f"""{path_link}</a><br>"""
            )

            if sign_csr_zip:
                path_link = os.path.join(provisioning_zip_dir, sign_csr_zip).replace("\\", "/")
                display_msg += (
                    f"""Scripts to Sign CSRs: <a href='{path_link}'>""" f"""{path_link}</a>"""
                )
            elif signed_crt_zip:
                path_link = os.path.join(provisioning_zip_dir, signed_crt_zip).replace("\\", "/")
                display_msg += f"""Signed Certs: <a href='{path_link}'>""" f"""{path_link}</a>"""

        except BaseException as e:
            if "EC key" in str(e):
                e = str(e).replace("EC key", "ECC key")
            display_msg = f"Provisioning Package process failed with:\n{e}"
            msg_box.setIcon(QMessageBox.Critical)

        finally:
            os.remove(working_file) if os.path.exists(working_file) else None
            os.remove(xml_file) if os.path.exists(xml_file) else None
            for file in zip_file_list:
                os.remove(file) if os.path.exists(file) else None
            os.chdir(curr_dir)
            msg_box.setText(display_msg)
            msg_box.exec_()
            self.close_app()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    obj = TflxProvisioningXml()
    obj.start_ui("asd")
    sys.exit(app.exec_())
