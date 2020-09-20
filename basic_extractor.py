from bs4 import BeautifulSoup as bs4


class Extractor:

    def __init__(self, html):
        self.html = bs4(str(html), 'html.parser')
        self.result_dict = dict()

    def work(self):

        white_list = ['a[href^="http://"]', 'a[href^="https://"]', 'a[href^="ftp://"]']
        clear_list = list()
        self.result_dict = {'meta title': self.html.title.string,
                            'meta description': self.html.find('meta', attrs={'name': "description"}),
                            'meta keywords': self.html.find('meta', attrs={'name': "keywords"}),
                            'h1': [h1 for h1 in self.html.find_all('h1')],
                            'h2': [h2 for h2 in self.html.find_all('h2')],
                            'h3': [h3 for h3 in self.html.find_all('h3')]}

        for tag in white_list:
            for line in self.html.select(tag):
                clear_list.append(line)
        self.result_dict['a'] = clear_list

        return self.result_dict


if __name__ == '__main__':
    from getter import Getter

    url_list = ['https://www.python.org',
                'https://www.python.org/about/',
                'https://www.python.org/doc/']
    getter = Getter()
    res = getter.work(url_list)
    parse = Extractor(res)
    print(parse.work())
