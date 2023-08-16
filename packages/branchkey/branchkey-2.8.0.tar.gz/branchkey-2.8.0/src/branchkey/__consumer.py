import json
import logging
import sys
from queue import Queue
from threading import Thread

import pika

from .utils import RBMQ_aggregation_status, RBMQ_run_status


class Consumer:
    def __init__(self, config: dict, msg_queue: Queue, run_status_callback):
        self.msg_queue = msg_queue
        self.run_status_callback = run_status_callback
        rabbitmq_config = {"leaf_name": "",
                           "leaf_id": "",
                           "queue_password": "",
                           "host": "response.branchkey.com",
                           "port": 5672,
                           "branch_id": "",
                           "tree_id": "",
                           "heartbeat_time_s": 30,
                           "conn_retries": 3,
                           "conn_retry_delay_s": 3}

        for key in config:
            rabbitmq_config[key] = config[key]

        self.queue_name = rabbitmq_config['leaf_id']

        self.rabbitmq_config = rabbitmq_config

        self.conn = self.__get_connection()
        self.channel = self.conn.channel()
        self.exchange = self.rabbitmq_config['branch_id']

    def __get_connection(self):
        try:
            creds = pika.PlainCredentials(
                self.rabbitmq_config["leaf_id"], self.rabbitmq_config["queue_password"])

            conn = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.rabbitmq_config["host"],
                port=self.rabbitmq_config["port"],
                virtual_host=self.rabbitmq_config['tree_id'],
                credentials=creds,
                heartbeat=int(self.rabbitmq_config["heartbeat_time_s"]),
                connection_attempts=int(self.rabbitmq_config["conn_retries"]),
                retry_delay=int(self.rabbitmq_config["conn_retry_delay_s"]),
                client_properties={"connection_name": "leaf-"+self.rabbitmq_config["leaf_id"]}))

        except Exception as e:
            sys.exit("[Consumer] Error while connecting to rabbitmq: " + str(e))

        else:
            return conn

    def __callback(self, ch, method, properties, body):
        try:
            msg = body.decode()
            logging.debug("[Consumer] Message received: " + str(msg))
        except Exception("Error with msg from RabbitMQ") as e:
            logging.error(
                f"[Consumer] Failed with msg from RabbitMQ {str(msg)}")
            raise e
        try:
            msg = json.loads(msg)
        except Exception as e:
            logging.error(f"[Consumer] Failed decode message to JSON {str(e)}")
            raise e
        if 'message_type' not in msg:
            raise Exception("message_type not in msg from RBMQ")
        logging.debug(
            f"[Consumer] Message type ready {type(msg['message_type'])}")

        if msg['message_type'] == RBMQ_aggregation_status:
            logging.debug("[Consumer] Putting agg_id to Queue: " +
                          str(msg['body']['aggregation_id']))
            if self.msg_queue.full():
                logging.debug("[Consumer] Removing old agg_id from Queue: " +
                          str(self.msg_queue.get(block=True)))
            self.msg_queue.put(msg['body']['aggregation_id'], block=False)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        elif msg['message_type'] == RBMQ_run_status:
            logging.debug("[Consumer] setting run_status: " +
                          str(msg['body']['run_status']))
            self.run_status_callback(msg['body']['run_status'])
            ch.basic_ack(delivery_tag=method.delivery_tag)

        else:
            logging.error(f"Failed to match message type")

    def start(self):
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.__callback)
        try:
            logging.info("[Consumer] Starting rabbitmq consumer")
            self.channel.start_consuming()
        except Exception as e:
            logging.error(f"[Consumer] Error starting rabbitmq consumer: {e}")
            self.stop(e)

    def stop(self, err=None):
        logging.info("[Consumer] Stopping rabbitmq consumer: " + str(err))
        if self.channel.is_open:
            self.channel.close()
        if self.conn.is_open:
            self.conn.close()
        return

    def spawn_consumer_thread(self):
        print("Starting Consumer")
        t = ConsumerThread(target=self.start, callback=self.stop, daemon=True)
        t.start()
        return t


class ConsumerThread(Thread):
    def __init__(self, callback=None, *args, **keywords):
        Thread.__init__(self, *args, **keywords)
        self.callback = callback
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                return SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True
