import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QApplication, \
    QSystemTrayIcon, QMenu, QAction, qApp, QVBoxLayout, QMessageBox, QDialog, QComboBox, QCheckBox
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon, QPixmap, QRegExpValidator
from PyQt5.QtCore import Qt, QThread
from datetime import datetime, timedelta
from PIL import Image
from connDB import ConnectDB
from time import sleep
from functions import *
from api import Api

conexaoODBC = conectar()


class WindowConciliador(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conciliador")
        self.resize(796, 350)
        self.setStyleSheet("background-color: #262D37")
        self.setWindowIcon(QtGui.QIcon("icone.ico"))

        self.Ui_Informacoes()

        self.lblData = QLabel(self)
        self.lblData.setGeometry(28, 250, 130, 25)
        self.lblData.setText("Apartir de")
        self.lblData.setStyleSheet("font-size: 20px; color: #fff")
        self.txtData = QLineEdit(self)
        self.txtData.setGeometry(20, 290, 110, 35)
        self.txtData.setStyleSheet(
            "font-size: 15px; border: 2px solid #fff; border-radius: 5px; background-color: #262D37; color: #fff")
        self.txtData.setInputMask("99/99/9999")
        self.txtData.setText(dataAtual())
        self.txtData.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)

        self.lblAte = QLabel(self)
        self.lblAte.setGeometry(155, 250, 150, 25)
        self.lblAte.setText("Até")
        self.lblAte.setStyleSheet("font-size: 20px; color: #fff")
        self.lblMessage = QLabel(self)
        self.lblMessage.setText("Obrigatório somente para baixar dados")
        self.lblMessage.setStyleSheet("font-size: 10px; color: #fff")
        self.lblMessage.setGeometry(145, 325, 175, 25)
        self.checkBox = QCheckBox(self)
        self.checkBox.setGeometry(227, 253, 42, 27)
        self.checkBox.setChecked(True)
        self.checkBox.setStyleSheet(
            """
                QCheckBox::indicator:pressed {
                    background-color : lightblue;
                }
            """
        )
        self.txtAte = QLineEdit(self)
        self.txtAte.setGeometry(145, 290, 110, 35)
        self.txtAte.setInputMask("99/99/9999")
        try:
            conn = ConnectDB(conexaoODBC)
            conn.conecta()
            sqlCartoes = "select data from cartoesconcvendas order by data desc limit 1"
            conn.execute(sqlCartoes)
            lastDateCartoes = conn.fetchall_dict()
            if len(lastDateCartoes) == 0:
                dateCartoes = False
            else:
                dateCartoes = datetime.strptime(str((lastDateCartoes[0]['data'])), '%Y-%m-%d %H:%M:%S').strftime(
                    '%d/%m/%Y')
            sqlPagamentos = "select datarecebe from cartoesconcpag order by datarecebe desc limit 1"
            conn.execute(sqlPagamentos)
            lastDatePagamentos = conn.fetchall_dict()
            if len(lastDatePagamentos) == 0:
                datePagamentos = False
            else:
                datePagamentos = datetime.strptime(str(lastDatePagamentos[0]['datarecebe']),
                                                   '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
            if dateCartoes:
                pass
                # self.txtAte.setText(dateCartoes)
            elif datePagamentos:
                pass
                # self.txtAte.setText(datePagamentos)
            else:
                self.txtAte.setInputMask("99/99/9999")
        except Exception as e:
            print(e)
        self.txtAte.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
        self.checkBoxChecked()

        self.lblLoja = QLabel(self)
        self.lblLoja.setGeometry(300, 250, 37, 25)
        self.lblLoja.setText("Loja")
        self.lblLoja.setStyleSheet("font-size: 20px; color: #fff")
        self.txtLoja = QLineEdit(self)
        self.txtLoja.setGeometry(270, 290, 110, 35)
        self.txtLoja.setStyleSheet(
            "font-size: 15px; border: 2px solid #fff; border-radius: 5px; background-color: #262D37; color: #fff")
        self.txtLoja.setInputMask("9")
        self.txtLoja.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)

        self.buttonLimparDados = QPushButton(self)
        self.buttonLimparDados.setGeometry(400, 250, 105, 35)
        self.buttonLimparDados.setText("Limpar")
        self.buttonLimparDados.setStyleSheet("""
                                        QPushButton {
                                              align-items: center;
                                              appearance: button;
                                              background-color: #0276FF;
                                              border-radius: 8px;
                                              border-style: none;
                                              box-shadow: rgba(255, 255, 255, 0.26) 0 1px 2px inset;
                                              box-sizing: border-box;
                                              color: #fff;
                                              cursor: pointer;
                                              display: flex;
                                              flex-direction: row;
                                              flex-shrink: 0;
                                              font-family: "RM Neue",sans-serif;
                                              font-size: 16px;
                                              line-height: 1.15;
                                              margin: 0;
                                              text-align: center;
                                              text-transform: none;
                                              transition: color .13s ease-in-out,background .13s ease-in-out,opacity .13s ease-in-out,box-shadow .13s ease-in-out;
                                              user-select: none;
                                              -webkit-user-select: none;
                                              touch-action: manipulation;
                                        }
                                        QPushButton:hover {
                                              background-color: #1C84FF;
                                        }
                                        QPushButton:pressed {
                                              background-color: #006AE8;
                                        }
                                        """)

        self.buttonBaixarDados = QPushButton(self)
        self.buttonBaixarDados.setGeometry(400, 291, 105, 40)
        self.buttonBaixarDados.setText("Baixar\nDados")
        self.buttonBaixarDados.setStyleSheet("""
                                        QPushButton {
                                              align-items: center;
                                              appearance: button;
                                              background-color: #0276FF;
                                              border-radius: 8px;
                                              border-style: none;
                                              box-shadow: rgba(255, 255, 255, 0.26) 0 1px 2px inset;
                                              box-sizing: border-box;
                                              color: #fff;
                                              cursor: pointer;
                                              display: flex;
                                              flex-direction: row;
                                              flex-shrink: 0;
                                              font-family: "RM Neue",sans-serif;
                                              font-size: 16px;
                                              line-height: 1.15;
                                              text-align: center;
                                              text-transform: none;
                                              transition: color .13s ease-in-out,background .13s ease-in-out,opacity .13s ease-in-out,box-shadow .13s ease-in-out;
                                              user-select: none;
                                              -webkit-user-select: none;
                                              touch-action: manipulation;
                                        }
                                        QPushButton:hover {
                                              background-color: #1C84FF;
                                        }
                                        QPushButton:pressed {
                                              background-color: #006AE8;
                                        }
                                        """)

        self.buttonEnviar = QPushButton(self)
        self.buttonEnviar.setGeometry(510, 250, 250, 35)
        self.buttonEnviar.setText("Enviar")
        self.buttonEnviar.setStyleSheet("""
                                        QPushButton {
                                              align-items: center;
                                              appearance: button;
                                              background-color: #0276FF;
                                              border-radius: 8px;
                                              border-style: none;
                                              box-shadow: rgba(255, 255, 255, 0.26) 0 1px 2px inset;
                                              box-sizing: border-box;
                                              color: #fff;
                                              cursor: pointer;
                                              display: flex;
                                              flex-direction: row;
                                              flex-shrink: 0;
                                              font-family: "RM Neue",sans-serif;
                                              font-size: 16px;
                                              line-height: 1.15;
                                              margin: 0;
                                              padding: 10px 21px;
                                              text-align: center;
                                              text-transform: none;
                                              transition: color .13s ease-in-out,background .13s ease-in-out,opacity .13s ease-in-out,box-shadow .13s ease-in-out;
                                              user-select: none;
                                              -webkit-user-select: none;
                                              touch-action: manipulation;
                                        }
                                        QPushButton:hover {
                                              background-color: #1C84FF;
                                        }
                                        QPushButton:pressed {
                                              background-color: #006AE8;
                                        }
                                        """)

        self.buttonFechar = QPushButton(self)
        self.buttonFechar.setGeometry(510, 296, 250, 35)
        self.buttonFechar.setText("Fechar")
        self.buttonFechar.setStyleSheet("""
                                        QPushButton {
                                              align-items: center;
                                              appearance: button;
                                              background-color: #FF0000;
                                              border-radius: 8px;
                                              border-style: none;
                                              box-shadow: rgba(255, 255, 255, 0.26) 0 1px 2px inset;
                                              box-sizing: border-box;
                                              color: #fff;
                                              cursor: pointer;
                                              display: flex;
                                              flex-direction: row;
                                              flex-shrink: 0;
                                              font-family: "RM Neue",sans-serif;
                                              font-size: 16px;
                                              line-height: 1.15;
                                              margin: 0;
                                              padding: 10px 21px;
                                              text-align: center;
                                              text-transform: none;
                                              transition: color .13s ease-in-out,background .13s ease-in-out,opacity .13s ease-in-out,box-shadow .13s ease-in-out;
                                              user-select: none;
                                              -webkit-user-select: none;
                                              touch-action: manipulation;
                                        }
                                        QPushButton:hover {
                                              background-color: #FF1612;
                                        }
                                        QPushButton:pressed {
                                              background-color: #FF0000;
                                        }
                                        """)
        self.buttonLimparDados.clicked.connect(self.limparDados)
        self.buttonBaixarDados.clicked.connect(self.baixarDados)
        self.buttonFechar.clicked.connect(sys.exit)
        self.buttonEnviar.clicked.connect(self.enviarVendas)
        self.checkBox.clicked.connect(self.checkBoxChecked)
        self.txtData.setFocus()

        # Desabilitar botão "Maximizar" e "Fechar"
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint & ~Qt.WindowCloseButtonHint)
        self.create_taskbar_icon()
        # Criar sinal personalizado para lidar com a minimização
        self.minimize_action_triggered = False

    def Ui_Informacoes(self):
        self.janelaDeInformacoes = QTextEdit(self)
        self.janelaDeInformacoes.setGeometry(13, 10, 770, 221)
        self.janelaDeInformacoes.setStyleSheet(
            "background-color: #262D37; color: #fff; border: 2px solid #fff; border-radius: 5px; font-family: Arial; font-size: 15px")

        # Cria um layout e adiciona o QTextEdit a ele
        layout = QVBoxLayout()
        layout.addWidget(self.janelaDeInformacoes)

        # Define as margens do layout para ajustar a altura
        layout.setContentsMargins(11, 10, 10, 115)

        # Cria o widget principal e define o layout nele
        main_widget = QWidget(self)
        main_widget.setLayout(layout)
        main_widget.setGeometry(13, 10, 770, 221)
        self.setCentralWidget(main_widget)

    def create_taskbar_icon(self):
        self.icon = Image.open("icone.ico")  # Substitua "logo.png" pelo caminho real do arquivo de ícone
        menu = QMenu()
        restore_action = QAction("Abrir", self)
        restore_action.triggered.connect(self.maximizar_app)
        menu.addAction(restore_action)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icone.ico"))
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def maximizar_app(self):
        self.show_normal()
        self.minimize_action_triggered = False
        window.close()
        login.txtNumUsuario.setFocus()
        login.txtNumUsuario.setText("")
        login.txtUsuario.setCurrentIndex(0)
        login.txtSenha.setText("")
        login.lblMessage.setText("")
        login.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.setVisible(True)

    def changeEvent(self, event):
        if self.isMinimized() and not self.minimize_action_triggered:
            self.hide()
            self.tray_icon.setVisible(True)
            event.ignore()  # Impede o evento de mudança de estado de janela padrão

    def show_normal(self):
        self.tray_icon.setVisible(False)
        self.showNormal()
        self.activateWindow()

    def quit_application(self):
        self.tray_icon.setVisible(False)
        qApp.quit()

    def checkBoxChecked(self):
        if self.checkBox.isChecked():
            self.txtAte.setDisabled(True)
            self.txtAte.setStyleSheet(
                "font-size: 15px; border: 2px solid #fff; border-radius: 5px; background-color: #262D37; color: #grey")
        else:
            self.txtAte.setEnabled(True)
            self.txtAte.setFocus()
            self.txtAte.setStyleSheet(
                "font-size: 15px; border: 2px solid #fff; border-radius: 5px; background-color: #262D37; color: #fff")

    def enviarVendas(self):
        if self.txtData.text() == "//" or self.txtLoja.text() == "":
            msg = QMessageBox()
            msg.setWindowTitle("Aviso")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Preencha todos os campos!")
            msg.exec()
        else:
            conn = ConnectDB(conexaoODBC)
            conn.conecta()
            sqlEmpresa = f"select cnpj, conctoken from empresa where loja={self.txtLoja.text()}"
            conn.execute(sqlEmpresa)
            empresa = conn.fetchall_dict()
            if not empresa:
                msg = QMessageBox()
                msg.setWindowTitle("Aviso")
                msg.setIcon(QMessageBox.Information)
                msg.setText(f"Loja {self.txtLoja.text()} não existe")
                msg.exec()
            else:
                worker = WorkerThread(self)
                worker.start()

    def baixarDados(self):
        if self.txtData.text() == "//" or self.txtAte.text() == "//" or self.txtLoja.text() == "":
            msg = QMessageBox()
            msg.setWindowTitle("Aviso")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Preencha todos os campos!")
            msg.exec()
            return

        conn = ConnectDB(conexaoODBC)
        conn.conecta()
        sqlEmpresa = f"select cnpj, conctoken from empresa where loja={int(self.txtLoja.text())}"
        conn.execute(sqlEmpresa)
        empresa = conn.fetchall_dict()
        if not empresa:
            msg = QMessageBox()
            msg.setWindowTitle("Aviso")
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"Loja {self.txtLoja.text()} não existe")
            msg.exec()
            return

        apartirText = self.txtData.text()
        ateText = self.txtAte.text()
        apartirDate = datetime.strptime(apartirText, "%d/%m/%Y")
        ateDate = datetime.strptime(ateText, "%d/%m/%Y")

        # Calcula a diferença em dias entre as datas
        diffDias = (ateDate - apartirDate).days

        if diffDias > 4:
            msg = QMessageBox()
            msg.setWindowTitle("Aviso")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Você só pode baixar até 5 dias")
            msg.exec()
            return
        elif diffDias < 0:
            msg = QMessageBox()
            msg.setWindowTitle("Aviso")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Até não pode ser menor que Apartir")
            msg.exec()
            return

        self.janelaDeInformacoes.append("Por favor aguarde...\n")
        self.txtLoja.setDisabled(True)
        self.txtData.setDisabled(True)
        self.txtAte.setDisabled(True)
        self.checkBox.setChecked(True)
        self.checkBox.setDisabled(True)
        self.buttonBaixarDados.setDisabled(True)
        self.buttonEnviar.setDisabled(True)
        self.buttonFechar.setDisabled(True)
        try:
            worker = WorkerThreadGet(self)
            worker.start()
        except Exception as e:
            print(e)
            self.janelaDeInformacoes.append("Ocorreu um erro!")
            self.buttonBaixarDados.setEnabled(True)
            self.buttonEnviar.setEnabled(True)
            self.buttonFechar.setEnabled(True)
            self.txtData.setEnabled(True)
            self.txtAte.setEnabled(True)
            self.checkBox.setEnabled(True)
            self.txtLoja.setEnabled(True)

    def limparDados(self):
        self.janelaDeInformacoes.setText("")


class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(400, 400)
        self.setStyleSheet("QMainWindow {background-color: #A5CCD1; border-radius: 10px}")
        self.setWindowIcon(QtGui.QIcon("icone.ico"))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        self.title = QLabel(self)
        self.title.setText("Conciliador")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4F4F4F; font-family: Arial")
        self.title.setGeometry(145, 40, 110, 70)

        self.imgCupom = QLabel(self)
        self.imgCupom.setGeometry(170, 15, 80, 70)
        self.pixmap = QPixmap('icone.ico')
        self.pixmap = self.pixmap.scaled(60, 40)
        self.imgCupom.setPixmap(self.pixmap)
        self.imgCupom.resize(self.pixmap.width(), self.pixmap.height())

        self.lblMessage = QLabel(self)
        self.lblMessage.setText("")
        self.lblMessage.setStyleSheet("QLabel {color: #ff0000; font-size: 12px; font-family: Arial}")
        self.lblMessage.setGeometry(127, 293, 150, 40)

        self.lblNumUsuario = QLabel(self)
        self.lblNumUsuario.setText("N° Usuário")
        self.lblNumUsuario.setStyleSheet("QLabel {font-size: 14px; font-family: Arial; font-weight: bold}")
        self.lblNumUsuario.setGeometry(160, 80, 80, 70)
        self.txtNumUsuario = QLineEdit(self)
        self.txtNumUsuario.setGeometry(130, 130, 140, 25)
        self.txtNumUsuario.setStyleSheet("QLineEdit {border-radius: 5px; font-size: 11px; font-weight: bold}")
        self.txtNumUsuario.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
        rx = QtCore.QRegExp("[0-9]{3}")  # +++
        val = QRegExpValidator(rx)  # +++
        self.txtNumUsuario.setValidator(val)

        self.lblUsuario = QLabel(self)
        self.lblUsuario.setText("Usuários")
        self.lblUsuario.setStyleSheet("QLabel {font-size: 14px; font-family: Arial; font-weight: bold}")
        self.lblUsuario.setGeometry(165, 145, 80, 70)
        self.txtUsuario = QComboBox(self)
        self.txtUsuario.setGeometry(130, 195, 140, 25)
        self.txtUsuario.setStyleSheet("QComboBox {background-color: #fff; color: black; border-radius: 5px;\
                                     border-color: lightgray; border-style: solid;} \
                                     QComboBox::down-arrow {image: url(arrow-down.ico); width: 10px} \
                                     QComboBox::drop-down {border:none;}")
        try:
            conn = ConnectDB(conexaoODBC)
            conn.conecta()
            sqlAcesso = "select id, nome from acesso"
            conn.execute(sqlAcesso)
            acessos = conn.fetchall()
            qtdAcesso = 0
            for i in acessos:
                self.txtUsuario.addItem(acessos[qtdAcesso][1])
                qtdAcesso += 1
        except AttributeError:
            self.lblMessage.setGeometry(153, 293, 150, 40)
            self.lblMessage.setText("Erro de Conexão!")

        self.lblSenha = QLabel(self)
        self.lblSenha.setText("Senha")
        self.lblSenha.setStyleSheet("QLabel {font-size: 14px; font-family: Arial; font-weight: bold}")
        self.lblSenha.setGeometry(175, 215, 80, 70)
        self.txtSenha = QLineEdit(self)
        self.txtSenha.setEchoMode(QLineEdit.Password)
        rx = QtCore.QRegExp("[0-9]{10}")  # +++
        val = QRegExpValidator(rx)  # +++
        self.txtSenha.setValidator(val)
        self.txtSenha.setGeometry(130, 265, 140, 25)
        self.txtSenha.setStyleSheet("QLineEdit {border-radius: 5px; font-size: 12px; font-weight: 500}")
        self.txtSenha.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)

        self.btnEntrar = QPushButton(self)
        self.btnEntrar.setText("Entrar")
        self.btnEntrar.setStyleSheet("""
                                    QPushButton {
                                        border-radius: 5px; 
                                        font-size: 13px; 
                                        font-weight: bold;
                                        background-color: #fff;
                                        font-family: Arial
                                    }
                                    QPushButton:hover {
                                        background-color: #FCFF6C
                                    }
                                    QPushButton:pressed {
                                        background-color: #ffff80
                                    }
        """)
        self.btnEntrar.setGeometry(140, 335, 120, 40)
        self.btnEntrar.clicked.connect(lambda: self.validarUsuario(self.txtNumUsuario.text(),
                                                                   self.txtUsuario.currentText(),
                                                                   self.txtSenha.text()))

    def validarUsuario(self, idUser, user, password):
        if idUser == "" or user == "" or password == "":
            msg = QMessageBox()
            msg.setWindowTitle("Aviso")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Preencha todos os campos!")
            msg.exec()
            self.txtNumUsuario.setFocus()
        else:
            try:
                conn = ConnectDB(conexaoODBC)
                conn.conecta()
                sqlUsuario = f"select coalesce(nome, ''), coalesce(senha, 0) from acesso where id={idUser}"
                conn.execute(sqlUsuario)
                usuario = conn.fetchone()
                if not usuario:
                    raise ValueError
                nomeBanco = usuario[0]
                senhaBanco = usuario[1]
                if nomeBanco == user and senhaBanco == int(password):
                    window.show()
                    login.close()
                else:
                    raise ValueError

            except ValueError:
                self.txtNumUsuario.setText("")
                self.txtSenha.setText("")
                self.lblMessage.setText("Usuário ou senha inválido")
                self.txtNumUsuario.setFocus()

            except Exception:
                self.lblMessage.setGeometry(147, 293, 150, 40)
                self.lblMessage.setText("Ocorreu um erro!")


class WorkerThreadGet(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.window = parent

    def run(self):
        try:
            conn = ConnectDB(conexaoODBC)
            conn.conecta()
            sqlEmpresa = "select cnpj from empresa"
            conn.execute(sqlEmpresa)
            empresa = conn.fetchone()
            if not empresa:
                raise Exception
            formatA = empresa[0].replace('.', '')
            formatB = formatA.replace('/', '')
            cnpjFormatado = formatB.replace('-', '')
            apartir = self.parent().txtData.text()
            ate = self.parent().txtAte.text()
            loja = self.parent().txtLoja.text()
            # Chamada das funções getVendas e getPagamentos
            api = Api()
            vendas = api.getVendas(apartir, ate, loja, cnpjFormatado)
            pagamentos = api.getPagamentos(apartir, ate, loja, cnpjFormatado)
            if vendas or pagamentos:
                self.parent().txtData.setEnabled(True)
                self.parent().txtAte.setEnabled(True)
                self.parent().checkBox.setEnabled(True)
                self.parent().txtLoja.setEnabled(True)
                self.parent().buttonBaixarDados.setEnabled(True)
                self.parent().buttonEnviar.setEnabled(True)
                self.parent().buttonFechar.setEnabled(True)
                self.parent().janelaDeInformacoes.append("Arquivos baixados com sucesso!\n")
            if not vendas:
                self.parent().txtData.setEnabled(True)
                self.parent().txtAte.setEnabled(True)
                self.parent().checkBox.setEnabled(True)
                self.parent().txtLoja.setEnabled(True)
                self.parent().buttonBaixarDados.setEnabled(True)
                self.parent().buttonEnviar.setEnabled(True)
                self.parent().buttonFechar.setEnabled(True)
                self.parent().janelaDeInformacoes.append("Não existem relatórios de vendas para ser baixados\n")
            if not pagamentos:
                self.parent().txtData.setEnabled(True)
                self.parent().txtAte.setEnabled(True)
                self.parent().checkBox.setEnabled(True)
                self.parent().txtLoja.setEnabled(True)
                self.parent().buttonBaixarDados.setEnabled(True)
                self.parent().buttonEnviar.setEnabled(True)
                self.parent().buttonFechar.setEnabled(True)
                self.parent().janelaDeInformacoes.append("Não existem relatórios de pagamentos para ser baixados\n")
        except Exception as e:
            self.parent().txtData.setEnabled(True)
            self.parent().txtAte.setEnabled(True)
            self.parent().checkBox.setEnabled(True)
            self.parent().txtLoja.setEnabled(True)
            self.parent().buttonBaixarDados.setEnabled(True)
            self.parent().buttonEnviar.setEnabled(True)
            self.parent().buttonFechar.setEnabled(True)
            self.parent().janelaDeInformacoes.append("Ocorreu um erro\n")
            print(e)


class WorkerThread(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.window = parent

    def run(self):
        try:
            enviarJson(window.txtData.text(), window.txtLoja.text())
        except Exception as e:
            print(e)


def enviarJson(date, loja):
    window.janelaDeInformacoes.append("Por favor aguarde...\n")
    try:
        window.buttonEnviar.setDisabled(True)
        window.buttonFechar.setDisabled(True)
        window.buttonBaixarDados.setDisabled(True)
        window.txtData.setDisabled(True)
        window.txtLoja.setDisabled(True)
        window.txtAte.setDisabled(True)
        window.checkBox.setChecked(True)
        window.checkBox.setDisabled(True)
        dataFornecida = datetime.strptime(str(date), '%d/%m/%Y').strftime('%Y%m%d')
        newList = []
        conn = ConnectDB(conexaoODBC)
        conn.conecta()
        sqlEmpresa = f"select cnpj, conctoken from empresa where loja={loja}"
        conn.execute(sqlEmpresa)
        empresa = conn.fetchall_dict()
        formatA = empresa[0]['cnpj'].replace('.', '')
        formatB = formatA.replace('/', '')
        cnpjFormatado = formatB.replace('-', '')
        token = empresa[0]['conctoken']
        conn.conecta()
        sqlCartoes = f"""
                    SELECT c.id, c.formapgto, c.data data, c.valor, c.nsu, 
                    TRIM(LEADING '0' FROM split_str( nomepos,';', 2)) nsuhost,
                    TRIM(LEADING '0' FROM split_str( nomepos,';', 3)) autorizacao, o.detef, o.para,
                    if(TRIM(LEADING '0' FROM c.modalidade)=2, 0, 1)  modalidade
                    FROM cartoesoperadoras o inner join cartoes c on o.detef=c.autorizador
                    where c.data between {dataFornecida} and {dataFornecida}235959 and modalidade>0 and valor>0 and
                    loja={int(loja)} limit 3000
                    """
        conn.execute(sqlCartoes)
        cartoes = conn.fetchall_dict()
        if not cartoes:
            raise AttributeError
        cont = 0
        responseApi = None
        vendasEnviadas = 0
        for i in cartoes:
            vendasSistema = {
                "cnpj": "",  # string - tabela empresa - obrigatorio
                "id_erp": "",  # string - obrigatorio
                "data_venda": "",  # string (date: YYYY-MM-DD) - tabela cartoes - obrigatorio
                "valor_bruto": 0.1,  # float - tabela cartoes - obrigatorio
                "parcela": 1,  # int - obrigatorio
                "total_parcela": 1,  # int
                "nsu": "",  # string - tabela cartoes
                "codigo_autorizacao": "",  # string
                "cod_meio_captura": 2,  # int - fixo 2
                "cod_forma_pagamento": 1,  # int
                "cod_operadora": 1
            }
            vendasSistema['cnpj'] = str(cnpjFormatado)
            vendasSistema['id_erp'] = int(cartoes[cont]['id'])
            vendasSistema['data_venda'] = formatDate(cartoes[cont]['data'])
            vendasSistema['valor_bruto'] = float(cartoes[cont]['valor'])
            vendasSistema['nsu'] = int(cartoes[cont]['nsuhost'])
            vendasSistema['codigo_autorizacao'] = checkAuthorization(str(cartoes[cont]['autorizacao']))
            vendasSistema['cod_operadora'] = int(cartoes[cont]['para'])
            vendasSistema['cod_forma_pagamento'] = int(cartoes[cont]['modalidade'])
            # print(f'{cont} - {vendasSistema}')
            newList.append(vendasSistema)
            cont += 1
            if len(newList) % 100 == 0 or cont == len(cartoes):
                api = Api()
                responseApi = api.enviar_requisicao_post(newList)
                if responseApi['mensagem'] == 'Algumas vendas não foram processadas por conter duplicidade de informação!':
                    # print(newList[-1])
                    window.janelaDeInformacoes.append(f"{responseApi['mensagem']}: {responseApi['vendas_duplicadas']}\n")
                    newList = []  # Limpa a lista para começar um novo grupo de 100 itens
                elif responseApi['mensagem'] == 'Vendas criada com sucesso!':
                    # print(newList[-1])
                    window.janelaDeInformacoes.append("Enviando itens...\n")
                    vendasEnviadas += int(responseApi['quantidade_vendas_processadas'])
                    newList = []  # Limpa a lista para começar um novo grupo de 100 itens'
                sleep(60)

            if cont % 6000 == 0 or cont == len(cartoes) and cont == 6000:
                # Pausa o envio por 1 minuto após 60 envios (ou após o último envio se houver menos de 60)
                window.janelaDeInformacoes.append("Aguarde 1 minuto...\n")
                sleep(60)
        if responseApi['mensagem'] == 'Algumas vendas não foram processadas por conter duplicidade de informação!':
            window.janelaDeInformacoes.append("Não foi possivel fazer o envio de todas as vendas pois existem vendas duplicadas!\n")
        elif responseApi['mensagem'] == 'Vendas criada com sucesso!':
            window.janelaDeInformacoes.append(f"Vendas enviadas com sucesso! - quantidade de vendas processadas: {vendasEnviadas}\n")
        window.buttonBaixarDados.setEnabled(True)
        window.buttonEnviar.setEnabled(True)
        window.buttonFechar.setEnabled(True)
        window.txtData.setEnabled(True)
        window.txtLoja.setEnabled(True)
        window.txtAte.setEnabled(True)
        window.checkBox.setEnabled(True)

    except AttributeError:
        window.janelaDeInformacoes.append("Não existem vendas para envio.\n")
        window.buttonBaixarDados.setEnabled(True)
        window.buttonEnviar.setEnabled(True)
        window.buttonFechar.setEnabled(True)
        window.txtData.setEnabled(True)
        window.txtLoja.setEnabled(True)
        window.txtAte.setEnabled(True)
        window.checkBox.setEnabled(True)

    except Exception as e:
        print(e)
        window.janelaDeInformacoes.append("Ocorreu um erro!\n")
        window.buttonBaixarDados.setEnabled(True)
        window.buttonEnviar.setEnabled(True)
        window.buttonFechar.setEnabled(True)
        window.txtData.setEnabled(True)
        window.txtLoja.setEnabled(True)
        window.txtAte.setEnabled(True)
        window.checkBox.setEnabled(True)


app = QApplication(sys.argv)
window = WindowConciliador()
window.show()
# login = Login()
# login.show()
sys.exit(app.exec_())
