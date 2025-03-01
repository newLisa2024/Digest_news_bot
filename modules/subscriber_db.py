# modules/subscriber_db.py

import logging
import gspread
import config

# Пытаемся установить соединение с Google Sheets через сервисный аккаунт
try:
    gc = gspread.service_account(filename=config.GOOGLE_SHEETS_CREDENTIALS_FILE)
    # Открываем таблицу по названию, указанному в config
    sheet = gc.open(config.SPREADSHEET_NAME).sheet1
    logging.info("Подключение к Google Sheets успешно установлено.")
except Exception as e:
    logging.error("Ошибка подключения к Google Sheets: %s", e)
    sheet = None

def add_subscriber(user_id, username):
    """
    Добавляет подписчика в Google Таблицу.
    """
    if sheet is None:
        logging.error("Google Sheets не подключены. Невозможно добавить подписчика.")
        return

    try:
        # Добавляем новую строку с информацией о подписчике.
        # Здесь можно добавить дополнительные поля, например дату подписки.
        sheet.append_row([user_id, username])
        logging.info("Подписчик %s успешно добавлен.", user_id)
    except Exception as e:
        logging.error("Ошибка добавления подписчика %s: %s", user_id, e)

def remove_subscriber(user_id):
    """
    Удаляет подписчика из Google Таблицы по user_id.
    """
    if sheet is None:
        logging.error("Google Sheets не подключены. Невозможно удалить подписчика.")
        return

    try:
        # Ищем ячейку с нужным user_id.
        cell = sheet.find(str(user_id))
        if cell:
            # Удаляем всю строку, где найден user_id.
            sheet.delete_rows(cell.row)
            logging.info("Подписчик %s успешно удалён.", user_id)
        else:
            logging.info("Подписчик %s не найден в таблице.", user_id)
    except Exception as e:
        logging.error("Ошибка удаления подписчика %s: %s", user_id, e)

def list_subscribers():
    """
    Возвращает список всех подписчиков в виде списка словарей.
    """
    if sheet is None:
        logging.error("Google Sheets не подключены. Невозможно получить список подписчиков.")
        return []

    try:
        # Получаем все записи из таблицы.
        records = sheet.get_all_records()
        return records
    except Exception as e:
        logging.error("Ошибка получения списка подписчиков: %s", e)
        return []
