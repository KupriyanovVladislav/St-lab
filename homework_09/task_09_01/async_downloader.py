import asyncio
import re
import requests

from aiohttp import ClientSession
from time import time
from task_09_01.thread_downloader import COUNTRY_REGEX, Country, urljoin


def write_image(data: str, filename: str):
    with open(f'flags/{filename}.png', 'wb') as out:
        out.write(data)


def load_image_linear(main_url: str):
    response = requests.get(main_url)

    time_start = time()

    for tup in re.findall(COUNTRY_REGEX, response.text):
        country = Country(*tup)
        response_flag = requests.get(urljoin(main_url, country.flag_url))
        write_image(response_flag.content, country.name)

    time_end = time()

    print(time_end - time_start)


async def fetch_content(url: str, name: str, session: ClientSession):
    async with session.get(url) as response:
        data = await response.read()
        write_image(data, name)


async def load_image_async(main_url: str):
    response = requests.get(main_url)
    tasks = []

    async with ClientSession() as session:
        for tup in re.findall(COUNTRY_REGEX, response.text):
            country = Country(*tup)
            tasks.append(asyncio.create_task(fetch_content(
                urljoin(main_url, country.flag_url),
                country.name,
                session
            )))

        await asyncio.gather(*tasks)


def async_main(main_url: str):
    time_start = time()
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(load_image_async(main_url))
    ioloop.close()
    print(time() - time_start)


if __name__ == '__main__':
    main_url = 'https://www.countryflags.io'
    async_main(main_url)
    load_image_linear(main_url)
