import threading

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
        self.thread_amount = 3

    def run(self):
        for message in rabbitpy.consume('amqp://localhost:5672', 'audit_start'):
            in_data = json.loads(message.body.decode('utf8'))
            if isinstance(in_data['url_list'], str):
                in_data['url_list'] = list(in_data['url_list'])

            # Slicing data into list(list() * thread_amount)
            data_sliced = [in_data['url_list'][i::self.thread_amount] for i in range(self.thread_amount)]

            threads = [threading.Thread(target=self.work, args=urls) for urls in data_sliced]
            [threads[i].start() for i in range(len(threads))]
            [threads[i].join() for i in range(len(threads))]

            message.ack()

    def work(self, url_list):
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


