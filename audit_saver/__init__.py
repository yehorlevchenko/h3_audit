import psycopg2
from psycopg2.extras import RealDictCursor
import rabbitpy
import json
import pkgutil


class AuditSaver:
    def __init__(self):
        pass

    def run(self):
        with rabbitpy.Connection('amqp://rabbitmq:5672') as connection:
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

        with psycopg2.connect(dbname="audit",
                              user="postgres",
                              host="db",
                              port=5432,
                              password="postgres",
                              cursor_factory=RealDictCursor) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, audit_results)


if __name__ == '__main__':
    from time import sleep
    saver = AuditSaver()
    sleep(30)
    saver.run()
