#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: YangyangLi
@contact:li002252@umn.edu
@version: 0.0.1
@license: MIT Licence
@file: utils.py
@time: 2022-12-15
"""

import re
from pathlib import Path
import asyncio
import aiofiles
import aiohttp
from lxml import etree
from typing import List
import yaml
import logging

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def format_title(title: str):
    """Format title to be used in the URL.

    .. example::
        >>> format_title('The Art of Computer Programming, Volume 1: Fundamental Algorithms (3rd Edition)')
        'The Art of Computer Programming, Volume 1: Fundamental Algorithms'
    """

    title = title.rsplit("(")[0].strip()
    return title


def get_cover_images(items):
    asyncio.run(_get_cover_images(items))


async def download(url, name, headers, session: aiohttp.ClientSession) -> None:
    """Download a file from `url` and save it locally under `local_filename`."""
    try:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                async with aiofiles.open(
                    f"source/_static/covers/{name.replace(' ', '_')}.jpg", "wb"
                ) as f:
                    async for chunk in resp.content.iter_chunked(1024 * 1024):
                        await asyncio.sleep(0.001)
                        await f.write(chunk)
            else:
                raise RuntimeError(
                    f"Cannot download {url} with status code {resp.status}"
                )
    except Exception as e:
        LOGGER.error(f"Cannot download {url}: {e}")


async def _get_cover_images(items):
    timeout = aiohttp.client.ClientTimeout(2 * 60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = []
        for item in items:
            image_path = Path(
                f"source/_static/covers/{item['name'].replace(' ', '_')}.jpg"
            )
            if not image_path.exists():
                tasks.append(_get_cover_image_worker(item, session))
            else:
                LOGGER.info(f"Cover image for {item['name']} already exists")

        await asyncio.gather(*tasks)


async def _get_cover_image_worker(item, session):
    base_domain = "https://www.goodreads.com"
    search_domain = base_domain + "/search/"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 "
        "Safari/537.36",
        "Connection": "keep-alive",
    }

    title = item["name"]
    first_num = 2
    async with session.get(search_domain, params={"q": title}, headers=headers) as resp:
        try:
            resp.raise_for_status()
        except Exception as e:
            LOGGER.info(f"Failed to fetch {title} cover using default\n{e.args}")
        else:
            tree = etree.HTML(await resp.text())

            cover_urls: List[str] = tree.xpath(
                f"//table[@class='tableList']//tr[position()<{first_num}]//a[@class='bookTitle']/@href"
            )
            names: List[str] = tree.xpath(
                f"//table[@class='tableList']//tr[position()<{first_num}]//td/a/@title"
            )
            assert len(cover_urls) == len(names)

            if not cover_urls:
                LOGGER.info(f"Failed to fetch {title} cover using default")
            else:
                # fetch the first one
                cover = await _fetch_image(
                    session, base_domain + cover_urls[0], headers
                )
                await download(cover[0], title, headers, session)
                LOGGER.info(f"Successfully fetched {title} cover {cover[0]}")


async def _fetch_image(session, url, header):
    cover = []
    async with session.get(url, headers=header) as resp:
        try:
            resp.raise_for_status()
        except Exception as e:
            LOGGER.info(f"Failed to fetch image cover from {url} \n{e.args}")
            return cover
        else:
            t = await resp.text()
            tree = etree.HTML(t)
            cover.extend(tree.xpath("//img[@id='coverImage']/@src"))

            if not cover:
                # use Beautiful Soup
                from bs4 import BeautifulSoup

                soup = BeautifulSoup(t, "html.parser")

                tag = soup.find("img", {"class": "ResponsiveImage"})

                cover.append(tag.get("src"))

            if not cover:
                pat = re.compile(r"<img \n+ id=\"coverImage\" .+? src=\"(.+)\" />")
                cover.extend(re.findall(pat, t))

            return cover


def main():
    books = yaml.safe_load((Path("./source") / "library.yml").read_text())
    get_cover_images(books)


if __name__ == "__main__":
    main()
