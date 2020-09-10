import requests


class Getter:
    def __init__(self):
        pass

    def work(self, url_list):
        """
        :return: list(dict(url, status_code, html))
        """
        result = self._get_html(url_list)
        return result

    def _get_html(self, url_list):
        """
        :return: list(dict(url, status_code, html))
        """
        result = list()
        session = requests.Session()
        # TODO: consider implementing UA generator
        headers = {'user-agent':
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) '
                       'AppleWebKit/605.1.15 (KHTML, like Gecko) '
                       'Version/13.1.2 Safari/605.1.15'}
        for url in url_list:
            custom_status = None
            try:
                response = session.get(url, headers=headers)
            except requests.exceptions.ConnectionError as e:
                custom_status = 1001
            except requests.exceptions.Timeout as e:
                custom_status = 1002
            except Exception as e:
                custom_status = 1013
            finally:
                url_result = {
                    "url": url,
                    "status_code": custom_status if custom_status
                    else response.status_code,
                    "html": '' if custom_status else response.text
                }
                result.append(url_result)

        return result


if __name__ == "__main__":
    url_list = ['https://www.python.org', 'https://www.python.org/about/',
                'https://www.python.org/doc/']
    getter = Getter()
    res = getter.work(url_list)
    print(res)
