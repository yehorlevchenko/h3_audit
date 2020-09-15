from selectolax.parser import HTMLParser


class Extractor(HTMLParser):
    """
    Designed for extraction tags in self.tag_dict from HTML
    """
    def __init__(self, html_text, detect_encoding=True,
                 use_meta_tags=True, decode_errors=u'ignore'):

        super().__init__(html_text, detect_encoding=detect_encoding,
                         use_meta_tags=use_meta_tags,
                         decode_errors=decode_errors)
        self.tag_dict = {'meta_title': 'meta[property="og:title"]',
                         'meta_description': 'meta[property="og:description"]',
                         'meta_keywords': 'meta[property="og:keywords"]',
                         'h1': 'h1',
                         'h2': 'h2',
                         'h3': 'h3',
                         'a': 'a[href^="https"], a[href^="http"]'
                         }

    def find_all(self):
        """
        Collects all node lists to dict
        :return:dict(list(str))
        """
        result_dict = dict()
        for tag in self.tag_dict.keys():
            result_dict[tag] = self.find_tag(self.tag_dict[tag])
        return result_dict

    def find_tag(self, tag):
        """
        Extracts all nodes with tag name from HTML
        :param tag:
        :return: list(str) - str is node code and text
        """
        node_list = list()
        all_nodes = self.css(tag)
        for node in all_nodes:
            if node:
                node_list.append(node.html)
        return node_list


if __name__ == "__main__":
    html = """
    """
    extractor = Extractor(html)
    print(extractor.find_all())
