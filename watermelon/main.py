import typer
import shutil
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from youtubesearchpython import VideosSearch
from loguru import logger

from src.download import Downloader
from src.player import Player

app = typer.Typer()


@app.command()
def sync_top100(
    melon_url: str = "https://www.melon.com/chart/index.htm",
    downloader_url: str = "http://localhost:8998",
    downloader_api: str = "cafe0a23-28b3-46c8-b3bc-093694898c2b",
    player_url: str = "http://localhost:13378",
    audio_save_dir: str = "./watermelon/player/audiobooks/top100",
):
    shutil.rmtree(audio_save_dir)
    os.makedirs(audio_save_dir, exist_ok=True)

    # Get HTML using Webdriver with BeautifulSoup
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get(melon_url)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Make a DataFrame
    titles = [song.text.strip("\n") for song in soup.select("div.ellipsis.rank01")]
    singers = [
        singer.text
        for singer in soup.select("div.ellipsis.rank02 > span.checkEllipsis")
    ]
    logger.info(f"singers: {len(singers)}")

    # Close webdriver
    driver.close()
    driver.quit()

    downloader = Downloader(url=downloader_url, api_key=downloader_api)
    for singer, title in zip(singers, titles):
        search_results = VideosSearch(f"{singer} - {title} Lyrics", limit=1).result()[
            "result"
        ]

        title = search_results[0]["title"]
        link = search_results[0]["link"]

        logger.info(f"title: {title} link: {link}")
        downloader.download_file(link=link)

    logger.info("Download Done!!")

    player = Player(url=player_url)
    lib_id = player.get_all_libraries()["libraries"][0]["id"]

    player.scan_library(lib_id=lib_id)


if __name__ == "__main__":
    app()
