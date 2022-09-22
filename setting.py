import os
from dotenv import load_dotenv, find_dotenv

if not (p := find_dotenv()):
    print('Не найден файл .env')
else:
    load_dotenv(dotenv_path=p)

VK_KEY = os.getenv('VK_KEY')
ID_VK_GROUP = os.getenv('ID_VK_GROUP')

if not VK_KEY or not ID_VK_GROUP:
    exit('В переменных окружения не найдены данные ключа VK или ID сообщества!')

VER_VK_API = '5.131'
