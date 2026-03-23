# место для будующих тестов
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Базовый URL сайта
BASE_URL = "https://stellarburgers.education-services.ru/"

def open_site():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    driver.get(BASE_URL)
    return driver, wait

def close(driver):
    driver.quit()

def test_registration_success():
    driver, wait = open_site()
    try:
        # Открываем окно регистрации
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Зарегистрироваться"))).click()
        # Заполняем поля
        name_input = wait.until(EC.presence_of_element_located((By.NAME, "name")))
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
        name_input.send_keys("АвтоматическийТест")
        email_input.send_keys("Ivan_Zotov_41_132@yandex.ru")
        password_input.send_keys("QWf12laewrю.")
        # Отправляем форму
        driver.find_element(By.XPATH, "//button[contains(text(), 'Зарегистрироваться')]").click()
        # Проверка успешной регистрации (например, переход в ЛК)
        assert "Личный кабинет" in driver.page_source
    finally:
        close(driver)

def test_registration_invalid_password():# проверка регистрации при невалидном пароле
    driver, wait = open_site()
    try:
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Зарегистрироваться"))).click()
        driver.find_element(By.NAME, "name").send_keys("АвтоматическийТест")
        driver.find_element(By.NAME, "email").send_keys("Ivan_Zotov_41_132@yandex.ru")
        driver.find_element(By.NAME, "password").send_keys("QWf.")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Зарегистрироваться')]").click()
        error_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "error-message")))
        assert "недостаточно символов" in error_element.text.lower()
    finally:
        close(driver)

def test_login_via_button_on_main():# проверка кнопки войти
    driver, wait = open_site()
    try:
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Войти"))).click()
        email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password_input = driver.find_element(By.NAME, "password")
        email_input.send_keys("Ivan_Zotov_41_132@yandex.ru")
        password_input.send_keys("QWf12laewrю.")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()
        assert "Личный кабинет" in driver.page_source
    finally:
        close(driver)

def test_login_via_cabinet_button(): # проверка входе через кнопку лечный кабинет
    driver, wait = open_site()
    try:
        driver.find_element(By.LINK_TEXT, "Личный кабинет").click()
        email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password_input = driver.find_element(By.NAME, "password")
        email_input.send_keys("Ivan_Zotov_41_132@yandex.ru")
        password_input.send_keys("QWf12laewrю.")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()
        assert "Личный кабинет" in driver.page_source
    finally:
        close(driver)

def test_login_from_registration_form(): # проверка входа через кнопку регистрации
    driver, wait = open_site()
    try:
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Зарегистрироваться"))).click()
        name_input = wait.until(EC.presence_of_element_located((By.NAME, "name")))
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
        name_input.send_keys("АвтоматическийТест")
        email_input.send_keys("Ivan_Zotov_41_132@yandex.ru")
        password_input.send_keys("QWf12laewrю.")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Зарегистрироваться')]").click()
        # Переход к окну входа
        driver.find_element(By.LINK_TEXT, "Войти").click()
        email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password_input = driver.find_element(By.NAME, "password")
        email_input.send_keys("Ivan_Zotov_41_132@yandex.ru")
        password_input.send_keys("QWf12laewrю.")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()
        assert "Личный кабинет" in driver.page_source
    finally:
        close(driver)

def test_login_from_password_recovery(): # проверка востановления пароля
    driver, wait = open_site()
    try:
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Восстановить пароль"))).click()
        email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_input.send_keys("Ivan_Zotov_41_132@yandex.ru")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Восстановить')]").click()
        msg = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "success-message")))
        assert "Инструкция отправлена" in msg.text
    finally:
        close(driver)

def test_navigation_cabinet(): # проверка навигации в личном кабинете
    driver, wait = open_site()
    try:
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Личный кабинет"))).click()
        assert "Личный кабинет" in driver.page_source
    finally:
        close(driver)

def test_navigation_to_constructor(): # тестн навигаци при создании бургера
    driver, wait = open_site()
    try:
        driver.get(BASE_URL)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "logo"))).click()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Конструктор"))).click()
        assert "Создайте свой бургер" in driver.page_source
    finally:
        close(driver)

def test_logout(): # проверка разлогинивания 
    driver, wait = open_site()
    try:
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Войти"))).click()
        email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password_input = driver.find_element(By.NAME, "password")
        email_input.send_keys("Ivan_Zotov_41_132@yandex.ru")
        password_input.send_keys("QWf12laewrю.")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()
        # пользователь авторизовался, теперь будем выходить 
        driver.get(BASE_URL + "/lk")
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Выйти"))).click()
        assert "Войти" in driver.page_source
    finally:
        close(driver)

def test_perehod_na_razdely_blyud(): # тест перехода в раздел с блюдами
    driver, wait = open_site()
    try:
        driver.get(BASE_URL + "/constructor")
        for tab_text in ["Булки", "Соусы", "Начинки"]:
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, tab_text))).click()
            section_title = wait.until(EC.presence_of_element_located((By.XPATH, f"//h2[contains(text(), '{tab_text}')]")))
            assert section_title is not None
    finally:
        close(driver)

# Запуск всех тестов по порядку
if __name__ == "__main__":
    try:
        test_registration_success()
        print("Тест регистрации успешной пройден.")
        test_registration_invalid_password()
        print("Тест некорректного пароля пройден.")
        test_login_via_button_on_main()
        print("Тест входа через кнопку на главной пройден.")
        test_login_via_cabinet_button()
        print("Тест входа через кнопку 'Личный кабинет' пройден.")
        test_login_from_registration_form()
        print("Тест входа из формы регистрации пройден.")
        test_login_from_password_recovery()
        print("Тест восстановления пароля пройден.")
        test_navigation_cabinet()
        print("Тест навигации в личный кабинет пройден.")
        test_navigation_to_constructor()
        print("Тест навигации к конструктору пройден.")
        test_logout()
        print("Тест выхода из аккаунта пройден.")
        test_perehod_na_razdely_blyud()
        print("Тест перехода по разделам блюда пройден.")
        print("Все тесты успешно выполнены!")
    except AssertionError as e:
        print("Один из тестов не прошел:", e)