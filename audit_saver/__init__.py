import psycopg2
from psycopg2.extras import RealDictCursor
import rabbitpy
import json
import pkgutil


class AuditSaver:
    def __init__(self):
        pass

    def run(self):
        with rabbitpy.Connection('amqp://localhost:5672') as connection:
            with connection.channel() as channel:
                queue = rabbitpy.Queue(channel, 'audit_finish')
                for message in queue.consume():
                    audit_results = json.loads(message.body.decode('utf8'))
                    self.save_data(audit_results)
                    message.ack()

    def save_data(self, audit_results):
        query = pkgutil.get_data('audit_saver', 'data/insert_audit_result.sql')
        if not query:
            raise RuntimeError('Failed to find insert_audit_result query')

        with psycopg2.connect(dbname="postgres",
                              user="postgres",
                              host="0.0.0.0",
                              port=5432,
                              password="postgres",
                              cursor_factory=RealDictCursor) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, audit_results)


if __name__ == '__main__':
    test_data = {"audit_id": 1,
                 "main_url": 'http://python.org',
                 'title': [1110],
                 'description': [],
                 'keywords': [1151],
                 'h1': [1161],
                 'h2': [],
                 'h3': [1180]}
    saver = AuditSaver()
    saver.save_data(test_data)
