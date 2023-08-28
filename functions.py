import configparser
from PyQt5.QtCore import QDateTime
from datetime import datetime


def dataAtual():
    dateTime = QDateTime.currentDateTime()
    dateDisplay = dateTime.toString("dd/MM/yyyy")
    return dateDisplay


def formatDate(date):
    if date:
        return datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')


def checkAuthorization(authorization):
    if len(authorization) < 6:
        for i in range(10):
            if len(authorization) == 6:
                return authorization
            listAuth = list(authorization)
            listAuth.insert(0, "0")
            authorization = "".join(listAuth)
    return authorization


def verifyDecimalAndHexadecimal(value):
    try:
        try:
            if value.isdigit():
                return value
            else:
                raise ValueError
        except ValueError:
            integer_value = int(value, 16)
            if integer_value:     # Verifica se é um número hexadecimal válido
                return integer_value
            else:
                raise ValueError
    except ValueError:
        return 0


def conectar():
    """
        È necessario criar uma seção no config
        [conciliador]
        conectar='nome da conexão odbc para o servidor'
    """
    try:
        config = configparser.ConfigParser()
        config.read(f'conciliador.ini', encoding='utf-8')
        return config.get('conciliador', 'conectar')
    except ValueError:
        return False
