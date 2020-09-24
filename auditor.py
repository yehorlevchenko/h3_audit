import rabbitpy
import json

from getter import Getter
from extractor import Extractor
from analyzer import Analyzer


class Auditor:
    def __init__(self):
        self.getter = Getter()
        self.extractor = Extractor()
        self.analyzer = Analyzer()

    def run(self):
        for message in rabbitpy.consume('amqp://localhost:5672', 'audit_start'):
            in_data = json.loads(message.body.decode('utf8'))
            result = self.work(in_data['url_list'])
            message.ack()
            print(result)

    def work(self, url_list):
        if isinstance(url_list, str):
            url_list = [url_list]

        raw_page_list = self.getter.work(url_list)
        for raw_page_data in raw_page_list:
            if raw_page_data['status_code'] == 200:
                raw_tags = self.extractor.work(raw_page_data['html'])
                results = self.analyzer.work(raw_tags)
                return results




if __name__ == '__main__':
    a = Auditor()
    # a.work("http://python.org")
    a.run()


