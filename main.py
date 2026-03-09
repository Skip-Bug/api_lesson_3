from dotenv import load_dotenv
import argparse
import requests
import os


def shorten_link(token, link):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    body = {
        "url": link
    }

    response = requests.post(
        'https://clc.li/api/url/add',
        headers=headers,
        json=body
        )
    response.raise_for_status()
    return response.json()['shorturl']
    
    

def create_parser():
    parser = argparse.ArgumentParser(
        description='Делаем сокращение ссылок'
    )
    parser.add_argument(
        'link',
        nargs='?',
        help='Ссылка для обработки'
    )
    return parser

def get_count_clicks(token, link):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(
        url=f'https://clc.li/api/urls?short={link}',
        headers=headers
        )

    response.raise_for_status()
    return response.json()


def is_shorten_link(link):
    return 'clc.li' in link


def main():
    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()
    token = os.getenv('CLC_LI_TOKEN')
    link = args.link or input("Введите ссылку: ").strip()

    if not token:
        print("ОШИБКА: Не найден токен в переменных окружения!")
        return


    if is_shorten_link(link):
        try:
            link_stats = get_count_clicks(
                token,
                link
                )

            if 'data' in link_stats:
                clicks_count = link_stats['data'].get('clicks', 0)
                print('Количество кликов ', clicks_count)
            elif 'error' in link_stats:
                error = link_stats.get('message', 'Неизвестная ошибка')
                print(f"API вернул ошибку: {error}")
            else:
                print("Не удалось получить статистику")

        except requests.exceptions.HTTPError:
            print("Ошибка соединения с API!")
        return

    try:
        full_short_link = shorten_link(token, link)
        print('Короткая ссылка ', full_short_link)
    except requests.exceptions.HTTPError:
        print("ОШИБКА: Проблема при обращении к API!")


if __name__ == "__main__":
    main()
