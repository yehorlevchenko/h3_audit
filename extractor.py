from bs4 import BeautifulSoup
import re


class Extractor:
    """
    Designed for extraction tags in self.tag_dict from HTML
    """

    def __init__(self):
        self.tag_dict = {'title': 'title',
                         'meta_title': {'name': 'title'},
                         'description': {'name': 'description'},
                         'keywords': {'name': 'keywords'},
                         'h1': 'h1',
                         'h2': 'h2',
                         'h3': 'h3',
                         'a': 'a'}

    def work(self, raw_html):
        """
        Collects all node lists to dict
        :return:dict(list(str))
        """
        soup = BeautifulSoup(raw_html, 'lxml')
        result = dict()
        for tag, tag_value in self.tag_dict.items():
            extract_tags = soup.find_all(tag_value)
            if extract_tags:
                if tag == 'a':
                    result[tag] = self._clear_a(extract_tags)
                else:
                    result[tag] = [item.getText() for item in extract_tags]
            else:
                extract_tags = soup.find_all('meta', attrs=tag_value)
                result[tag] = [item.get('content') for item in extract_tags]
        return result

    def _clear_a(self, a_list):
        unique_a = set()
        # whitelist = ['/', './', 'https://', 'http://', 'ftp://']
        # TODO: THIS PATTERN MATCHES ABSOLUTE LINKS, SHOULD ALSO MATCH RELATIVE
        # TODO: PATTERN SHOULD NOT MATCH RELATIVE LINKS STARTING WITH //
        pattern = '/?https?:\/\/w{0,3}\w*?\.(\w*?\.)?\w{2,3}\S*|www\.(\w*?\.)?\w*?\.\w{2,3}\S*|(\w*?\.)?\w*?\.\w{2,3}[\/\?]\S*/'

        for tag in a_list:
            href = tag.get('href')
            check = re.match(pattern, href)
            if check:
                if check.groups():
                    unique_a.add(tag.get('href'))
        return list(unique_a)


if __name__ == "__main__":
    import requests
    headers = {'user-agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    response = requests.get('https://www.python.org', headers=headers)
    # print(response.text)
    extractor = Extractor(response.text)
    print(extractor.work())