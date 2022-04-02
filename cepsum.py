from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from credentials import userName,password # strings containng credentials
import time
import datetime
timeout=10

def checkTime(x):
    """
    return true if element contain the desired hours. 
    For exemple, if you are free to play at 17h,
        if x.text.find('17:') != -1:
            return True
    """
    # if x.text.find('17:') != -1:
    #     return True
    if x.text.find('18:') != -1:
        return True
    if x.text.find('19:') != -1:
        return True
    if x.text.find('20:') != -1:
        return True
    return False

def findSlots(driver):
    """
    Gets all tha available timeslots, then tries to reserve for all of them until a reservation is succesfully made
    """
    timeSlots = WebDriverWait(driver, timeout).until(lambda d: d.find_elements(by=By.CSS_SELECTOR,value="a.bouton-plat.neutre"))

    timeSlotsIterator = filter(checkTime,timeSlots)
    timeSlots = list(timeSlotsIterator)
    for timeSlot in timeSlots:
        try:
            timeSlot.click()

            """
            You need to press confirm twice to make a reservation. This part (the complete button) is not stable. You can comment it out so the webdriver does not try to confirm the reservation. At this point, the driver already "locked in" a time slot, and you have 5 minutes to complete the reservation yourself.
            """
            completeButton = WebDriverWait(driver, timeout).until(lambda d: d.find_element(by=By.CSS_SELECTOR,value="[id$=btnConfirmer]"))
            completeButton.click()
            driver.wait = WebDriverWait(driver, timeout)
            completeButton = WebDriverWait(driver, timeout).until(lambda d: d.find_element(by=By.CSS_SELECTOR,value="[id$=btnConfirmer]"))
            completeButton.click()
        except:
            backButton = WebDriverWait(driver, timeout).until(lambda d: d.find_element(by=By.CSS_SELECTOR,value="[id$=btnPrecedentEtape3]"))
            backButton.click()
            findSlots(driver)
        break

def reserveCepsum():
    """
    Main function: launches the browser, logs in, then reserves a slot
    """
    driver = webdriver.Chrome()
    driver.get("https://interactif.cepsum.umontreal.ca/CapNet/login.coba")
    userName_field = driver.find_element(by=By.CSS_SELECTOR,value="[id$=txtCodeUsager]")
    userName_field.clear()
    userName_field.send_keys(userName)

    password_field = driver.find_element(by=By.CSS_SELECTOR,value="[id$=txtMotDePasse]")
    password_field.clear()
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    reserveButton = WebDriverWait(driver, timeout).until(lambda d: d.find_element(by=By.XPATH,value="//a[text()='Réservations - Sports de raquette & salles']"))

    reserveButton.click()

    addReservationButton = WebDriverWait(driver, timeout).until(lambda d: d.find_element(by=By.XPATH,value="//span[text()='Ajouter une réservation']"))
    addReservationButton.click()

    tennis_string = 'TENNIS'
    badminton_string = 'BAD'
    tennisButton =WebDriverWait(driver, timeout).until(lambda d: d.find_element(by=By.CSS_SELECTOR,value=f"[id$={tennis_string}]"))
    tennisButton.click()
    nextDayButton = WebDriverWait(driver, timeout).until(lambda d: d.find_element(by=By.CSS_SELECTOR,value="[id$=btnDateSuiv]"))
    nextDayButton.click()
    nextDayButton = WebDriverWait(driver, timeout).until(lambda d: d.find_element(by=By.CSS_SELECTOR,value="[id$=btnDateSuiv]"))
    nextDayButton.click()
    findSlots(driver)

    


# sleep all day and wake up when reservations open
while True:
    numHoursToSleep = ((18 - datetime.datetime.now().hour) + 24 ) % 24
    numMinutesToSleep = ((59 - datetime.datetime.now().minute) + 60 ) % 60
    numSecondsToSleep = ((58 - datetime.datetime.now().second) + 60 ) % 60
    print("launched at: " + str(datetime.datetime.now()))
    print("Sleeping for " + str(numHoursToSleep) + " hours " + str(numMinutesToSleep) + " minutes " + str(numSecondsToSleep) + " seconds")

    time.sleep(numHoursToSleep*3600 + numMinutesToSleep*60 + numSecondsToSleep)
    reserveCepsum()
