import os
from dotenv import load_dotenv
load_dotenv()

login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")
lang = "rus" #eng

#curl -o python-installer.exe https://python.org
#python-installer.exe /quiet PrependPath=1
