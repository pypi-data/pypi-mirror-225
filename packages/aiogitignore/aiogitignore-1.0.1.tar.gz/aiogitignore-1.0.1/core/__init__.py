import asyncio
import sys
import aiohttp
import async_lru
import os

URL = r"https://www.toptal.com/developers/gitignore/api/"


@async_lru.alru_cache(maxsize=1024)
async def get_gitignore(language: str) -> str:
    """Get the `.gitignore` file for the selected language.

    Args:
        language (str): language.

    Returns:
        str: Git ignore file.
    """
    url = URL + language.lower()
    async with aiohttp.ClientSession() as session:
        print(f"Initializing request for {language.capitalize()}...")
        async with session.get(url) as response:
            print(f"Request for {language.capitalize()} completed.")
            return await response.text()


async def get_gitignore_list(*args: str) -> list[str]:
    """Gets the files associated to the languages.

    Returns:
        list[str]: list of files.
    """
    return await asyncio.gather(
        *[get_gitignore(lang) for lang in args if not lang.startswith("-")]
    )


def check_if_file_exists() -> None:
    """Check if the `.gitignore` file already exists.

    Raises:
        FileExistsError: if the file exists and will not be overwritten.
    """
    if os.path.exists(".gitignore") and (
        "--overwrite" not in sys.argv or "-o" not in sys.argv
    ):
        raise FileExistsError(
            "File already exists. Use --overwrite or -o to overwrite it."
        )
