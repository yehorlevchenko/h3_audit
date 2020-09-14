from selectolax.parser import HTMLParser, Node


class Extractor(HTMLParser):

    def __init__(self, html, detect_encoding=True,
                 use_meta_tags=True, decode_errors=u'ignore'):

        super().__init__(html, detect_encoding=detect_encoding,
                         use_meta_tags=use_meta_tags,
                         decode_errors=decode_errors)

    def find_all(self, tag_list):
        """
        :param tag_list: list(str)
        :return:
        """
        tag_dict = dict()
        for tag in tag_list:
            tag_dict[tag] = self.find_tag(tag)
        return tag_dict

    def find_tag(self, tag):
        """
        :param tag:
        :return: list(str) - str is node code and text
        """
        node_list = list()
        all_nodes = self.css(tag)
        for node in all_nodes:
            if self._validate_node(node):
                node_list.append(node.html)
        return node_list

    def _validate_node(self, node):
        if node:
            if node.tag == 'a':
                try:
                    link = node.attributes['href']
                except AttributeError:
                    return False
                return not (link.startswith('mailto:') or link.startswith('file:'))
        else:
            return False


if __name__ == "__main__":
    html = """
    """
    extractor = Extractor(html)
    tag_list = ['title', 'description', 'keywords', 'h1', 'h2', 'h3', 'a']
    print(extractor.find_all(tag_list))