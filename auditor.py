import rabbitpy
import json
from queue import SimpleQueue

from getter import Getter
from extractor import Extractor
from analyzer import Analyzer


class Auditor:
    def __init__(self):
        self.getter = Getter()
        self.extractor = Extractor()
        self.analyzer = Analyzer()

    def run(self):
        with rabbitpy.Connection('amqp://localhost:5672') as connection:
            with connection.channel() as channel:
                queue = rabbitpy.Queue(channel, 'audit_start')
                for message in queue.consume():
                    # TODO: add try\except and publosh broken messages to
                    #  audit_error queue
                    in_data = json.loads(message.body.decode('utf8'))
                    result = self.work(in_data)
                    self.finish_task(channel, in_data, result)
                    message.ack()

    def work(self, audit_data):
        page_limit = audit_data['limit']
        page_done_count = 0
        start_url = audit_data['main_url']
        result_data = list()
        new_url_set = {start_url}
        url_queue = SimpleQueue()

        if not start_url.endswith('/'):
            start_url = f'{start_url}/'

        while not url_queue.empty():
            url = url_queue.get
            page_data = self.getter.work(url)
            page_result = {
                'status_code': page_data['status_code'],
                'url': url
            }

            if page_data['status_code'] == 200:
                raw_tags = self.extractor.work(page_data['html'], start_url)
                url_set = raw_tags['a'].difference(url_set)

                for url in url_set:
                    url_queue.put(url)
                new_url_set.update(url_set)

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


