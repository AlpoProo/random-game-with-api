from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QFileDialog, QMessageBox, QWidget, QInputDialog, QLineEdit, QVBoxLayout, QListWidget, QMainWindow
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import Qt, QEasingCurve
from PyQt5.QtWidgets import QTableWidget
import sys
import requests
import html
import sqlite3
from PyQt5.QtGui import QPalette, QColor
from animbutton import AnimButton

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Pencere özellikleri
        self.setWindowTitle("Oyun Made by Alperen")
        self.setGeometry(100, 100, 600, 250)

        # Arka plan rengi
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(100, 100, 100))
        palette.setColor(QPalette.Button, QColor(50, 50, 50))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.setPalette(palette)

        # Kullanıcı Adı ve Şifre Girişi
        self.kullanici_adi = QLineEdit(self)
        self.kullanici_adi.setPlaceholderText("Kullanıcı Adı")
        self.kullanici_adi.move(50, 20)
        self.kullanici_adi.setStyleSheet("background-color: #fff; color: #000; font-size: 14px;")

        self.sifre = QLineEdit(self)
        self.sifre.setEchoMode(QLineEdit.Password)
        self.sifre.setPlaceholderText("Şifre")
        self.sifre.move(50, 50)
        self.sifre.setStyleSheet("background-color: #fff; color: #000; font-size: 14px;")

        # Kullanıcı adı alanına odaklan
        self.kullanici_adi.setFocus()

        # Giriş yap butonuna tıklama olayı bağla
        self.giris_yap = QPushButton("Giriş Yap", self)
        self.giris_yap.setGeometry(180, 20, 100, 30)
        self.giris_yap.setStyleSheet("font-size: 14px; background-color: #444; color: #fff;")
        self.giris_yap.clicked.connect(self.giris_yap_clicked)

        # Animasyonlu buton oluştur
        self.anim_button = AnimButton("Kullanıcıları Listele", self)
        self.anim_button.setGeometry(280, 20, 150, 30)
        self.anim_button.setStyleSheet("font-size: 14px; background-color: #444; color: #fff;")
        self.anim_button.clicked.connect(self.kullanici_listele)

        # Kullanıcı ekle butonu
        self.kullanici_ekle = QPushButton("Kullanıcı Ekle", self)
        self.kullanici_ekle.setGeometry(180, 50, 100, 30)
        self.kullanici_ekle.setStyleSheet("font-size: 14px; background-color: #444; color: #fff;")
        self.kullanici_ekle.clicked.connect(self.kullanici_ekle_clicked)

        # Kullanıcı sil butonu
        self.kullanici_ekle = QPushButton("Kullanıcı Sil", self)
        self.kullanici_ekle.setGeometry(280, 50, 150, 30)
        self.kullanici_ekle.setStyleSheet("font-size: 14px; background-color: #444; color: #fff;")
        self.kullanici_ekle.clicked.connect(self.kullanici_sil)



        # Soru al butonu
        self.soru_al = QPushButton("Soru Al", self)
        self.soru_al.setGeometry(50, 170, 200, 50)
        self.soru_al.setStyleSheet("font-size: 18px; background-color: #555; color: #fff;")
        self.soru_al.setVisible(False)
        self.soru_al.clicked.connect(self.soru_al_clicked)

        # Puan butonu
        self.puan = QPushButton("Toplam Puanı Görüntüle", self)
        self.puan.setGeometry(300, 170, 200, 50)
        self.puan.setStyleSheet("font-size: 14px; background-color: #444; color: #fff;")
        self.puan.setVisible(False)
        self.puan.clicked.connect(self.puan_clicked)

        #Çıkış butonu
        self.cikis = QPushButton("Çıkış", self)
        self.cikis.setGeometry(250, 100, 150, 50)
        self.cikis.setStyleSheet("font-size: 16px; background-color: #fff; color: #000;")
        self.cikis.clicked.connect(QApplication.quit)





        # toplam puan
        self.toplam_puan = 0

    def giris_yap_clicked(self):
        kullanici_adi = self.kullanici_adi.text()
        sifre = self.sifre.text()

        # Veritabanından kullanıcı adı ve şifre kontrolü yapın
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("oyun.db")

        if not db.open():
            QMessageBox.critical(
                None,
                "Uyarı",
                "Veritabanına bağlanırken hata oluştu: " + db.lastError().text(),
                QMessageBox.Ok,
            )
            return

        query = QSqlQuery()
        query.prepare("SELECT * FROM kullanicilar WHERE kullanici_adi = :kullanici_adi AND sifre = :sifre")
        query.bindValue(":kullanici_adi", kullanici_adi)
        query.bindValue(":sifre", sifre)
        query.exec()

        if query.next():
            # Giriş başarılı, butonları etkinleştirin
            self.soru_al.setVisible(True)
            self.puan.setVisible(True)
            self.cikis.setVisible(True)

        else:
            # Giriş başarısız, uyarı mesajı gösterin
            QMessageBox.warning(self, "Uyarı", "Kullanıcı adı veya şifre hatalı.")

    def kullanici_ekle_clicked(self):
        kullanici_adi = self.kullanici_adi.text()
        sifre = self.sifre.text()

        if kullanici_adi and sifre:
            # Veritabanı bağlantısı
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName('oyun.db')
            db.open()

            # Veritabanında kullanıcı adı kontrolü yapalım
            query = QSqlQuery()
            query.exec(f"SELECT * FROM kullanicilar WHERE kullanici_adi='{kullanici_adi}'")
            if query.next():
                QMessageBox.warning(self, 'Hata', 'Bu kullanıcı adı zaten mevcut.')
                return

            # Veritabanına kullanıcı ekleme
            query.prepare('INSERT INTO kullanicilar (kullanici_adi, sifre) VALUES (?, ?)')
            query.addBindValue(kullanici_adi)
            query.addBindValue(sifre)
            query.exec()
            db.close()

            QMessageBox.information(self, 'Başarılı', 'Kullanıcı başarıyla eklendi.')
        else:
            QMessageBox.warning(self, 'Hata', 'Lütfen kullanıcı adı ve şifre alanlarını doldurun.')

    def kullanici_listele(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("oyun.db")

        if not db.open():
            QMessageBox.critical(
                None,
                "Uyarı",
                "Veritabanına bağlanırken hata oluştu: " + db.lastError().text(),
                QMessageBox.Ok,
            )
            return []

        query = QSqlQuery("SELECT kullanici_adi FROM kullanicilar", db)
        users = []
        while query.next():
            user = query.value(0)
            users.append(user)

        db.close()

        msg = QMessageBox()
        msg.setWindowTitle("Kullanıcılar")
        msg.setText("\n".join(users))
        msg.exec_()


    def soru_al_clicked(self):
        api = requests.get('https://opentdb.com/api.php?amount=1&category=15')
        soru = api.json()['results'][0]['question']
        soru = html.unescape(soru)
        cevap, ok_pressed = QInputDialog.getText(self, "Sorunuzun cevabını giriniz : ", soru)

        if ok_pressed and cevap:
            dogru_cevap = api.json()['results'][0]['correct_answer']
            dogru_cevap = html.unescape(dogru_cevap)

            if cevap.lower() == dogru_cevap.lower():
                QMessageBox.information(self, "Sonuç", "Doğru cevap.")
                self.toplam_puan += 10

            else:
                QMessageBox.information(self, "Sonuç", f"Yanlış cevap. Doğru cevap: {dogru_cevap}")
                
                if self.toplam_puan >= 5:
                    self.toplam_puan -= 5
        
    def kullanici_sil_clicked(self, kullanici_adi):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("oyun.db")

        if not db.open():
            QMessageBox.critical(
                None,
                "Uyarı",
                "Veritabanına bağlanırken hata oluştu: " + db.lastError().text(),
                QMessageBox.Ok,
            )
            return

        query = QSqlQuery(db)
        query.prepare("DELETE FROM kullanicilar WHERE kullanici_adi = :kullanici_adi")
        query.bindValue(":kullanici_adi", kullanici_adi)
        if not query.exec():
            QMessageBox.critical(
                None,
                "Uyarı",
                "Kullanıcı silinirken hata oluştu: " + query.lastError().text(),
                QMessageBox.Ok,
            )

        db.close()

    def kullanici_sil(self):
        kullanici_adi, ok = QInputDialog.getText(
            self, "Kullanıcı Sil", "Kullanıcı Adı:"
        )
        if ok and kullanici_adi:
            self.kullanici_sil_clicked(kullanici_adi)
    
    def puan_clicked(self):
        QMessageBox.information(self, "Puan Durumu", f"Toplam puanınız : {self.toplam_puan}")



    
app = QApplication(sys.argv)
win = AppWindow()
win.show()
sys.exit(app.exec_())