import json
from queue import Queue
import rabbitpy
import threading

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
        result_queue = Queue()
        result_list = list()
        with rabbitpy.Connection('amqp://localhost:5672') as connection:
            with connection.channel() as channel:
                queue = rabbitpy.Queue(channel, 'audit_start')
                for message in queue.consume():
                    # TODO: add try\except and publish broken messages to
                    #  audit_error queue
                    in_data = json.loads(message.body.decode('utf8'))

                    # Slicing data into list(list() * thread_amount)
                    data_sliced = [in_data['url_list'][i::self.thread_amount] for i in range(self.thread_amount)]

                    threads = [threading.Thread(target=lambda q, arg: q.put(self.work(arg)),
                                                args=(result_queue, urls)) for urls in data_sliced]
                    [thread.start() for thread in threads]
                    [thread.join() for thread in threads]

                    while not result_queue.empty():
                        result_list.append(result_queue.get())
                    self.finish_task(channel, in_data, result_list)
                    message.ack()

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


