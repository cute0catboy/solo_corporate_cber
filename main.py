from playwright.sync_api import sync_playwright
import time
import config
import random
from pynput.keyboard import Controller, Key  # Добавили Key для работы с Backspace

LOGIN = config.login
PASSWORD = config.password

keyboard = Controller()

# Символы, которые могут использоваться для "ошибок"
TYPO_CHARS = "йцукенгшщзхъфывапролджэячсмитьбю"

def type_char(ch):
    keyboard.press(ch)
    time.sleep(random.uniform(0.02, 0.05))
    keyboard.release(ch)

def human_type(text):
    text_length = len(text)

    # 1. Задаем случайное количество ошибок от 2 до 10
    # target_errors_count = random.randint(2, 10)

    # 2. Собираем все индексы букв (пропуская пробелы и знаки препинания)
    # possible_indices = [i for i, ch in enumerate(text) if ch.isalpha()]

    # Защита: если текст слишком короткий и букв меньше 10, берем максимум доступных
    # amt_errors = min(target_errors_count, len(possible_indices))
    
    # Случайно выбираем уникальные позиции для будущих ошибок
    # typo_indices = set(random.sample(possible_indices, amt_errors))

    # 3. Основной цикл печати с контролем индекса (idx)
    for idx, ch in enumerate(text):
        # Базовая задержка между буквами (200-178 cpm)
        time.sleep(random.uniform(0.20, 0.33))

        # Если текущий индекс выбран для генерации ошибки
        # if idx in typo_indices:
        #     wrong = random.choice(TYPO_CHARS)

            # Не выбираем ту же самую букву, что должна быть
        #     while wrong == ch.lower():
        #         wrong = random.choice(TYPO_CHARS)

            # Печатаем ошибочную букву
        #     type_char(wrong)

            # Осознание ошибки (пауза перед удалением)
        #     time.sleep(random.uniform(0.25, 0.45))

            # Надежное нажатие Backspace с удержанием
        #     keyboard.press(Key.backspace)
        #     time.sleep(random.uniform(0.08, 0.12))  # Браузер гарантированно заметит
        #     keyboard.release(Key.backspace)

            # Пауза после удаления, чтобы тренажер успел стереть символ
        #     time.sleep(random.uniform(0.20, 0.35))

        # Печатаем правильный символ
        type_char(ch)

def speed_test(): # спид тест
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()
        page.goto("https://solocorporate.com")

        page.get_by_placeholder("E-mail").first.fill(LOGIN)
        page.get_by_placeholder("Пароль").first.fill(PASSWORD)
        page.get_by_role("button", name="Войти").click()
        page.wait_for_timeout(3000)

        page.locator('a[href="/study"]').click()
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

def learning_course(): # прохождение обучения
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()
        page.goto("https://sberbank.solocorporate.com/co/sberbankж прода")

        page.get_by_placeholder("E-mail").first.fill(LOGIN)
        page.get_by_placeholder("Пароль").first.fill(PASSWORD)
        page.get_by_role("button", name="Войти").click()
        page.wait_for_timeout(3000)

        page.locator('a[href="/study"]').click()
        page.wait_for_timeout(2000)
        page.locator('a[href="/study/rus"]').first.click()
        page.wait_for_timeout(2000)

        page.get_by_role("link", name="Продолжить обучение").click()

        while True:
            try:
                # Создаем локатор для кнопок выполнения/повторения задания
                exercise_btn = page.locator('button.btn-primary[data-ergotyping-params$="/1"], button.btn-primary[data-ergotyping-marker="repeat"]')
                
                # Создаем локатор для кнопки перехода на следующий урок
                next_lesson_btn = page.locator('a[role="lessonav-next"]')

                # Проверяем, видима ли кнопка задания на экране
                if exercise_btn.is_visible():
                    # 1. Кликаем по активной кнопке задания
                    exercise_btn.click()
                    page.wait_for_timeout(1000) # Даем тексту прогрузиться после клика

                    # Получаем text упражнения
                    text = page.locator(".text-prompt-value").evaluate("""
                        element => [...element.querySelectorAll("b")]
                            .map(b => b.textContent)
                            .join("")
                        """)
                    text = text.replace("\xa0", " ")

                    # Печатаем текст
                    human_type(text)
                    page.wait_for_timeout(1500) # Даем тренажеру обработать завершение ввода
                    
                    # 2. Ждем появления кнопки "Продолжить" и кликаем по ней
                    page.locator('button.action-continue').click()
                
                # Если кнопок заданий нет, но появилась кнопка "Далее" для смены урока
                elif next_lesson_btn.is_visible():
                    print("Все задания урока выполнены. Переходим к следующему уроку...")
                    next_lesson_btn.click()
                    page.wait_for_timeout(2000) # Даем странице нового урока загрузиться
                
                else:
                    # Если ни одной кнопки пока не видно, просто ждем
                    time.sleep(1)

                # Пауза перед следующим кругом
                time.sleep(1)
                
            except Exception as e:
                print(f"Ожидание появления кнопок или завершение: {e}")
                time.sleep(3) # Перезапуск цикла через 3 секунды, если что-то пошло не так

if __name__ == "__main__":
    learning_course()
