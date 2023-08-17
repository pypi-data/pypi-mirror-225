import sys

from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)


class ProvisionUserInputs(QDialog):
    """
    TrustFlex provisional XML Dialog to get all the user input for processing
    """

    def __init__(self, parent=None, xml_type="prod_xml", cert_type="custCert"):
        """
        Init class
        """
        super(ProvisionUserInputs, self).__init__(parent)

        # Init UI
        self.setup_UI()

        # user data
        self.user_data = {}

        # Setup signals/slots
        self.setup_singals_slots()

        # Reset paths
        self.encryption_key_lineedit.setText("")
        self.csr_zip_lineedit.setText("")
        self.ca_key_lineedit.setText("")

        # Show UI for production XML only,
        # for proto XML just process the data directly
        try:
            if xml_type == "prod_xml":
                if cert_type != "custCert":
                    # Disable all csr and ca key data
                    self.csr_zip_lineedit.setEnabled(False)
                    self.csr_zip_button.setEnabled(False)
                    self.ca_key_lineedit.setEnabled(False)
                    self.ca_key_button.setEnabled(False)
                self.show()
            else:
                self.close()
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
            """Encryption Key - Load encryption key .pem file provided by Microchip"""
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

    @Slot()
    def setup_singals_slots(self):
        # Setup slots for file select buttons
        self.encryption_key_button.clicked.connect(self.encryption_file_callback)
        self.csr_zip_button.clicked.connect(self.csr_zip_file_callback)
        self.ca_key_button.clicked.connect(self.ca_key_file_callback)
        # Setup slot for close button
        self.cancel_button.clicked.connect(self.close_app)
        # Setup slot for OK button
        self.ok_button.clicked.connect(self.process_ok)

    @Slot()
    def close_app(self):
        # Close signal called from cancel button
        self.close()

    @Slot()
    def encryption_file_callback(self):
        # Callback for encryption key select button
        file_name = QFileDialog.getOpenFileName(
            None, caption="Select Encryption Key File", filter="*.pem"
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

    @Slot()
    def ca_key_file_callback(self):
        # Callback for CA key select button
        file_name = QFileDialog.getOpenFileName(
            None, caption="Select CA Key for CSR signing", filter="*.key"
        )
        if file_name[0] is not None:
            self.ca_key_lineedit.setText(file_name[0])

    @Slot()
    def process_ok(self):
        enc_key_file = self.encryption_key_lineedit.text()
        csr_zip_file = self.csr_zip_lineedit.text()
        ca_key_file = self.ca_key_lineedit.text()

        # user data
        self.user_data.update({"enc_key_file": enc_key_file})
        self.user_data.update({"csr_zip_file": csr_zip_file})
        self.user_data.update({"ca_key_file": ca_key_file})

        self.close()

    @Slot()
    def process_cancel(self):
        self.user_data.clear()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    obj = ProvisionUserInputs()
    app.exec_()
    print(obj.user_data)
