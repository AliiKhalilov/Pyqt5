import sys
from PyQt5.QtWidgets import *
import sqlite3
class Window1(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: lightblue")
        self.database()
        self.components()
        self.show()
    def components(self):
        self.labelname = QLabel("Username", self)
        self.labelpass = QLabel("Password", self)
        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.okey = QPushButton("Submit", self)
        self.okey.setStyleSheet("background-color: yellow")
        self.register = QPushButton("Register", self)
        self.register.setStyleSheet("background-color: darkblue")
        self.space = QLabel("               ", self)
        self.v_box = QVBoxLayout()
        self.v_box.addWidget(self.labelname)
        self.v_box.addWidget(self.username)
        self.v_box.addWidget(self.labelpass)
        self.v_box.addWidget(self.password)
        self.v_box.addStretch()
        self.v_box.addWidget(self.space)
        self.v_box.addWidget(self.okey)
        self.v_box.addWidget(self.register)
        h_box = QHBoxLayout()
        h_box.addStretch()  # Pushes items to the left
        h_box.addLayout(self.v_box)
        h_box.addStretch()  # Pushes items to the right
        self.setLayout(h_box)
        self.setWindowTitle("Ali's Page")
        self.okey.clicked.connect(self.login)
        self.register.clicked.connect(self.signin)
    def database(self):
        self.connection = sqlite3.connect("Ali_Database.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS USERS (NAME TEXT, PASSWORD TEXT)")
        self.connection.commit()
    def login(self):
        x = self.username.text()
        y = self.password.text()
        self.cursor.execute("SELECT * FROM USERS WHERE NAME=? AND PASSWORD=?", (x, y))
        data = self.cursor.fetchall()
        if len(data) == 0:
            self.space.setText("Username or Password is wrong.\n Please input again correctly")
        else:
            self.space.setText("Welcome, " + x)
    def signin(self):
        self.w = Window2(self.cursor)  # Pass the cursor to the next window
        self.w.show()
        self.hide()
class Window2(Window1):
    def __init__(self, cursor):
        super().__init__()  # Call the init method of Window1 to perform the configurations.
        self.setStyleSheet("background-color: lightpink")
        self.cursor = cursor
        self.setWindowTitle("Registration Page")
        self.okey.clicked.connect(self.signin2)  # Update the link of the Okay button.
        self.v_box.removeWidget(self.register)
        self.register.deleteLater()
    def signin2(self):
        x = self.username.text()
        y = self.password.text()
        self.cursor.execute("SELECT * FROM USERS")
        liste = self.cursor.fetchall()
        selected = [item[0] for item in liste]
        if x in selected:
            self.space.setText("This username is already used")
        else:
            self.cursor.execute("INSERT INTO USERS VALUES (?, ?)", (x, y))
            self.cursor.connection.commit()
            self.space.setText("Registration successful!")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window1()
    sys.exit(app.exec_())
