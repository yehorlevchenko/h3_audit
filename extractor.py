from selectolax.parser import HTMLParser


class Exctractor:
    def __init__(self):
        self.tags_needed = {'meta_title': 'meta[property="og:title"]',
                            'meta_description': 'meta[property="og:description"]',
                            'meta_keywords': 'meta[property="og:keywords"]',
                            'h1': 'h1',
                            'h2': 'h2',
                            'h3': 'h3',
                            'a': 'a[href^="http"]'}

    def parser(self, html_page):
        result = {}
        for tag in self.tags_needed.keys():
            x=HTMLParser(html_page).css(self.tags_needed[tag])
            for node in x:
                result[tag]=[tag, node.html]
        return result


html_page='''
'''
extractor = Exctractor()
res = extractor.parser(html_page)
print(res)



