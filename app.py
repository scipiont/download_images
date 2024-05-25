# import asyncio
# import aiohttp
# import os
# import sys
# import time
# from datetime import datetime
# from urllib.parse import urlparse

# async def download_image(session, url):
#     filename = os.path.basename(urlparse(url).path)
#     async with session.get(url) as response:
#         if response.status == 200:
#             with open(filename, 'wb') as f:
#                 while True:
#                     chunk = await response.content.read(1024)
#                     if not chunk:
#                         break
#                     f.write(chunk)
#             download_time = datetime.now().strftime("%H:%M")  # Реальное время скачивания
#             print(f"Скачивание завершено: {filename} в {download_time}.")

# async def main(urls):
#     async with aiohttp.ClientSession() as session:
#         tasks = [download_image(session, url) for url in urls]
#         await asyncio.gather(*tasks)

# if __name__ == "__main__":
#     start_time = time.time()
#     urls = sys.argv[1:]  # Список URL-адресов передается через аргументы командной строки
#     asyncio.run(main(urls))
#     total_time = time.time() - start_time
#     print(f"Общее время выполнения: {total_time:.2f} секунд.")
# # указать url картинки через пробел
# # пример скачивания: python app.py https://angelamethist.com/image/ezgif.com-crop.gif https://dva.pw/images/designer_photo2.png

# import argparse
# import asyncio
# import aiohttp
# from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
# import requests
# from urllib.parse import urlparse
# import os

# # Функция для скачивания изображения (используется в многопоточности и многопроцессорности)
# def download_image(url):
#     filename = os.path.basename(urlparse(url).path)
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open(filename, 'wb') as f:
#             f.write(response.content)
#         print(f"{filename} скачан.")

# # Многопоточная загрузка
# def download_images_multithreaded(urls):
#     with ThreadPoolExecutor(max_workers=5) as executor:
#         executor.map(download_image, urls)

# # Многопроцессорная загрузка
# def download_images_multiprocessed(urls):
#     with ProcessPoolExecutor() as executor:
#         executor.map(download_image, urls)

# # Асинхронная загрузка
# async def async_download_image(session, url):
#     filename = os.path.basename(urlparse(url).path)
#     async with session.get(url) as response:
#         if response.status == 200:
#             with open(filename, 'wb') as f:
#                 while True:
#                     chunk = await response.content.read(1024)
#                     if not chunk:
#                         break
#                     f.write(chunk)
#             print(f"{filename} скачан.")

# async def download_images_async(urls):
#     async with aiohttp.ClientSession() as session:
#         tasks = [async_download_image(session, url) for url in urls]
#         await asyncio.gather(*tasks)

# # Основная функция
# def main(mode):
#     with open('urls.txt') as f:
#         urls = [line.strip() for line in f]

#     if mode == 'multithread':
#         download_images_multithreaded(urls)
#     elif mode == 'multiprocess':
#         download_images_multiprocessed(urls)
#     elif mode == 'async':
#         asyncio.run(download_images_async(urls))
#     else:
#         print("Неизвестный режим. Выберите 'multithread', 'multiprocess' или 'async'.")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Скачивание изображений разными методами.")
#     parser.add_argument('mode', type=str, help="Метод скачивания: multithread, multiprocess, async")
#     args = parser.parse_args()

#     main(args.mode)

import argparse
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import requests
from urllib.parse import urlparse
import os
import time
from datetime import datetime

# Создаем папку для скачанных изображений, если она не существует
download_folder = 'downloaded_images'
os.makedirs(download_folder, exist_ok=True)

# Функция для скачивания изображения (используется в многопоточности и многопроцессорности)
def download_image(url):
    start_time = time.time()
    filename = os.path.join(download_folder, os.path.basename(urlparse(url).path))
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        elapsed_time = time.time() - start_time
        print(f"{filename} скачан за {elapsed_time:.2f} сек. в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

# Многопоточная загрузка
def download_images_multithreaded(urls):
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_image, urls)

# Многопроцессорная загрузка
def download_images_multiprocessed(urls):
    with ProcessPoolExecutor() as executor:
        executor.map(download_image, urls)

# Асинхронная функция для скачивания изображения
async def async_download_image(session, url):
    start_time = time.time()
    filename = os.path.join(download_folder, os.path.basename(urlparse(url).path))
    async with session.get(url) as response:
        if response.status == 200:
            with open(filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            elapsed_time = time.time() - start_time
            print(f"{filename} скачан за {elapsed_time:.2f} сек. в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

# Асинхронная загрузка
async def download_images_async(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [async_download_image(session, url) for url in urls]
        await asyncio.gather(*tasks)

# Основная функция
def main(mode):
    with open('urls.txt') as f:
        urls = [line.strip() for line in f]

    if mode == 'multithread':
        download_images_multithreaded(urls)
    elif mode == 'multiprocess':
        download_images_multiprocessed(urls)
    elif mode == 'async':
        asyncio.run(download_images_async(urls))
    else:
        print("Неизвестный режим. Выберите 'multithread', 'multiprocess' или 'async'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скачивание изображений разными методами с выводом времени и сохранением в отдельную папку.")
    parser.add_argument('mode', type=str, help="Метод скачивания: multithread, multiprocess, async")
    args = parser.parse_args()

    main(args.mode)