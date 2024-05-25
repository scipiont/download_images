import asyncio
import aiohttp
import os
import sys
import time
from datetime import datetime
from urllib.parse import urlparse

async def download_image(session, url):
    filename = os.path.basename(urlparse(url).path)
    async with session.get(url) as response:
        if response.status == 200:
            with open(filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            download_time = datetime.now().strftime("%H:%M")  # Реальное время скачивания
            print(f"Скачивание завершено: {filename} в {download_time}.")

async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [download_image(session, url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    start_time = time.time()
    urls = sys.argv[1:]  # Список URL-адресов передается через аргументы командной строки
    asyncio.run(main(urls))
    total_time = time.time() - start_time
    print(f"Общее время выполнения: {total_time:.2f} секунд.")
# указать url картинки через пробел
# пример скачивания: python app.py https://angelamethist.com/image/ezgif.com-crop.gif https://dva.pw/images/designer_photo2.png