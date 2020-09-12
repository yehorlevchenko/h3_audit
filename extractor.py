from bs4 import BeautifulSoup


class Extractor:
    def __init__(self):
        self.tag_dict = {'title': 'title',
                         'description': {'name': 'description'},
                         'keywords': {'name': 'keywords'},
                         'h1': 'h1',
                         'h2': 'h2',
                         'h3': 'h3',
                         'a': self._extract_a}

    def work(self, raw_html):
        """
        Main func of extractor. Creates the final result by going
        through the self.tag_dict

        :return: dict{tag1:[extracting values of tag1],
                      tag2:[extracting values of tag2]}
        """
        self.soup = BeautifulSoup(raw_html, 'lxml')
        result = dict()
        for tag, tag_value in self.tag_dict.items():
            if callable(tag_value):
                result[tag] = [str(item) for item in tag_value()]
            else:
                extract_tags = self.soup.find_all(tag_value)
                if extract_tags:
                    result[tag] = [str(item) for item in extract_tags]
                else:
                    extract_tags = self.soup.find_all(attrs=tag_value)
                    result[tag] = [str(item) for item in extract_tags]
        return result

    def _extract_a(self):
        """
        The method extracting all <a> tags. Keeps only unique
        links in the href= that start with whitelist
         such as "http://", "/" etc.

        :return: list[extracting values]
        """
        a_list = self.soup.find_all(['a', 'href'])
        unique_a = set()
        whitelist = ['/', 'https://', 'http://', 'ftp://']
        for tag in a_list:
            href = tag.get('href')
            if any(href.startswith(prefix) for prefix in whitelist):
                unique_a.add(tag)
        return list(unique_a)


if __name__ == '__main__':
    import requests
    headers = {'user-agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    response = requests.get('https://www.python.org', headers=headers)
    extractor = Extractor()
    print(extractor.work(response.text))
