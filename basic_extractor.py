from bs4 import BeautifulSoup as bs4

from getter import Getter



class Extractor:
    '''
    :param html = accepts html string
    '''

    def __init__(self, html):
        self.html = bs4(str(html), 'html.parser')
        self.data_dict = dict()

    def work(self):
        self._parse_html()
        return self.data_dict

    def _parse_html(self):

        h1 = list()
        h2 = list()
        h3 = list()
        a = list()

        self.data_dict['meta title'] = self.html.title.string

        self.data_dict['meta description'] = self.html.find('meta', attrs={'name': "description"})

        self.data_dict['meta keywords'] = self.html.find('meta', attrs={'name': "keywords"})

        result_h1 = self.html.find_all('h1')

        for line_h1 in result_h1:
            h1.append(line_h1)

        result_h2 = self.html.find_all('h2')

        for line_h2 in result_h2:
            h2.append(line_h2)

        result_h3 = self.html.find_all('h3')

        for line_h3 in result_h3:
            h3.append(line_h3)

        result_a = self.html.select('a[href^="http://"]')

        for line_a in result_a:
            a.append(line_a)

        self.data_dict['h1, h2, h3'] = h1, h2, h3

        self.data_dict['a'] = a



if __name__ == '__main__':
    url_list = ['https://www.python.org'
    , 'https://www.python.org/about/',
             'https://www.python.org/doc/']
    getter = Getter()
    res = getter.work(url_list)
    parse = Extractor(res)
    print(parse.work())