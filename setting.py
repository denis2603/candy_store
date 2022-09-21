import os
from dotenv import load_dotenv, find_dotenv

if not (p := find_dotenv()):
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv(dotenv_path=p)

VK_KEY = os.getenv('VK_KEY')
ID_VK_GROUP = os.getenv('ID_VK_GROUP')

VER_VK_API = '5.131'
