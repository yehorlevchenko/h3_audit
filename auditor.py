import rabbitpy
import json
from queue import SimpleQueue
from time import sleep

from getter import Getter
from extractor import Extractor
from analyzer import Analyzer


class Auditor:
    def __init__(self):
        self.getter = Getter()
        self.extractor = Extractor()
        self.analyzer = Analyzer()
        self.queue = SimpleQueue()
        self.connection = None
        self.channel = None

    def run(self):
        if self._connect():
            self.channel = self.connection.channel()
            queue = rabbitpy.Queue(self.channel, 'audit_start')
            for message in queue.consume():
                # TODO: add try\except and publosh broken messages to
                #  audit_error queue
                in_data = json.loads(message.body.decode('utf8'))
                result = self.work(in_data)
                self.finish_task(self.channel, in_data, result)
                message.ack()

    def _connect(self):
        attempts = 5
        for attempt in range(1, attempts + 1):
            try:
                self.connection = rabbitpy.Connection('amqp://rabbitmq:5672')
            except Exception:
                if attempt == 5:
                    return False
                else:
                    sleep(15)

        return True

    def work(self, audit_data):
        page_limit = audit_data['limit']
        page_done_count = 0
        result_data = list()
        start_url = audit_data['main_url']

        if not start_url.endswith('/'):
            start_url = f'{start_url}/'

        url_set = {start_url}
        self.queue.put(*url_set)

        while not self.queue.empty():
            url = self.queue.get()
            page_data = self.getter.work(url)
            page_result = {
                'status_code': page_data['status_code'],
                'url': url
            }

            if page_data['status_code'] == 200:
                raw_tags = self.extractor.work(page_data['html'], start_url)
                new_url_set = raw_tags['a'].difference(url_set)
                for url in new_url_set:
                    self.queue.put(url)
                url_set.update(new_url_set)
                page_result.update(self.analyzer.work(raw_tags))

            result_data.append(page_result)
            page_done_count += 1
            if page_done_count == page_limit:
                break

        return result_data

    def finish_task(self, channel, task_data, result_data):
        # audit_results = {"audit_id": 1,
        #                  "main_url": "http://python.org",
        #                  "page_data": [%dict with page results%]
        #                  }
        final_message = rabbitpy.Message(
            channel=channel,
            body_value=result_data
        )
        final_message.publish(exchange="audit", routing_key="audit_finish")



if __name__ == '__main__':
    a = Auditor()
    a.run()


