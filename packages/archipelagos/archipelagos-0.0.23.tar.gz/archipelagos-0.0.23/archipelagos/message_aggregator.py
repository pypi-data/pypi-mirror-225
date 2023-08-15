"""
Consumes messages published on a MQTT topic on an MQTT Broker and writes the message to Apache Kafka.
"""
from __future__ import annotations

from archipelagos.server.platform import StartupError, ExitCodes, ComponentNames, AlertProvider
from archipelagos.server.config import ConfigurationFileUtils
from archipelagos.common.settings import SettingsFile
from archipelagos.server import setup_logging

from paho.mqtt.client import Client, MQTTMessage, Properties, MQTT_ERR_SUCCESS, MQTTv311
from confluent_kafka.admin import AdminClient, NewTopic, KafkaError
from paho.mqtt.reasoncodes import ReasonCodes
from typing import Any, List, Tuple, Dict
from confluent_kafka import Producer
from json import JSONDecodeError
from paho import mqtt
import datetime
import socket
import time
import json
import sys
import os


class MessageAggregator:
    """
    Entry point for the Message Aggregator component.
    """
    # Objects used when reading settings files or logging

    COMPONENT_NAME = ComponentNames.MESSAGE_AGGREGATOR
    CONFIGURATION_FILENAME = COMPONENT_NAME.lower().replace(" ", "-") + ".settings"
    LOG_FILENAME = "logs/" + COMPONENT_NAME.replace(" ", "-") + ".log"
    LOGGER = setup_logging(LOG_FILENAME)
    COMPONENT = None

    # Constants during processing MQTT messages

    _MQTT_VERSION = MQTTv311
    _SUBSCRIPTION_MAP = "subscription_mapping"

    # Constants useful when interacting with Kafka

    _MESSAGE_KEY_PREFIX = str(os.getpid()) + socket.gethostname()
    _SECURITY_PROTOCOL = 'security.protocol'
    _SASL_SSL = 'SASL_SSL'
    _SASL_MECHANISMS = 'sasl.mechanisms'
    _PLAIN = 'PLAIN'
    _SASL_USERNAME = 'sasl.username'
    _SASL_PASSWORD = 'sasl.password'
    _BOOTSTRAP_SERVERS = "bootstrap.servers"
    _RECONNECT_BACKOFF_MILLISECOND = "reconnect.backoff.ms"
    _RECONNECT_BACKOFF_MAX_MILLISECOND = "reconnect.backoff.max.ms"
    _RECONNECT_BACKOFF_MILLISECOND_DEFAULT = 50
    _RECONNECT_BACKOFF_MAX_MILLISECOND_DEFAULT = 1_000 * 10
    _DEFAULT_PARTITIONS = 2
    _DEFAULT_REPLICATION = 2

    @staticmethod
    def start():
        """
        Start the component.
        """
        try:
            MessageAggregator.LOGGER.info(f"Starting the {MessageAggregator.COMPONENT_NAME}.")

            MessageAggregator.COMPONENT = MessageAggregator.create()
            MessageAggregator.COMPONENT.run()

        except StartupError as se:
            MessageAggregator.LOGGER.exception(f"An exception was thrown when starting the {MessageAggregator.COMPONENT_NAME}.")
            sys.exit(se.exit_code)
        except:
            MessageAggregator.LOGGER.exception(f"An exception was thrown when starting the {MessageAggregator.COMPONENT_NAME}.")
            sys.exit(ExitCodes.UNDETERMINED_STARTUP_ERROR)

    @staticmethod
    def stop():
        """
        Stop the component.
        """
        try:
            if MessageAggregator.COMPONENT is not None:
                MessageAggregator.COMPONENT.close()
        except Exception:
            MessageAggregator.LOGGER.exception(f"An exception was thrown when stopping the {MessageAggregator.COMPONENT_NAME}.")
        finally:
            MessageAggregator.COMPONENT = None

        sys.exit(ExitCodes.SUCCESSFUL_EXECUTION)

    @staticmethod
    def create() -> MessageAggregator:
        """
        Create an instance of the component.

        :return: The component, or None if it could not be created (e.g. due to incorrect configuration).
        :rtype: DataService
        """
        # Find the configuration file

        configuration_file = SettingsFile.locate(MessageAggregator.CONFIGURATION_FILENAME, ".")
        configuration_settings = configuration_file.settings

        # Obtain the username and password for the MQTT broker

        mqtt_username = ConfigurationFileUtils.get_mqqt_broker_username(MessageAggregator.LOGGER, configuration_settings)
        mqtt_password = ConfigurationFileUtils.get_mqqt_broker_password(MessageAggregator.LOGGER, configuration_settings)

        # Obtain the URL and port for the MQTT broker

        mqtt_cluster_url = ConfigurationFileUtils.get_mqqt_broker_url(MessageAggregator.LOGGER, configuration_settings)
        mqtt_cluster_port = ConfigurationFileUtils.get_mqqt_broker_port(MessageAggregator.LOGGER, configuration_settings)

        # Obtain the number of seconds that a keep alive check should be made with the MQTT broker

        mqtt_keep_alive = ConfigurationFileUtils.get_mqqt_keep_alive(MessageAggregator.LOGGER, configuration_settings)

        # Obtain the MQTT client ID

        mqtt_client_id = ConfigurationFileUtils.get_mqqt_client_id(MessageAggregator.LOGGER, configuration_settings)

        # Obtain the MQTT topic subscription details and the QoS to use

        mqtt_topic = ConfigurationFileUtils.get_mqqt_topic(MessageAggregator.LOGGER, configuration_settings)
        mqtt_qos = ConfigurationFileUtils.get_mqqt_qos(MessageAggregator.LOGGER, configuration_settings)

        # Obtain the Kafka credentials

        kafka_username = ConfigurationFileUtils.get_kafka_username(MessageAggregator.LOGGER, configuration_settings)
        kafka_password = ConfigurationFileUtils.get_kafka_password(MessageAggregator.LOGGER, configuration_settings)

        # Obtain the Kafka servers and topic

        kafka_servers = ConfigurationFileUtils.get_kafka_servers(MessageAggregator.LOGGER, configuration_settings)
        kafka_topic = ConfigurationFileUtils.get_kafka_topic(MessageAggregator.LOGGER, configuration_settings)

        # Configure the alert provider

        alert_provider = AlertProvider(MessageAggregator.COMPONENT_NAME)

        # We have managed to obtain the required configuration so return an instance of this class

        return MessageAggregator(mqtt_username=mqtt_username,
                                 mqtt_password=mqtt_password,
                                 mqtt_cluster_url=mqtt_cluster_url,
                                 mqtt_cluster_port=mqtt_cluster_port,
                                 mqtt_keep_alive=mqtt_keep_alive,
                                 mqtt_client_id=mqtt_client_id,
                                 mqtt_topic=mqtt_topic,
                                 mqtt_qos=mqtt_qos,
                                 kafka_username=kafka_username,
                                 kafka_password=kafka_password,
                                 kafka_servers=kafka_servers,
                                 kafka_topic=kafka_topic,
                                 alert_provider=alert_provider)

    def __init__(self,
                 mqtt_username: str,
                 mqtt_password: str,
                 mqtt_cluster_url: str,
                 mqtt_cluster_port: int,
                 mqtt_keep_alive: int,
                 mqtt_client_id: str,
                 mqtt_topic: str,
                 mqtt_qos: int,
                 kafka_username: str,
                 kafka_password: str,
                 kafka_servers: str,
                 kafka_topic: str,
                 alert_provider: AlertProvider):
        """
        :param mqtt_username: Username for MQTT broker.
        :type mqtt_username: str

        :param mqtt_password: Password for MQTT broker.
        :type mqtt_password: str

        :param mqtt_cluster_url: URL for MQTT broker.
        :type mqtt_cluster_url: str

        :param mqtt_cluster_port: Port for MQTT broker.
        :type mqtt_cluster_port: int

        :param mqtt_keep_alive: Number of seconds between when keep alive check are made to the MQTT broker.
        :type mqtt_keep_alive: int

        :param mqtt_client_id: .
        :type mqtt_client_id: str

        :param mqtt_topic: MQTT topic subscription details.
        :type mqtt_topic: str

        :param mqtt_qos: MQTT QoS to use when subscribing to topics.
        :type mqtt_qos: int

        :param kafka_username: Username to use when connecting to Kafka; None if no username should be used (such as when testing).
        :type kafka_username: str

        :param kafka_password: Password to use when connecting to Kafka; None if no password should be used (such as when testing).
        :type kafka_password: str

        :param kafka_servers: Comma separated list of URLs:ports for the Kafka brokers to connect to.
        :type kafka_servers: str

        :param kafka_topic: Topic on which to publish messages.
        :type kafka_topic: str

        :param alert_provider: The alert provider to use.
        :type alert_provider: AlertProvider
        """
        self._mqtt_username = mqtt_username
        self._mqtt_password = mqtt_password
        self._mqtt_cluster_url = mqtt_cluster_url
        self._mqtt_cluster_port = mqtt_cluster_port
        self._mqtt_keep_alive = mqtt_keep_alive
        self._mqtt_client_id = mqtt_client_id
        self._mqtt_topic = mqtt_topic
        self._mqtt_qos = mqtt_qos

        self._kafka_username = kafka_username
        self._kafka_password = kafka_password
        self._kafka_servers = kafka_servers
        self._kafka_topic = kafka_topic

        self._alert_provider = alert_provider

        self._connected = False
        self._mqtt_client = None
        self._kafka_producer = None

    @staticmethod
    def _on_connect(client: Client,
                    user_data: Any,
                    flags: Dict[str, Any],
                    result_code: int):
        """
        Called when a client is connected.

        :param client: Client associated with the callback.
        :type client: Client

        :param user_data: User data set in Client() or userdata_set(), or None if no such data was provided.
        :type user_data: Any

        :param user_data: User data set in Client() or userdata_set(), or None if no such data was provided.
        :type user_data: Any

        :param flags: Contains response flags from the broker (flags['session present'] is useful for clients that are using clean session set to 0 only; if a client with clean session=0 that reconnects to a broker that it has previously connected to, this flag indicates whether the broker still has the session information for the client. If 1, the session still exists)..
        :type flags: Dict[str, Any]

        :param result_code: Result code; int for MQTT 3.1.1 (0: connection successful, 1: incorrect protocol version, 2: invalid client identifier, 3: server unavailable, 4: bad username or password, 5: not authorised, 6-255: currently unused).
        :type result_code: ReasonCodes or int
        """
        if result_code == 0:
            client.connected_flag = True
            MessageAggregator.LOGGER.info(f"Successful MQTT broker connection request acknowledged with result code '{result_code}'.")
        else:
            client.connected_flag = False
            MessageAggregator.LOGGER.info(f"Unsuccessful MQTT broker connection request acknowledged with result code '{result_code}'.")

    @staticmethod
    def _on_disconnect(client: Client,
                       user_data: Any,
                       result_code: ReasonCodes or int):
        """
        Called when a client is disconnected.

        :param client: Client associated with the callback.
        :type client: Client

        :param user_data: User data set in Client() or userdata_set(), or None if no such data was provided.
        :type user_data: Any

        :param user_data: User data set in Client() or userdata_set(), or None if no such data was provided.
        :type user_data: Any

        :param result_code: Result code; int for MQTT 3.1.1 (0: connection successful, 1: incorrect protocol version, 2: invalid client identifier, 3: server unavailable, 4: bad username or password, 5: not authorised, 6-255: currently unused).
        :type result_code: ReasonCodes or int
        """
        client.connected_flag = False

        if result_code != 0:
            MessageAggregator.LOGGER.info(f"Unexpected MQTT broker disconnection event published with result code '{result_code}'.")
        else:
            MessageAggregator.LOGGER.info(f"Graceful MQTT broker disconnection event published with result code '{result_code}'.")

    @staticmethod
    def _reconnect():
        """
        Called when a client is disconnected.
        """
        MessageAggregator.LOGGER.info(f"Reconnected.")

    @staticmethod
    def _on_subscribe(client: Client,
                      user_data: Any,
                      message_id: int,
                      granted_qos: Tuple[int] or List[ReasonCodes],
                      properties: Properties = None):
        """
        Called when a client has subscribed to a topic.

        :param client: Client associated with the callback.
        :type client: Client

        :param user_data: User data set in Client() or userdata_set(), or None if no such data was provided.
        :type user_data: Any

        :param message_id: Matches the message ID returned from the corresponding call to subscribe().
        :type message_id: int

        :param granted_qos: Information regarding the quality of service granted by the MQTT broker; Tuple[int] for MQTT 3.1.1.
        :type granted_qos: Tuple[int] or List[ReasonCodes]

        :param properties: MQTT 5.0 properties received from the broker; will be None if MQTT 3.1.1 is used.
        :type properties: Properties
        """
        # Obtain the subscription details associated with the message ID

        topic, qos = user_data[MessageAggregator._SUBSCRIPTION_MAP][message_id]

        # Display the subscription details

        MessageAggregator.LOGGER.info(f"MQTT broker reported that client subscribed to topic '{topic}' with QoS {qos}.")

    @staticmethod
    def _inspect_json(json_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inspects a given message from the MQTT broker and decides if it should be published.

        :param json_data: JSON to publish.
        :type json_data: Dict[str, Any]

        :return: JSON to publish or None if json_data should not be published.
        :rtype: Dict[str, Any] or None
        """
        return json_data

    @staticmethod
    def _publish_message(json_data: Dict[str, Any]) -> bool:
        """
        Publishes a given message to Kafka (if valid).

        :param json_data: JSON to publish.
        :type json_data: Dict[str, Any]

        :return: True if a message was valid and was published, False if it was not valid (an error will be thrown if it could not be published).
        :rtype: bool
        """
        # Evaluate if the message was valid

        json_to_publish = MessageAggregator._inspect_json(json_data=json_data)

        if json_to_publish is None:
            return False
        else:
            # Partition key is used by Kinesis when you have multiple shards to determine which shard to use

            timestamp = datetime.datetime.utcnow().isoformat()
            message_key = MessageAggregator._MESSAGE_KEY_PREFIX + timestamp

            MessageAggregator.COMPONENT.kafka_producer.produce(topic=MessageAggregator.COMPONENT.kafka_topic,
                                                               key=message_key,
                                                               value=json.dumps(json_data))
            return True

    @staticmethod
    def on_message(client: Client,
                   user_data: Any,
                   message: MQTTMessage):
        """
        Called when a message is received from a topic subscribed to by a client.

        :param client: Client associated with the callback.
        :type client: Client

        :param user_data: User data set in Client() or userdata_set().
        :type user_data: Any

        :param message: Message received.
        :type message: MQTTMessage
        """
        try:
            MessageAggregator.LOGGER.info(f"Consumed on the MQTT topic '{message.topic}' with QoS {message.qos} the message {message.payload}.")

            json_data = json.loads(message.payload)
            published = MessageAggregator._publish_message(json_data=json_data)

            if published:
                MessageAggregator.LOGGER.info(f"Published to the Kafka topic '{MessageAggregator.COMPONENT.kafka_topic}' the event {json_data}.")
            else:
                MessageAggregator.LOGGER.info(f"Did not publish to the Kafka topic '{MessageAggregator.COMPONENT.kafka_topic}' the event {message.payload} as the message received from MQTT was not considered valid.")
        except JSONDecodeError:
            MessageAggregator.LOGGER.info(f"Did not publish to the Kafka topic '{MessageAggregator.COMPONENT.kafka_topic}' the event {message.payload} as the message received from MQTT was not considered valid JSON.")
        except Exception as e:
            MessageAggregator.LOGGER.exception(f"Unable to publish to the Kafka topic '{MessageAggregator.COMPONENT.kafka_topic}' the event {message.payload}.\n\n", e)

    def run(self):
        """
        Run the services supported by the component.
        """
        # Create MQTT client

        client_user_data = {MessageAggregator._SUBSCRIPTION_MAP: {}}

        self._mqtt_client = Client(client_id=self._mqtt_client_id,
                                   clean_session=False,
                                   protocol=MessageAggregator._MQTT_VERSION,
                                   userdata=client_user_data)
        self._mqtt_client.username_pw_set(self._mqtt_username, self._mqtt_password)
        self._mqtt_client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self._mqtt_client.connected_flag = False

        # Set MQTT callback functions

        self._mqtt_client.on_connect = MessageAggregator._on_connect
        self._mqtt_client.on_disconnect = MessageAggregator._on_disconnect
        self._mqtt_client.on_subscribe = MessageAggregator._on_subscribe
        self._mqtt_client.on_message = MessageAggregator.on_message

        # Connect to MQTT cluster

        self._mqtt_client.loop()

        while not self._mqtt_client.connected_flag:
            try:
                self._mqtt_client.connect(host=self._mqtt_cluster_url, port=self._mqtt_cluster_port, keepalive=self._mqtt_keep_alive)
                self._mqtt_client.connected_flag = True
            except Exception as e:
                MessageAggregator.LOGGER.exception(f"Unable to connect to the MQTT broker; will try again in {self._mqtt_keep_alive} seconds.", e)
                time.sleep(self._mqtt_keep_alive)

        # Subscribe to the specified MQTT topic

        error_code, subscription_message_id = self._mqtt_client.subscribe(topic=self._mqtt_topic, qos=self._mqtt_qos)

        if error_code == MQTT_ERR_SUCCESS:
            # Store the mapping from message ID to topic and QoS so that it can be used in callbacks

            client_user_data[MessageAggregator._SUBSCRIPTION_MAP][subscription_message_id] = [self._mqtt_topic, self._mqtt_qos]

            # If necessary, create the Kafka topic

            try:
                admin_client = AdminClient({MessageAggregator._BOOTSTRAP_SERVERS: self._kafka_servers})
                topic_list = [NewTopic(self._kafka_topic, MessageAggregator._DEFAULT_PARTITIONS, MessageAggregator._DEFAULT_REPLICATION)]
                futures = admin_client.create_topics(topic_list)
                future = futures[self._kafka_topic]

                if not future.cancelled():
                    exception = future.exception()

                    if exception is None:
                        future.result()
                    else:
                        error = exception.args[0]
                        code = error.code()

                        if code != KafkaError.TOPIC_ALREADY_EXISTS:
                            raise StartupError(f"Unable to create the Kafka topic '{self._kafka_topic}'.", ExitCodes.COULD_NOT_CONNECT_TO_KAFKA, error)
            except Exception as e:
                raise StartupError(f"Unable to create the Kafka topic '{self._kafka_topic}'.", ExitCodes.COULD_NOT_CONNECT_TO_KAFKA, e)

            # Create the Kafka producer

            config = {MessageAggregator._BOOTSTRAP_SERVERS: self._kafka_servers,
                      MessageAggregator._RECONNECT_BACKOFF_MILLISECOND: MessageAggregator._RECONNECT_BACKOFF_MILLISECOND_DEFAULT,
                      MessageAggregator._RECONNECT_BACKOFF_MAX_MILLISECOND: MessageAggregator._RECONNECT_BACKOFF_MAX_MILLISECOND_DEFAULT}

            if self._kafka_username is not None and self._kafka_password is not None:
                config[MessageAggregator._SECURITY_PROTOCOL] = MessageAggregator._SASL_SSL
                config[MessageAggregator._SASL_MECHANISMS] = MessageAggregator._PLAIN
                config[MessageAggregator._SASL_USERNAME] = self._kafka_username
                config[MessageAggregator._SASL_PASSWORD] = self._kafka_password

            self._kafka_producer = Producer(config)

            # Loop forever; can also use loop_start and loop_stop

            self._mqtt_client.loop_forever()
        else:
            # As we could not subscribe exit and report issue

            raise ValueError(f"Not subscribed to topic '{self._mqtt_topic}' with QoS {self._mqtt_qos}; error code {error_code}.")

        # All looks good, so now wait for requests

        self._connected = True

    def close(self):
        """
        Disconnect from the database etc.
        """
        if self._connected:
            # Stop the MQTT client

            try:
                self._mqtt_client.close()
            except Exception:
                MessageAggregator.LOGGER.exception("An exception was thrown when shutting down the MQTT client.")

            # Flush the Kafka producer

            try:
                self._kafka_producer.flush()
            except Exception:
                MessageAggregator.LOGGER.exception("An exception was thrown when flushing the Kafka producer.")

    @property
    def alert_provider(self) -> AlertProvider:
        """
        AlertProvider associated with this.
        """
        return self._alert_provider

    @property
    def kafka_topic(self) -> str:
        """
        Kafka topic on which to publish messages.
        """
        return self._kafka_topic

    @property
    def kafka_producer(self) -> str:
        """
        Kafka producer to use.
        """
        return self._kafka_producer


if __name__ == "__main__":
    MessageAggregator.start()
