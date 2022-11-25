from crawler import Crawler
from limpeza import CleanComents

link = 'https://www.amazon.com.br/Alice-Pa%C3%ADs-das-Maravilhas-Classic/dp/8594541759/\
ref=sr_1_4?keywords=alice+no+pa%C3%ADs+das+maravilhas&qid=1665860065&qu=\
eyJxc2MiOiIzLjc3IiwicXNhIjoiMy40MCIsInFzcCI6IjMuNDMifQ%3D%3D&sprefix=alice%2Caps%2C391&sr=8-4'

# Instânciando a classe responsável pela raspagem do site
crawler = Crawler()
livro = crawler.get_info_book(link)

print(livro)

mongodb = MongoDB('biblioteca')
db = mongodb()

# Inserindo no banco de dados
db.livros.insert_one(livro.json())

# Buscando no banco de dados
alice = db.livros.find_one({'titulo': 'Alice no País das Maravilhas (Classic Edition)'})

# Instânciando a classe responsável por sanitizar os comentários
cleancoments = CleanComents(alice['comentarios'])

# Sanitizando os comentários
cleancoments.clean()

print(cleancoments.list_words)

print(cleancoments.counter())

cleancoments.word_clound()
