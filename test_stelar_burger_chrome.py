from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from user_data import email, password , user_name
from locators import *
from urls import stellarburgers_URL

BASE_URL = stellarburgers_URL

class TestRegistration:
    """Тесты регистрации нового пользователя"""
    # новый пользователь валидные данные
    def test_registration_success(self, driver):
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, loc_button_login_in_acaunt))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, loc_linc_reg))).click()
        
        name_input = wait.until(EC.visibility_of_element_located((By.XPATH, loc_name)))
        driver.find_element(By.XPATH, loc_email).send_keys(email)
        driver.find_element(By.XPATH, loc_pass).send_keys(password)
        
        name_input.send_keys(user_name)
        driver.find_element(By.XPATH, loc_button_reg).click()

        login_header = wait.until(EC.visibility_of_element_located((By.XPATH, loc_login_Vhod)))
        assert login_header.is_displayed()
    #регистрация нового пользователя не валидные данные( пароль)
    def test_registration_invalid_password(self, driver):
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, loc_button_login_in_acaunt))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, loc_linc_reg))).click()
        
        wait.until(EC.visibility_of_element_located((By.XPATH, loc_pass))).send_keys("123")
        driver.find_element(By.XPATH, loc_button_reg).click()
        
        error = wait.until(EC.presence_of_element_located((By.XPATH, loc_non_correct_pas)))
        assert "Некорректный пароль" in error.text


class TestLogin:
    """Тесты авторизации уже существующего пользователя"""
    # через кнопку войти в акаунт
    def test_login_via_button_on_main(self, driver):
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, loc_button_login_in_acaunt))).click()
        
        wait.until(EC.visibility_of_element_located((By.XPATH, loc_email))).send_keys(email)
        driver.find_element(By.XPATH, loc_pass).send_keys(password)
        driver.find_element(By.XPATH, loc_button_Voiti).click()
        
        assert wait.until(EC.element_to_be_clickable((By.XPATH, loc_button_oformit_zakaz)))
    # через кнопку личного кабинета
    def test_login_via_cabinet_button(self, driver):
        wait = WebDriverWait(driver, 10)
        driver.find_element(By.XPATH, loc_lichni_cabinet).click()
        
        wait.until(EC.visibility_of_element_located((By.XPATH, loc_email))).send_keys(email)
        driver.find_element(By.XPATH, loc_pass).send_keys(password)
        driver.find_element(By.XPATH, loc_button_Voiti).click()
        
        assert wait.until(EC.presence_of_element_located((By.XPATH, loc_button_oformit_zakaz)))
    # кнопка на окне регистрации
    def test_login_from_registration_form(self, driver):
        wait = WebDriverWait(driver, 10)
        driver.find_element(By.XPATH, loc_lichni_cabinet).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, loc_linc_reg))).click()
        driver.find_element(By.XPATH, loc_linc_voiti).click()
        
        wait.until(EC.visibility_of_element_located((By.XPATH, loc_email))).send_keys(email)
        driver.find_element(By.XPATH, loc_pass).send_keys(password)
        driver.find_element(By.XPATH, loc_button_Voiti).click()
        
        assert wait.until(EC.presence_of_element_located((By.XPATH, loc_button_oformit_zakaz)))
    # кнопку на окне востановления пароля
    def test_login_from_password_recovery(self, driver):
        wait = WebDriverWait(driver, 10)
        driver.find_element(By.XPATH, loc_lichni_cabinet).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, loc_vostanovit_paroll))).click()
        driver.find_element(By.XPATH, loc_button_Voiti).click()
        
        assert wait.until(EC.presence_of_element_located((By.XPATH, loc_vhod)))


class TestUserProfile:
    """Тесты функционала личного кабинета"""
    # проверка работы личного кабинет ( пользователь не авторизован)
    def test_navigation_cabinet(self, driver):
        wait = WebDriverWait(driver, 10)
        driver.find_element(By.XPATH, loc_lichni_cabinet).click()
        assert wait.until(EC.presence_of_element_located((By.XPATH, loc_vhod)))

    def test_navigation_to_constructor(self, driver):
        wait = WebDriverWait(driver, 10)
        driver.find_element(By.XPATH, loc_lichni_cabinet).click()
        driver.find_element(By.XPATH, loc_constructor).click()
        assert wait.until(EC.presence_of_element_located((By.XPATH, loc_test_soberi_burger)))
    # тест выхода с аккаунта
    def test_logout(self, driver):
        wait = WebDriverWait(driver, 10)
        # Предусловие: Логин
        driver.find_element(By.XPATH, loc_button_login_in_acaunt).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, loc_email))).send_keys(email)
        driver.find_element(By.XPATH, loc_pass).send_keys(password)
        driver.find_element(By.XPATH, loc_button_Voiti).click()
        
        # Выход
        wait.until(EC.element_to_be_clickable((By.XPATH, loc_lichni_cabinet))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, loc_out))).click()
        assert wait.until(EC.visibility_of_element_located((By.XPATH, loc_vhod)))


class TestConstructor:
    """Тесты разделов конструктора"""
    # переход в соусы
    def test_navigation_to_sauces(self, driver):
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, loc_button_sous))).click()
        assert wait.until(EC.visibility_of_element_located((By.XPATH, loc_text_sous)))
    # переход в начинки
    def test_navigation_to_fillings(self, driver):
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, loc_buton_nachinki))).click()
        assert wait.until(EC.visibility_of_element_located((By.XPATH, loc_text_nachinki)))
    # переход в булки
    def test_navigation_to_buns(self, driver):
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, loc_button_sous))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, loc_text_bulki))).click()
        assert wait.until(EC.visibility_of_element_located((By.XPATH, loc_text_bulki)))