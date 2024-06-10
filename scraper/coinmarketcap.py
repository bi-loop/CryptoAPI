import requests
from bs4 import BeautifulSoup

class CoinMarketCap:
    BASE_URL = "https://coinmarketcap.com/currencies/"

    @staticmethod
    def fetch_coin_data(coin):
        url = f"{CoinMarketCap.BASE_URL}{coin}/"
        response = requests.get(url)
        if response.status_code == 200:
            return CoinMarketCap.parse_coin_data(response.text)
        else:
            return None

    @staticmethod
    def parse_coin_data(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        data = {}

        # Scrape necessary details here
        # Example:
        data['price'] = soup.select_one("#section-coin-overview > div:nth-of-type(2) > span").text
        data['market cap'] = soup.select_one('#section-coin-stats > div > dl > div:nth-of-type(1) > div:nth-of-type(1) > dd').text
        data['volume'] = soup.select_one('#section-coin-stats > div > dl > div:nth-of-type(2) > div:nth-of-type(1) > dd').text
        data['volume rank'] = soup.select_one('#section-coin-stats > div > dl > div:nth-of-type(2) > div:nth-of-type(2) > div > span').text
        data['circulating supply'] = soup.select_one('#section-coin-stats > div > dl > div:nth-of-type(4) > div > dd').text
        data['total supply'] = soup.select_one('#section-coin-stats > div > dl > div:nth-of-type(5) > div > dd').text
        data['max supply'] = soup.select_one('#section-coin-stats > div > dl > div:nth-of-type(6) > div > dd').text
        data['fully diluted market cap'] = soup.select_one('#section-coin-stats > div > dl > div:nth-of-type(7) > div > dd').text
        
        return data
