import requests
from bs4 import BeautifulSoup

class Loader:
    def load_url(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # ここでは例として、すべての段落のテキストを結合しています。
        # 必要に応じて、特定の要素を取得するようにカスタマイズしてください。
        text = ' '.join([p.text for p in soup.find_all('p')])
        return text