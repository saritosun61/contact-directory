# pyuic5 -o telefon_rehberi_2.py telefon_rehberi.ui
# pyrcc5 -o ikonlarim_rc.py ikonlarim.qrc

from PyQt5.QtWidgets import *
from telefon_rehberi import *
import sys
import sqlite3

class TelefonRehberi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_TelefonRehberim()
        self.ui.setupUi(self)
        self.ui.pushButton_cikis.clicked.connect(self.cikis)
        self.ui.pushButton_guncelle.clicked.connect(self.guncelle)
        self.ui.pushButton_kaydet.clicked.connect(self.kaydet)
        self.ui.pushButton_listele.clicked.connect(self.listele)
        self.ui.pushButton_sil.clicked.connect(self.sil)
        self.ui.lineEdit_ara.textChanged.connect(self.ara)
        self.ui.action_cikis.triggered.connect(self.cikis)
        self.ui.action_Guncelle.triggered.connect(self.guncelle)
        self.ui.action_Listele.triggered.connect(self.listele)
        self.ui.action_Sil.triggered.connect(self.sil)
        self.ui.action_Kaydet.triggered.connect(self.kaydet)
        self.ui.tableWidget_tablo.itemSelectionChanged.connect(self.tablo_secim)
        self.vt = sqlite3.connect("telefonRehberi.db3")
        self.im = self.vt.cursor()
        self.im.execute("""CREATE TABLE IF NOT EXISTS rehber 
        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        adi TEXT NOT NULL,
        soyadi TEXT NOT NULL,
        telefon TEXT NOT NULL UNIQUE,
        tip TEXT NOT NULL 
                        )
                """)
        self.vt.commit()


    def cikis(self):
        self.vt.close()
        pencere.close()
        uygulama.quit()
        sys.exit()
    def guncelle(self):
        a,b,c,d = self.oku()
        self.im.execute("UPDATE rehber SET adi=?, soyadi=?,telefon=?,tip=? WHERE id=?",(a,b,c,d,self.id))
        self.vt.commit()
        QMessageBox.information(self,"Güncelleme",f"{a} {b}'nin kaydı güncellendi!",QMessageBox.Ok)
        self.temizle()
        self.listele()
    def oku(self):
        a = self.ui.lineEdit_adi.text()
        b = self.ui.lineEdit_soyadi.text()
        c = self.ui.lineEdit_telefon.text()
        if self.ui.radioButton_cep.isChecked():
            d = "Cep"
        elif self.ui.radioButton_ev.isChecked():
            d = "Ev"
        elif self.ui.radioButton_is.isChecked():
            d = "İş"
        else:
            d = "null"
        return a,b,c,d
    def kaydet(self):
        a,b,c,d = self.oku()
        self.im.execute("""INSERT INTO rehber (adi,soyadi,telefon,tip)
                VALUES(?,?,?,?)""",(a,b,c,d))
        self.vt.commit()
        QMessageBox.information(self,"Kaydet","Kayıt başarıyla eklendi",QMessageBox.Yes)
        self.temizle()
        self.listele()
    def temizle(self):
        self.ui.lineEdit_adi.clear()
        self.ui.lineEdit_soyadi.clear()
        self.ui.lineEdit_telefon.clear()
        self.ui.radioButton_cep.setChecked(False)
        self.ui.radioButton_is.setChecked(False)
        self.ui.radioButton_ev.setChecked(False)

    def listele(self):
        self.ui.tableWidget_tablo.clear()
        self.ui.tableWidget_tablo.setHorizontalHeaderLabels(("ID","ADI","SOYADI","TELEFON","TİP"))
        self.im.execute("SELECT * FROM rehber")
        for satır_indeks,satır_veri in enumerate(self.im):
            for sutun_indeks,sutun_veri in enumerate(satır_veri):
                self.ui.tableWidget_tablo.setItem(satır_indeks,sutun_indeks,QTableWidgetItem(str(sutun_veri)))
    
    def sil(self):
        yanıt = QMessageBox.question(self,"Sil","Silmek istediğinize emin minisiz?",QMessageBox.Yes|QMessageBox.No)
        if yanıt == QMessageBox.Yes:
            self.im.execute(f"DELETE FROM rehber WHERE id={self.id}")
            self.vt.commit()
            self.ui.statusbar.showMessage("Silme işlemi başarıyla gerçekleşti!",3000)
            self.temizle()
            self.listele()
        else:
            self.ui.statusbar.showMessage("Silme işlemi iptal edildi!",3000)
    def ara(self):
        ara = self.ui.lineEdit_ara.text()
        self.im.execute(f"""SELECT * FROM rehber WHERE 
                        adi LIKE '%{ara}%' OR 
                        soyadi LIKE '%{ara}%' OR 
                        telefon LIKE '%{ara}%' OR 
                        tip LIKE '%{ara}%' OR
                        id LIKE '%{ara}%'""")
        self.ui.tableWidget_tablo.clear()
        self.ui.tableWidget_tablo.setHorizontalHeaderLabels(("ID","ADI","SOYADI","TELEFON","TİP"))
        for satır_indeks,satır_veri in enumerate(self.im):
            for sutun_indeks,sutun_veri in enumerate(satır_veri):
                self.ui.tableWidget_tablo.setItem(satır_indeks,sutun_indeks,QTableWidgetItem(str(sutun_veri)))
    
    def tablo_secim(self):
        try:
            self.secilen = self.ui.tableWidget_tablo.selectedItems()
            self.id = int(self.secilen[0].text())
            self.ui.lineEdit_adi.setText(self.secilen[1].text())
            self.ui.lineEdit_soyadi.setText(self.secilen[2].text())
            self.ui.lineEdit_telefon.setText(self.secilen[3].text())
            d = self.secilen[4].text()
            if d == "Ev":
                self.ui.radioButton_ev.setChecked(True)
            elif d == "Cep":
                self.ui.radioButton_cep.setChecked(True)
            elif d == "İş":
                self.ui.radioButton_is.setChecked(True)
            else:
                self.ui.radioButton_cep.setChecked(False)
                self.ui.radioButton_ev.setChecked(False)
                self.ui.radioButton_is.setChecked(False)
        except:
            pass


if __name__ == "__main__":
    uygulama = QApplication(sys.argv)
    pencere = TelefonRehberi()
    pencere.show()
    sys.exit(uygulama.exec_())



