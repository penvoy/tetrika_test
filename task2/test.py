import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import csv

from solution import WikiParser


class TestWikiParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = WikiParser()

    def test_get_animals(self):
        # Пример HTML с животными
        html_content = '''
        <div class="mw-category mw-category-columns">
            <div><a href="/wiki/Кот">Кот</a></div>
            <div><a href="/wiki/Собака">Собака</a></div>
        </div>
        '''
        soup = BeautifulSoup(html_content, "html.parser")
        animals = self.parser.get_animals(soup)
        self.assertEqual(animals, ["Кот", "Собака"])

    def test_get_next_link(self):
        # Пример HTML с ссылкой на следующую страницу
        html_content = '''
        <a href="/wiki/Категория:Животные_по_алфавиту_2">Следующая страница</a>
        '''
        soup = BeautifulSoup(html_content, "html.parser")
        link = self.parser.get_next_link(soup)
        self.assertEqual(link, "/wiki/Категория:Животные_по_алфавиту_2")

        # Тест без следующей страницы
        html_content_no_next = '''
        <div>No next link here</div>
        '''
        soup_no_next = BeautifulSoup(html_content_no_next, "html.parser")
        link_no_next = self.parser.get_next_link(soup_no_next)
        self.assertIsNone(link_no_next)
    
    @patch("aiohttp.ClientSession.get", new_callable=AsyncMock)
    async def test_get_page_data(self, mock_get):
        url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
        mocked_response = MagicMock()
        mocked_response.text = AsyncMock(return_value="Test HTML")
        mock_get.return_value.__aenter__.return_value = mocked_response

        soup = await self.parser.get_page_data(aiohttp.ClientSession(), url)
        self.assertEqual(soup, "Test HTML")  # Проверяем, что текст вернулся правильно

    @patch("csv.writer")
    async def test_save_data(self, mock_csv_writer):
        data = {'К': 1, 'С': 2}
        await self.parser.save_data("test.csv", data)
        mock_csv_writer().writerow.assert_any_call(['К', 1])
        mock_csv_writer().writerow.assert_any_call(['С', 2])
    
    @patch("aiohttp.ClientSession")
    @patch.object(WikiParser, "get_page_data", new_callable=AsyncMock)
    def test_parse(self, mock_get_page_data, mock_session):
        mock_get_page_data.side_effect = [
            BeautifulSoup('<div class="mw-category mw-category-columns"><div><a href="#">Кот</a></div></div>', "html.parser"),
        ]

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.parser.parse())
        
        # Проверяем, что данные были сохранены
        with open("beasts.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = [[row[0], int(row[1])] for row in reader]
            self.assertIn(['К', 1], rows)

if __name__ == "__main__":
    unittest.main()