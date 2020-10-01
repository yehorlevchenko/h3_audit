import rabbitpy
import json
import threading

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
            if isinstance(in_data['url_list'], str):
                in_data['url_list'] = list(in_data['url_list'])

            while True:
                if len(threading.enumerate()) <= 4:
                    thread = threading.Thread(target=self.work, args=in_data['url_list'])
                    thread.start()
                    message.ack()
                    break

    def work(self, url_list):
        if isinstance(url_list, str):
            url_list = [url_list]

        raw_page_list = self.getter.work(url_list)
        for raw_page_data in raw_page_list:
            if raw_page_data['status_code'] == 200:
                raw_tags = self.extractor.work(raw_page_data['html'])
                results = self.analyzer.work(raw_tags)
                return results

    def finish_task(self, channel, task_data, result_data):
        # task_data = {"audit_id": 1, "main_url": "http://python.org", "url_list": ["http://python.org"]}
        # result_data = {'title': [1110], 'description': None, 'keywords': [1151], 'h1': [1161], 'h2': None, 'h3': [1180]}
        task_data.pop('url_list')
        result_data.update(task_data)
        final_message = rabbitpy.Message(
            channel=channel,
            body_value=result_data
        )
        final_message.publish(exchange="audit", routing_key="audit_finish")



if __name__ == '__main__':
    a = Auditor()
    # a.work("http://python.org")
    a.run()


