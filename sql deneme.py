from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QFileDialog, QMessageBox, QWidget, QInputDialog, QLineEdit
import sys
import requests
import html
import sqlite3
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('oyun.sql')
if not db.open():
    print("Veritabanına bağlanılamadı:", db.lastError().text())
if db.open():
    print("tmm")




        self.setWindowTitle("Kullanıcı Listesi")

        # Layout tanımlama
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.v_layout = QVBoxLayout()
        self.central_widget.setLayout(self.v_layout)

        # ListWidget oluşturma
        self.user_list = QListWidget()
        self.v_layout.addWidget(self.user_list)

        # QPushButton oluşturma
        self.button = QPushButton("Kullanıcıları Listele")
        self.v_layout.addWidget(self.button)
        self.button.clicked.connect(self.kullanici_listele)

    def kullanici_listele(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setHostName("oyun.db")
        db.open()
        
        if not db.open():
            print("Veritabanına bağlanılamadı...")
            return []

        query = QSqlQuery("SELECT kullanici_adi FROM kullanici", db)
        users = []
        while query.next():
            user = query.value(0)
            users.append(user)
        
        db.close()

        # Kullanıcıları ListWidget'e ekleme
        self.user_list.clear()
        self.user_list.addItems(users)