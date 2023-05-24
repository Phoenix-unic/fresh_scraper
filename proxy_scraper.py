import requests
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Scraper:
    def __init__(self, url: str) -> None:
        self.headers = {
            'user-agent': UserAgent().chrome,
            'accept': '*/*'} 
        self.url = url
        self.proxy_list = []

    def is_200_status(self):
        code = requests.get(self.url).status_code
        return  code == 200
    
    def get_soup(self) -> BeautifulSoup:
        response = requests.get(url=self.url, headers=self.headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        return soup
    
    def get_data(self, soup: BeautifulSoup) -> None:
        table_rows = soup.select_one('.table.table-striped').select('tr')
        for row in table_rows:
            try:
                ip, port, code, country, anonimity, google, https, last_checked = [item.text.strip() for item in row.select('td')]
                proxy_data = {
                    'ip': ip, 
                    'port': port, 
                    'code': code, 
                    'coutnry': country, 
                    'anonimity': anonimity, 
                    'google': google, 
                    'https': https, 
                    'last_checked': last_checked
                    }
                self.proxy_list.append(proxy_data)
            except ValueError :
                continue

    def write_to_json(self, file_name: str) -> None:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(self.proxy_list, file, indent=4, ensure_ascii=False)
        print(f'{file_name} is created...')





def main():
    url='https://free-proxy-list.net/'
    scrap = Scraper(url)
    if scrap.is_200_status():
        sp = scrap.get_soup()
        scrap.get_data(sp)
        scrap.write_to_json(file_name='fresh_proxies.json')


if __name__ == '__main__':
    main()