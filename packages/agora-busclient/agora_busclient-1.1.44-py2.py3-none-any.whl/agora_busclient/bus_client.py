import json
from agora_config import config
from agora_logging import logger
from .messages import IoDataReportMsg, MessageEncoder, RequestMsg, MessageHeader, EventMsg
from .mqtt_client import MqttClient
from .base_mqtt_client import BaseMqttClient


class BusClientSingleton:
    _instance = None
    """
    Connects to the mqtt-net-server and handles sending and receiving messages
    """
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.subscriptions = set()
        self.bus = BaseMqttClient()
        config.observe("AEA2:BusClient", self.reconnect)

    @property
    def messages(self):
        return self.bus.messages

    def connect(self, sec: float):
        if config["AEA2:BusClient:Mock"] == "True":
            logger.info("Mocking BusClient based upon configuration settings 'AEA2:BusClient:Mock'")
            self.bus = BaseMqttClient()
        else:
            self.bus = MqttClient()
        self.bus.configure()
        self.bus.log_config()
        logger.info("bus_client connecting")
        self.bus.connect(sec)
        if self.is_connected():
            logger.info("bus_client connected")

    def disconnect(self):
        if self.bus.is_connected():
            self.bus.disconnect()

    def reconnect(self, _ = None):
        logger.info(f"BusClient: Received new configuration - reconnecting")
        self.disconnect()
        self.connect(3)

    def is_connected(self):
        return self.bus.is_connected()

    def send_message(self, topic, header: MessageHeader, payload):
        if not self.bus.is_connected():
            logger.error(
                "Cannot send message, BusClient is not connected to the broker")
            return
        headerJson = json.dumps(header, cls=MessageEncoder)
        payload_str = json.dumps(payload)
        if payload_str[0] is not '"':
            payload_str = json.dumps(payload_str)
        message = f"""{{
            "header": {headerJson},
            "payload": {payload_str}
        }}"""
        self.bus.send_message(topic, message)

    def send_raw_message(self, topic, payload):
        if not self.bus.is_connected():
            logger.error(
                "Cannot send message, BusClient is not connected to the broker")
            return
        self.bus.send_message(topic, payload)

    def send_data(self, msg: IoDataReportMsg, msgTopic="DataOut"):
        payload = json.dumps(msg, cls=MessageEncoder)
        self.send_raw_message(msgTopic, payload)

    def send_request(self, msg: RequestMsg, msgTopic="RequestOut") -> int:
        payload = json.dumps(msg, cls=MessageEncoder)
        self.send_raw_message(msgTopic, payload)
        return msg.header.MessageID
    
    def send_event(self, msg: EventMsg, msgTopic="EventOut") -> int:
        payload = json.dumps(msg, cls=MessageEncoder)
        self.send_raw_message(msgTopic, payload)
        return msg.EventId

    def configure(self):
        self.bus.configure()


bus_client = BusClientSingleton()
