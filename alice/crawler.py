from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from representacao_livro import Livro


class Crawler:

    def __init__(self):
        self.chromeOptions = Options()
        self.chromeOptions.add_argument('--headless')
        self.path_driver = '/home/luiz/Downloads/chromedriver/chromedriver'

    def get_page(self, link):
        print(f'Acessando o link -> {link}')
        driver = webdriver.Chrome(executable_path=self.path_driver, chrome_options=self.chromeOptions)
        driver.get(link)
        time.sleep(3)
        return BeautifulSoup(driver.page_source, 'html.parser')

    def get_comments(self, link):
        base = 'https://www.amazon.com.br{}'
        comments_list = []
        prox_link = None
        print('Buscando -> {}'.format(base.format(link)))
        bs_comments = self.get_page(base.format(link))
        tags_comments = bs_comments.find('div', {'id': 'cm_cr-review_list'}) \
            .find_all('div', {'id': re.compile('[A-Z0-9]*-review-card')})
        for tag in tags_comments:
            try:
                comments = tag.find('span', {'class': 'review-text'}).span.get_text()
            except AttributeError:
                print('Erro ao obter um comentario!!!')
            else:
                comments_list.append(comments)
        prox = bs_comments.find('li', {'class': 'a-last'}).a
        if prox is not None:
            prox_link = bs_comments.find('li', {'class': 'a-last'}).a['href']
        return comments_list, prox_link

    def get_all_comments(self, link):
        all_comments = []
        for i in range(100):
            comments, prox_link = self.get_comments(link)
            all_comments.extend(comments)
            if prox_link is not None:
                link = prox_link
            else:
                break
        return all_comments

    def get_info_book(self, link):
        bs_livro = self.get_page(link)
        try:
            title = bs_livro.find('span', {'id': 'productTitle'}).get_text().strip()
            sub = bs_livro.find('span', {'id': 'productSubtitle'}).get_text().strip()
            price = bs_livro.find('span', {'id': 'price'}).get_text()
            auhor = bs_livro.find('div', {'id': 'bylineInfo'}).find('span', {'class': 'a-declarative'}).a.get_text()
            link_comments = bs_livro.find('div', {'id': 'reviews-medley-footer'}) \
                .find('a', {'class': 'a-link-emphasis'})['href']
        except AttributeError:
            print('Erro ao obter alguns atributos')
            return None
        else:
            list_comments = self.get_all_comments(link_comments)

        return Livro(auhor, title, sub, price, list_comments)
