import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
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
                    try:
                        print(f"Got audit results {audit_results}")
                        self.save_data(audit_results)
                    except Exception as e:
                        print(e)
                    message.ack()

    def save_data(self, audit_results):
        query = """
        INSERT INTO panel_auditresults (url,
                                audit_id_id,
                                title_errors,
                                description_errors,
                                keywords_errors,
                                h1_errors,
                                h2_errors,
                                h3_errors,
                                status_code)
        VALUES %s;  
        """
        print(f"Saving audit results: {audit_results}")
        with psycopg2.connect(dbname="audit",
                              user="postgres",
                              host="db",
                              port=5432,
                              password="postgres",
                              cursor_factory=RealDictCursor) as connection:
            with connection.cursor() as cursor:
                to_tuple = tuple(i for i in audit_results)
                execute_values(cursor, query, to_tuple)
        print("Successfully saved")


if __name__ == '__main__':
    from time import sleep
    saver = AuditSaver()
    sleep(30)
    saver.run()
