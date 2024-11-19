import asyncio
import aiohttp
import csv
from bs4 import BeautifulSoup

class ExitParseException(Exception):
    pass

class WikiParser:
    def __init__(self) -> None:
        self.base_url = "https://ru.wikipedia.org"
        self.parse_url = "/wiki/Категория:Животные_по_алфавиту"

    # метод для получения списка животных
    def get_animals(self, soup: BeautifulSoup) -> list[str]:
        # находим все теги div с классом 
        columns = soup.find_all("div", class_="mw-category mw-category-columns")

        # собираем теги <a>
        links = [animal.findAll("a") for animal in columns][0]

        # собираем список животных 
        animals = [animal.text for animal in links]
        return animals

    # метод для получения ссылки на следующую страницу
    def get_next_link(self, soup: BeautifulSoup) -> str:
        link = soup.find("a", string="Следующая страница")
        return link.get("href") if link else None

    # метод для создания csv файла и записи данных в него
    async def save_data(self, filename: str, data: dict) -> None:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for key, value in data.items():
                writer.writerow([key, value])
    
    # метод для запроса по урлу
    async def get_page_data(self, session: aiohttp.ClientSession, url: str) -> BeautifulSoup:
        try:
            async with session.get(url, timeout=5) as response:
                resp = await response.text()
                soup = BeautifulSoup(resp, "html.parser")  
                return soup
        except Exception as e:
            raise e

    # главный метод для получения данных с wiki и преобразования в csv
    async def parse(self) -> None:
        data = {}
        try:
            async with aiohttp.ClientSession() as session:
                while True:
                    # делаем запрос и получаем данные 
                    page = await self.get_page_data(session, self.base_url + self.parse_url)

                    # получаем список животных
                    animals = self.get_animals(page)
                    for animal in animals:
                        # не берём животных на латинице
                        if animal[0] == "A":
                            raise ExitParseException()
                        
                        # считаем кол-во животных на букву
                        if not animal[0] in data.keys():
                            data[animal[0]] = 1
                            continue

                        data[animal[0]] += 1
                    # получаем ссылку на след страницу
                    next_link = self.get_next_link(page)
                    if next_link:
                        self.parse_url = next_link
                    else:
                        break
        except ExitParseException:
            pass 
        finally:
            await self.save_data("beasts.csv", data)

if __name__ == "__main__":
    asyncio.run(WikiParser().parse())