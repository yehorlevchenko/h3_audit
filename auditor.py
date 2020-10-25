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
        """
        Main cycle of the class.
        """
        if self._connect():
            self.channel = self.connection.channel()
            queue = rabbitpy.Queue(self.channel, 'audit_start')
            for message in queue.consume():
                # TODO: add try\except and publosh broken messages to
                #  audit_error queue
                in_data = json.loads(message.body.decode('utf8'))
                try:
                    result = self.work(in_data)
                    self.finish_task(result)
                except Exception as e:
                    print(str(e))
                    pass
                message.ack()

    def _connect(self):
        """
        Connector - validator.
        :return: True if connected, False if connection attempts > 5
        """
        attempts = 5
        for attempt in range(1, attempts + 1):
            try:
                self.connection = rabbitpy.Connection('amqp://rabbitmq:5672')
                # self.connection = rabbitpy.Connection('amqp://0.0.0.0:5672')
                print("Successfully connected to RabbitMQ ...")
                break
            except Exception:
                if attempt == 5:
                    return False
                else:
                    idle_time = 10
                    print(f"Connection failed. "
                          f"Retrying in {idle_time} secs ...")
                    sleep(idle_time)

        return True

    def work(self, audit_data):
        """
        :param audit_data: dict with audit_id, main_url, limit of pages
        :return: list with audit result data for each page in list()
        """
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

            if page_data['status_code'] == 200:
                raw_tags = self.extractor.work(page_data['html'], start_url)
                new_url_set = raw_tags['a'].difference(url_set)
                for url in new_url_set:
                    self.queue.put(url)
                url_set.update(new_url_set)
                tag_errors = self.analyzer.work(raw_tags)

                page_result = [url, audit_data['audit_id'],
                               tag_errors['title'],
                               tag_errors['description'],
                               tag_errors['keywords'],
                               tag_errors['h1'],
                               tag_errors['h2'],
                               tag_errors['h3'],
                               page_data['status_code']]

            result_data.append(page_result)
            page_done_count += 1
            if page_done_count == page_limit:
                break
        return result_data

    def finish_task(self, result_data):
        """
        Publishes audit result data to RabbitMQ queue
        :param result_data: audit result dict
        """

        print(f"Auditor task finished: {result_data}")
        final_message = rabbitpy.Message(
            channel=self.channel,
            body_value=result_data
        )
        final_message.publish(exchange="audit", routing_key="audit_finish")


if __name__ == '__main__':
    a = Auditor()
    a.run()


