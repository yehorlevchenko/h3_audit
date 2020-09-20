

class Analyzer:
    """
    1100-1109 - title errors
    1110-1119 - description errors
    1120-1129 - keywords errors
    """

    def __init__(self):
        pass

    def work(self, tag_dict):
        check_result_dict = dict()
        for tag, data in tag_dict.items():
            try:
                check = getattr(self, f'_check_{tag}')
            except AttributeError:
                print(f'Unknown check: _check_{tag}')
            else:
                if callable(check):
                    check_result_dict[tag] = check(data)
        return check_result_dict

    def _check_title(self, data):
        check_result = list()
        if not data:
            # err_msg = 'Missing title'
            check_result.append(1100)
            return check_result

        if len(data) > 1:
            # err_msg = 'Multiple titles found on page'
            check_result.append(1101)
            return check_result

        if len(data[0]) < 80:
            # err_msg = 'Title to short'
            check_result.append(1102)
            return check_result

        elif len(data[0]) > 140:
            # err_msg = 'Title to short'
            check_result.append(1103)
            return check_result

    def _check_description(self, data):
        check_result = list()
        if not data:
            # err_msg = 'Missing description'
            check_result.append(1110)
            return check_result

        if len(data) > 1:
            # err_msg = 'Multiple descriptions found on page'
            check_result.append(1111)
            return check_result

        if len(data[0]) < 50:
            # err_msg = 'Descriptions to short'
            check_result.append(1112)
            return check_result

        elif len(data[0]) > 160:
            # err_msg = 'Descriptions to long'
            check_result.append(1113)
            return check_result

    def _check_keywords(self, data):
        check_result = list()
        if not data:
            # err_msg = 'Missing keywords'
            check_result.append(1120)
            return check_result

        if len(data) > 1:
            # err_msg = 'Multiple keywords found on page'
            check_result.append(1121)
            return check_result

        if len(data[0].split(',')) < 3:
            # err_msg = 'Keywords to short'
            check_result.append(1122)
            return check_result

        elif len(data[0].split(',')) > 10:
            # err_msg = 'Keywords to long'
            check_result.append(1123)
            return check_result


if __name__ == '__main__':
    tag_dict = {'title': ['<title>Welcome to Python.org</title>'],
                'description': ['<meta content="The official home '
                                'of the Python Programming Language" '
                                'name="description"/>'],
                'keywords': ['<meta content="Python programming language, '
                             'object oriented web free open source software" '
                             'name="keywords"/>'],
                'h1': ['<h1>Functions Defined</h1>',
                       '<h1>Compound Data Types</h1>',
                       '<h1>Intuitive Interpretation</h1>'],
                'h2': ['<h2>Get Started</h2>',
                       '<h2>Download</h2>'],
                'h3': [],
                'a': ['<a href="/about/apps/" '
                      'title="">Applications</a>',
                      '<a class="tag" '
                      'href="http://www.ansible.com">'
                      'Ansible</a>',
                      '<a href="/success-stories/" '
                      'title="More Success Stories">More</a>']}
    analyzer = Analyzer()
    result = analyzer.work(tag_dict)
    print(result)
