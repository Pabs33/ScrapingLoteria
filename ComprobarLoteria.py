from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import time
import datetime

driver = webdriver.Edge('RutaSelecnium')

def sacarNumeros(numeroSorteo):

    formNumero = driver.find_element(by=By.ID, value='qa_subhome-comprobador-numero-LNAC')
    botonComprobar =  driver.find_element(by=By.ID, value='qa_subhome-comprobador-botonComprobar-LNAC')
    formNumero.send_keys(numeroSorteo)
    botonComprobar.click()

    time.sleep(1)
    try:
        premio = driver.find_element(by=By.ID, value='qa_subhome-resultadosComprobacion-premioConseguido-LNAC')
    except:
        premio = driver.find_element(by=By.CLASS_NAME, value='c-mensaje-no-ganador__literal-lo-sentimos')
        if(premio.text == 'ESTE NÚMERO NO HA SIDO PREMIADO.'):
            return('0,00€')
    return(premio.text)

def sacarFecha():
    opciones = driver.find_elements(by=By.CLASS_NAME, value='c-comprobador-subhome-lnac__fecha-option')
    return opciones[0].text

def sacarValorDecimo():
    valorDecimo = driver.find_element(by=By.ID, value='qa_subhome-comprobador-euros-LNAC')
    return valorDecimo.get_attribute('value')

#funcion para saber si se esta ejecutando un domingo
def saberFecha():
    date = datetime.datetime.now()
    dayOfTheWeek = date.strftime("%A")
    print(dayOfTheWeek)
    if(dayOfTheWeek == "Sunday"):
        return True
    return False


def main():

    if(saberFecha() == False):
        print('Hoy no es domingo con lo que no hay loteria para mostrar')
        return 1

    driver.get('https://www.loteriasyapuestas.es/es/loteria-nacional')

    time.sleep(3)

    #Aceptar las cookies
    botonCookies = driver.find_element(by=By.ID, value='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
    botonCookies.click()

    fechaSorteo = sacarFecha()

    try:
        premio64 = sacarNumeros(32464)
        valor64 = sacarValorDecimo()
    except:
        premio64 = 'No se ha podido obtener el premio, por favor consultelo mas tarde o consultelo desde la web oficial'
    driver.refresh()
    time.sleep(2)
    try:
        premio28 = sacarNumeros(46928)
        valor28 = sacarValorDecimo()
    except:
        premio28 = 'No se ha podido obtener el premio, por favor consultelo mas tarde o consultelo desde la web oficial'

    print('Premio del 64: ' + premio64)
    print('Premio del 28: ' + premio28)

    driver.quit()

if __name__ == '__main__':
    main()