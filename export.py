import requests
import json
from datetime import datetime

API_KEY = 'A21VIEI4U441C4P7'  # Замените на свой API ключ
OUTPUT_FILE = 'exchange_rates.json'  # Имя файла для сохранения

# URL для запроса данных о курсе EUR/USD
url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=EUR&apikey={API_KEY}'

try:
    r = requests.get(url)
    data = r.json()

    # Проверка на наличие ошибок в ответе
    if 'Error Message' in data:
        print(f"Ошибка от API: {data['Error Message']}")
    elif 'Note' in data:
        print(f"Примечание от API: {data['Note']}")  # Например, о лимите запросов
    elif 'Time Series (Digital Currency Daily)' in data:
        time_series = data['Time Series (Digital Currency Daily)']

        # Создаем словарь с актуальными данными
        exchange_data = {
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rates": []
        }

        print("Курс EUR/USD (ежедневно):")
        print("--------------------------------------------------")

        for date_str, values in sorted(time_series.items(), reverse=True):  # Сортируем по дате
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%d-%m-%Y')  # Форматируем дату

            # Считываем данные и добавляем в список
            entry = {
                "date": formatted_date,
                "open": values.get('1. open', 'N/A'),
                "high": values.get('2. high', 'N/A'),
                "low": values.get('3. low', 'N/A'),
                "close": values.get('4. close', 'N/A')
            }
            exchange_data["rates"].append(entry)

            # Вывод в консоль
            print(f"Дата: {formatted_date}")
            print(f"  Открытие: {entry['open']} USD")
            print(f"  Максимум: {entry['high']} USD")
            print(f"  Минимум: {entry['low']} USD")
            print(f"  Закрытие: {entry['close']} USD")
            print("--------------------------------------------------")

        # Запись данных в JSON-файл
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
            json.dump(exchange_data, file, indent=4, ensure_ascii=False)

        print(f"✅ Данные сохранены в {OUTPUT_FILE}")

    else:
        print("Неожиданный формат данных от API.")

except requests.exceptions.RequestException as e:
    print(f"Ошибка подключения: {e}")
except Exception as e:
    print(f"Произошла ошибка: {e}")
