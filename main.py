from playwright.sync_api import sync_playwright
import time
import config

LOGIN = config.login
PASSWORD = config.password

import random
from pynput.keyboard import Controller

keyboard = Controller()

# Символы, которые могут использоваться для "ошибок"
TYPO_CHARS = (
    "йцукенгшщзхъфывапролджэячсмитьбю"
)

def type_char(ch):
    keyboard.press(ch)
    time.sleep(random.uniform(0.02, 0.05))
    keyboard.release(ch)


def human_type(text):
    for ch in text:

        # Таблица задержек time.sleep(random.uniform(min, max)) для эмуляции печати:
        # --------------------------------------------------------------------------
        # Скорость (зв/мин) | Средняя (сек) | Пример кода
        # 150 cpm           | 0.400 cpm    | time.sleep(random.uniform(0.35, 0.45))
        # 175 cpm           | 0.343 cpm    | time.sleep(random.uniform(0.30, 0.39))
        # 200 cpm           | 0.300 cpm    | time.sleep(random.uniform(0.26, 0.34))
        # 225 cpm           | 0.267 cpm    | time.sleep(random.uniform(0.23, 0.30))
        # 250 cpm           | 0.240 cpm    | time.sleep(random.uniform(0.18, 0.23))
        # 275 cpm           | 0.218 cpm    | time.sleep(random.uniform(0.19, 0.25))
        # 300 cpm           | 0.200 cpm    | time.sleep(random.uniform(0.17, 0.23))
        time.sleep(random.uniform(0.26, 0.34))

        # Вероятность опечатки ~2%
#        if ch.isalpha() and random.random() < 0.02:
#
#            wrong = random.choice(TYPO_CHARS)
#
#            # Не выбираем ту же самую букву
#            while wrong == ch.lower():
#                wrong = random.choice(TYPO_CHARS)
#
#            # Печатаем ошибочную букву
#            type_char(wrong)
#
#            # Осознание ошибки :)
#            time.sleep(random.uniform(0.15, 0.35))
#
#            # Backspace
#            keyboard.press(Key.backspace)
#            time.sleep(random.uniform(0.02, 0.05))
#            keyboard.release(Key.backspace)
#
#            # Небольшая пауза
#            time.sleep(random.uniform(0.05, 0.15))

        # Печатаем правильный символ
        type_char(ch)

def speed_test(): #спид тест

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            slow_mo=300
        )

        page = browser.new_page()

        page.goto("https://sberbank.solocorporate.com/co/sberbank")

        # Логин
        page.get_by_placeholder("E-mail").first.fill(LOGIN)

        # Пароль
        page.get_by_placeholder("Пароль").first.fill(PASSWORD)

        # Вход
        page.get_by_role("button", name="Войти").click()

        # Ждём загрузку после логина
        page.wait_for_timeout(3000)

        # Переход в /study
        page.locator('a[href="/study"]').click()

        # (опционально) подождать загрузку страницы
        page.wait_for_timeout(2000)

        page.locator('a[href="/study/rus"]').first.click()

        page.wait_for_timeout(2000)

        page.locator('button[data-ergotyping-mode="test"]').click()

        text = page.locator(".text-prompt-value").evaluate("""
        element => [...element.querySelectorAll("b")]
            .map(b => b.textContent)
            .join("")
        """)
        text = text.replace("\xa0", " ")

        human_type(text)

        input("Нажмите Enter для выхода...")

        browser.close()

def learning_course(): #прохождение обучения

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            slow_mo=300
        )

        page = browser.new_page()

        page.goto("https://sberbank.solocorporate.com/co/sberbank")

        # Логин
        page.get_by_placeholder("E-mail").first.fill(LOGIN)

        # Пароль
        page.get_by_placeholder("Пароль").first.fill(PASSWORD)

        # Вход
        page.get_by_role("button", name="Войти").click()

        # Ждём загрузку после логина
        page.wait_for_timeout(3000)

        # Переход в /study ТУТ НАЧИНАЕТСЯ НАХОЖДЕНИЕ ТЕСТА ИЛИ УРОКА
        page.locator('a[href="/study"]').click()

        # (опционально) подождать загрузку страницы
        page.wait_for_timeout(2000)

        page.locator('a[href="/study/rus"]').first.click()

        page.wait_for_timeout(2000)

        page.get_by_role("link", name="Продолжить обучение").click()

        page.locator('button.btn-primary[data-ergotyping-mode="exercise"][data-ergotyping-params$="/1"]').click()

        text = page.locator(".text-prompt-value").evaluate("""
        element => [...element.querySelectorAll("b")]
            .map(b => b.textContent)
            .join("")
        """)
        text = text.replace("\xa0", " ")

        human_type(text)

        input("Нажмите Enter для выхода...")

        browser.close()

    #ПОЧЕМУ ТО ВОЗНИКЛА ОШИБКА ТИПО БЭКСПЕЙС НЕ НАЖИМАЕТСЯ МБ ПРОБЛЕМА В ПРОБЕЛЕ

if __name__ == "__main__":
    learning_course()