import sys
import cv2
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox

# Encrypted image path
image_path = r"C:\Users\aisha\OneDrive\Desktop\Stenography-main\encryptedImage.png"

class DecryptGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Decryption")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Enter passcode for decryption:")
        layout.addWidget(self.label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.decrypt_button = QPushButton("Decrypt Image", self)
        self.decrypt_button.clicked.connect(self.decrypt_image)
        layout.addWidget(self.decrypt_button)

        self.setLayout(layout)

    def decrypt_image(self):
        password_attempt = self.password_input.text()
        if not password_attempt:
            QMessageBox.warning(self, "Error", "Please enter the password to decrypt!")
            return

        img = cv2.imread(image_path)
        if img is None:
            QMessageBox.warning(self, "Error", "Encrypted image not found.")
            return

        n, m, z = 0, 0, 0

        # Retrieve stored password length and message length
        password_length = int(img[n, m, z])
        message_length = int(img[n + 1, m + 1, (z + 1) % 3])
        n += 2
        m += 2
        z = (z + 2) % 3
        extracted_password = ""
        # Extract stored password
        for _ in range(password_length):
            extracted_password += chr(int(img[n, m, z]))
            n += 1
            m += 1
            z = (z + 1) % 3
        # Debugging: Print extracted password
        print(f"Extracted Password: {extracted_password}")
        # Check if password is correct
        if extracted_password != password_attempt:
            QMessageBox.warning(self, "Error", "Incorrect password! Access denied.")
            return
        message = ""
        # Extract hidden message
        for _ in range(message_length):
            message += chr(int(img[n, m, z]))
            n += 1
            m += 1
            z = (z + 1) % 3
        QMessageBox.information(self, "Decryption Successful", f"Secret Message: {message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DecryptGUI()
    window.show()
    sys.exit(app.exec())
