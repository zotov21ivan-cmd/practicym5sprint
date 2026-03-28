import random
import string

def generate_email():
    number = random.randint(100, 999)
    return f"Ivan_Zotov_41_{number}@yandex.ru"

def generate_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

email = generate_email() 
password = generate_password()
user_name= "Иван"
# для перемещению по сайту во время написания тестов 
#Ivan_Zotov_41_222@yandex.ru
# QWEas112As