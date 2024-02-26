import requests
# from bs4 import BeautifulSoup
from newspaper import Article, ArticleException

class Loader:
    def load_url(url):
        article = Article(url)
        article.download()
        article.parse()
        text = article.text.replace('\n','')
                
        # response = requests.get(url)
        # soup = BeautifulSoup(response.content, 'html.parser')
        # text = ' '.join([p.text for p in soup.find_all('p')])
        return text