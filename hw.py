import requests, datetime, schedule, lxml, sys
from bs4 import BeautifulSoup
url = input('Вставь URL:')

def connect():
    try:
        requests.get('https://google.com', timeout=5)
        print("Интернет соединение установленно")
        return True
    except:
        print('Проверьте интернет соединение!')
        return False
connection = connect()
if connection:
    def main():
        if url != '' and 'http' in url or 'https' in url:
            time = int(input('Интервал:'))
            print('Выполняется парсинг ожидайте...')
            schedule.every(time).seconds.do(perform_request, url)
            while True:
                schedule.run_pending()
        else:
            print('Не правильный URL ад адрес!')
            sys.exit(0)
    def  perform_request(url):
        try:
            responce = requests.get(url)
            soup = BeautifulSoup(responce.text, 'lxml')
            responce.raise_for_status()
            title = soup.find('title')
            files = f"{datetime.datetime.now().strftime('%H-%M-%S')}_{title.text}.txt"
            print(f'Парсинг успешно завершен!\nОткройте папку parcing и найдите файл: {files}')
            with open(f'parcing/{files}', 'a', encoding='utf-8') as file:
                file.write(responce.text)
            sys.exit(0)
        except requests.exceptions.RequestException:
            print('Не правильный URL аддрес!')
            with open(f'parcing/error.txt', 'a', encoding='utf-8') as file:
                file.write(f'Не правильный URL ад адрес! -- {url}\n')
            sys.exit(0)
    main()
    perform_request(url)