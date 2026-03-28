# место для будующих тестов
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from user_data import email,password
from locators import *

# Базовый URL сайта
from urls import stellarburgers_URL
BASE_URL = stellarburgers_URL

def test_registration_success(driver):
    wait = WebDriverWait(driver, 10)
    
    wait.until(EC.element_to_be_clickable((By.XPATH, loc_button_login_in_acaunt))).click()
    
    wait.until(EC.element_to_be_clickable((By.XPATH, loc_linc_reg))).click()
    
    name_input = wait.until(EC.visibility_of_element_located((By.XPATH, loc_name)))
    email_input = driver.find_element(By.XPATH, loc_email)
    password_input = driver.find_element(By.XPATH, loc_pass)
    
    name_input.send_keys("АвтоматическийТест")
    email_input.send_keys(email)
    password_input.send_keys(password)
    
    driver.find_element(By.XPATH, loc_button_reg).click()

    login_header = wait.until(
        EC.visibility_of_element_located((By.XPATH, loc_login_Vhod ))
    )
    assert login_header.is_displayed(), "После регистрации не произошел переход на страницу Входа"


def test_registration_invalid_password(driver): # неправельный пароль
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, loc_button_login_in_acaunt))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, loc_linc_reg))).click()
    
    name_input = wait.until(EC.visibility_of_element_located((By.XPATH, loc_name)))
    email_input = driver.find_element(By.XPATH, loc_email)
    password_input = driver.find_element(By.XPATH, loc_pass)
    
    name_input.send_keys("АвтоматическийТест")
    email_input.send_keys(email)
    password_input.send_keys("123")#непрвильный пароль
    
    driver.find_element(By.XPATH, loc_button_reg).click()
    
    error = wait.until(EC.presence_of_element_located((By.XPATH, loc_non_correct_pas)))
    assert "Некорректный пароль" in error.text


def test_login_via_button_on_main(driver): # Вход через кнопку на главной странице
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, loc_button_login_in_acaunt))).click()
    
    email_input = wait.until(EC.visibility_of_element_located((By.XPATH,loc_email)))
    password_input = driver.find_element(By.XPATH, loc_pass)
    
    email_input.send_keys(email)
    password_input.send_keys(password)
    
    driver.find_element(By.XPATH, loc_button_Voiti).click()
    
    wait.until(EC.element_to_be_clickable((By.XPATH, loc_button_oformit_zakaz)))
    assert "Оформить заказ" in driver.page_source


def test_login_via_cabinet_button(driver): # Вход через кнопку Личный кабинет
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.XPATH, loc_lichni_cabinet).click()
        
    email_input = wait.until(EC.visibility_of_element_located((By.XPATH,loc_email)))
    password_input = driver.find_element(By.XPATH, loc_pass)
    
    email_input.send_keys(email)
    password_input.send_keys(password)
    
    driver.find_element(By.XPATH, loc_button_Voiti).click()
        
    assert wait.until(EC.presence_of_element_located((By.XPATH, loc_button_oformit_zakaz)))


def test_login_from_registration_form(driver): # Вход через ссылку в форме регистрации
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.XPATH, loc_lichni_cabinet).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, loc_linc_reg))).click()
    
    # Клик по ссылке "Войти" внизу страницы регистрации
    driver.find_element(By.XPATH, loc_linc_voiti).click()
    
    email_input = wait.until(EC.visibility_of_element_located((By.XPATH,loc_email)))
    password_input = driver.find_element(By.XPATH, loc_pass)
    
    email_input.send_keys(email)
    password_input.send_keys(password)
    
    driver.find_element(By.XPATH, loc_button_Voiti).click()
    
    assert wait.until(EC.presence_of_element_located((By.XPATH, loc_button_oformit_zakaz)))


def test_login_from_password_recovery(driver): # Вход через форму восстановления пароля
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.XPATH, loc_lichni_cabinet).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, loc_vostanovit_paroll))).click()
    
    # На странице восстановления тоже есть ссылка "Войти"
    driver.find_element(By.XPATH, loc_button_Voiti).click()
    assert wait.until(EC.presence_of_element_located((By.XPATH, loc_vhod)))


def test_navigation_cabinet(driver): #  Переход в Личный кабинет (для авторизованного)
    wait = WebDriverWait(driver, 10)
    # Тут подразумевается, что мы сначала залогинились 
    driver.find_element(By.XPATH, loc_lichni_cabinet).click()
    assert wait.until(EC.presence_of_element_located((By.XPATH, loc_vhod))) # Если не залогинены — кинет на вход


def test_navigation_to_constructor(driver): # Переход из личного кабинета в Конструктор по клику на логотип
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.XPATH, loc_lichni_cabinet).click()
    
    # Клик на логотип
    driver.find_element(By.XPATH, loc_constructor).click()
    assert wait.until(EC.presence_of_element_located((By.XPATH, loc_test_soberi_burger)))


def test_logout(driver): #  Выход из аккаунта 
    wait = WebDriverWait(driver, 10)
    # Логинимся
    driver.find_element(By.XPATH, loc_button_login_in_acaunt).click()
    
    email_input = wait.until(EC.visibility_of_element_located((By.XPATH,loc_email)))
    password_input = driver.find_element(By.XPATH, loc_pass)
    
    email_input.send_keys(email)
    password_input.send_keys(password)
    
    driver.find_element(By.XPATH, loc_button_Voiti).click()
        
    wait.until(EC.element_to_be_clickable((By.XPATH, loc_lichni_cabinet))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, loc_out))).click()
    
    assert wait.until(EC.visibility_of_element_located((By.XPATH, loc_vhod)))


def test_navigation_to_sauces(driver): # переход в соусы
    wait = WebDriverWait(driver, 10)
    
    wait.until(EC.element_to_be_clickable((By.XPATH, loc_button_sous))).click()
    
    assert wait.until(EC.visibility_of_element_located((By.XPATH, loc_text_sous)))

def test_navigation_to_fillings(driver): # переход в начинки
    wait = WebDriverWait(driver, 10)
    
    wait.until(EC.element_to_be_clickable((By.XPATH, loc_buton_nachinki))).click()
    
    assert wait.until(EC.visibility_of_element_located((By.XPATH, loc_text_nachinki)))

def test_navigation_to_buns(driver):# переход в булки
    wait = WebDriverWait(driver, 10)
    # Сначала кликнем на другой раздел, чтобы "Булки" перестали быть активными
    wait.until(EC.element_to_be_clickable((By.XPATH, loc_button_sous))).click()
    
    wait.until(EC.element_to_be_clickable((By.XPATH, loc_text_bulki))).click()
    
    assert wait.until(EC.visibility_of_element_located((By.XPATH, loc_text_bulki)))
    
    
