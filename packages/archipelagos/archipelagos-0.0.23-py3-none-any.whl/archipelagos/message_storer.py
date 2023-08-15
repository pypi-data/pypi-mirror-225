"""
Consumes messages published on an AWS Kinesis stream and writes the message to MongoDB.
"""
from __future__ import annotations

from archipelagos.server.platform import StartupError, ExitCodes, ComponentNames, AlertProvider
from archipelagos.server.database import MongoDatabaseManager, DatabaseConnectionDetails
from archipelagos.server.config import ConfigurationFileUtils
from archipelagos.common.settings import SettingsFile
from archipelagos.server import setup_logging

from confluent_kafka.admin import AdminClient, NewTopic, KafkaError
from typing import Dict, Any, Tuple, List
from confluent_kafka import Consumer
from datetime import datetime
from io import BytesIO
import socket
import json
import sys
import os


class MessageStorer:
    """
    Entry point for the Message Storer component.
    """
    # Objects used when reading settings files or logging

    COMPONENT_NAME = ComponentNames.MESSAGE_STORER
    CONFIGURATION_FILENAME = COMPONENT_NAME.lower().replace(" ", "-") + ".settings"
    LOG_FILENAME = "logs/" + COMPONENT_NAME.replace(" ", "-") + ".log"
    LOGGER = setup_logging(LOG_FILENAME)
    COMPONENT = None

    # Constants useful when processing records data or using MongoDB

    _CREATE = "create"
    _GRANULARITY = 'granularity'
    _META_FIELD = 'metaField'
    _MINUTES_GRANULARITY = "minutes"
    _NAME = 'name'
    _PAYLOAD = 'payload'
    _PUBLISHER = 'publisher'
    _TIMESERIES = 'timeseries'
    _TIMESTAMP = 'timestamp'
    _TIME_FIELD = "timeField"
    _TOPIC = 'topic'

    # Constants useful when interacting with Kafka

    _MESSAGE_KEY_PREFIX = str(os.getpid()) + socket.gethostname()
    _AUTO_OFFSET_RESET = 'auto.offset.reset'
    _EARLIEST = 'earliest'
    _SECURITY_PROTOCOL = 'security.protocol'
    _SASL_SSL = 'SASL_SSL'
    _SASL_MECHANISMS = 'sasl.mechanisms'
    _PLAIN = 'PLAIN'
    _SASL_USERNAME = 'sasl.username'
    _SASL_PASSWORD = 'sasl.password'
    _BOOTSTRAP_SERVERS = "bootstrap.servers"
    _LATEST = "latest"
    _GROUP_ID = "group.id"
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
            MessageStorer.LOGGER.info(f"Starting the {MessageStorer.COMPONENT_NAME}.")

            MessageStorer.COMPONENT = MessageStorer.create()
            MessageStorer.COMPONENT.run()

        except StartupError as se:
            MessageStorer.LOGGER.exception(f"An exception was thrown when starting the {MessageStorer.COMPONENT_NAME}.")
            sys.exit(se.exit_code)
        except:
            MessageStorer.LOGGER.exception(f"An exception was thrown when starting the {MessageStorer.COMPONENT_NAME}.")
            sys.exit(ExitCodes.UNDETERMINED_STARTUP_ERROR)

    @staticmethod
    def stop():
        """
        Stop the component.
        """
        try:
            if MessageStorer.COMPONENT is not None:
                MessageStorer.COMPONENT.close()
        except Exception:
            MessageStorer.LOGGER.exception(f"An exception was thrown when stopping the {MessageStorer.COMPONENT_NAME}.")
        finally:
            MessageStorer.COMPONENT = None

        sys.exit(ExitCodes.SUCCESSFUL_EXECUTION)

    @staticmethod
    def create() -> MessageStorer:
        """
        Create an instance of the component.

        :return: The component, or None if it could not be created (e.g. due to incorrect configuration).
        :rtype: DataService
        """
        # Find the configuration file

        configuration_file = SettingsFile.locate(MessageStorer.CONFIGURATION_FILENAME, ".")
        configuration_settings = configuration_file.settings

        # Obtain the Kafka credentials

        kafka_username = ConfigurationFileUtils.get_kafka_username(MessageStorer.LOGGER, configuration_settings)
        kafka_password = ConfigurationFileUtils.get_kafka_password(MessageStorer.LOGGER, configuration_settings)

        # Obtain the Kafka servers and topic

        kafka_servers = ConfigurationFileUtils.get_kafka_servers(MessageStorer.LOGGER, configuration_settings)
        kafka_topic = ConfigurationFileUtils.get_kafka_topic(MessageStorer.LOGGER, configuration_settings)

        # Obtain if the earliest data stored from the Kafka topic should be read or not

        kafka_read_earliest = ConfigurationFileUtils.get_kafka_read_earliest(MessageStorer.LOGGER, configuration_settings)

        # Obtain the Kafka consumer group ID to use

        kafka_group_id = ConfigurationFileUtils.get_kafka_consumer_group_id(MessageStorer.LOGGER, configuration_settings)

        # Create the object holding the details of the database to connect to (but do not yet connect)

        database_details = ConfigurationFileUtils.get_database_connection_details(MessageStorer.LOGGER, configuration_settings)

        # Obtain the name of the database collection in which to store the records published on the AWS Kinesis stream

        database_collection = ConfigurationFileUtils.get_database_collection(MessageStorer.LOGGER, configuration_settings)

        # Configure the alert provider

        alert_provider = AlertProvider(MessageStorer.COMPONENT_NAME)

        # We have managed to obtain the required configuration so return an instance of this class

        return MessageStorer(kafka_username=kafka_username,
                             kafka_password=kafka_password,
                             kafka_servers=kafka_servers,
                             kafka_topic=kafka_topic,
                             kafka_read_earliest=kafka_read_earliest,
                             kafka_group_id=kafka_group_id,
                             database_details=database_details,
                             database_collection=database_collection,
                             alert_provider=alert_provider)

    def __init__(self,
                 kafka_username: str,
                 kafka_password: str,
                 kafka_servers: str,
                 kafka_topic: str,
                 kafka_read_earliest: bool,
                 kafka_group_id: str,
                 database_details: DatabaseConnectionDetails,
                 database_collection: str,
                 alert_provider: AlertProvider):
        """
        :param kafka_username: Username to use when connecting to Kafka; None if no username should be used (such as when testing).
        :type kafka_username: str

        :param kafka_password: Password to use when connecting to Kafka; None if no password should be used (such as when testing).
        :type kafka_password: str

        :param kafka_servers: Comma separated list of URLs:ports for the Kafka brokers to connect to.
        :type kafka_servers: str

        :param kafka_topic: Topic on which to publish messages.
        :type kafka_topic: str

        :param kafka_read_earliest: True if the earliest data stored from the topic should be read, False for the data published after a component is started.
        :type kafka_read_earliest: bool

        :param kafka_group_id: Kafka consumer group ID to use.
        :type kafka_group_id: str

        :param database_details: Details of the database to connect to.
        :type database_details: DatabaseConnectionDetails

        :param database_collection: Name of database collection to store the data in.
        :type database_collection: str

        :param alert_provider: The alert provider to use.
        :type alert_provider: AlertProvider
        """
        self._kafka_username = kafka_username
        self._kafka_password = kafka_password
        self._kafka_servers = kafka_servers
        self._kafka_topic = kafka_topic
        self._kafka_read_earliest = kafka_read_earliest
        self._kafka_group_id = kafka_group_id

        self._database_details = database_details
        self._database_collection = database_collection

        self._kafka_consumer = None
        self._database_manager = None

        self._alert_provider = alert_provider
        self._connected = False

    @staticmethod
    def _is_valid_record(record_to_check: Dict[str, Any]) -> Tuple[bool, Dict[str, Any] or None]:
        """
        Determines if a given record retrieved from a stream is considered valid.

        :param record_to_check: Record retrieved from a stream to check.
        :type record_to_check: Dict[str, Any]

        :return: Tuple where the 1st element is True if record_to_check is valid, False otherwise; if 1st element is True the 2nd element is the parsed record, None otherwise.
        :rtype: Tuple[bool, Dict[str, Any] or None]
        """
        if isinstance(record_to_check, dict):
            if all([isinstance(key, str) for key in record_to_check.keys()]):
                if MessageStorer._TIMESTAMP in record_to_check and MessageStorer._TOPIC in record_to_check and MessageStorer._PUBLISHER in record_to_check and MessageStorer._PAYLOAD in record_to_check:
                    # Obtain required data

                    timestamp = record_to_check[MessageStorer._TIMESTAMP]
                    topic = record_to_check[MessageStorer._TOPIC]
                    publisher = record_to_check[MessageStorer._PUBLISHER]
                    payload = record_to_check[MessageStorer._PAYLOAD]

                    # Determine if required data looks valid

                    try:
                        timestamp = datetime.fromisoformat(timestamp)

                        if isinstance(topic, str) and isinstance(publisher, str) and isinstance(payload, dict):
                            if all([isinstance(key, str) for key in payload.keys()]):
                                parsed_record = {MessageStorer._TIMESTAMP: timestamp,
                                                 MessageStorer._TOPIC: topic,
                                                 MessageStorer._PUBLISHER: publisher,
                                                 MessageStorer._PAYLOAD: payload}

                                return True, parsed_record
                            else:
                                return False, None
                        else:
                            return False, None
                    except:
                        return False, None
                else:
                    return False, None
            else:
                return False, None
        else:
            return False, None

    def _process_records(self,
                         records: List[Dict[str, Any]]):
        """
        Store a set of records published on Kinesis into MongoDB.

        :param records: Records to process.
        :type records: List[Dict[str, Any]]
        """
        filters = []
        documents = []
        messages = []

        for record_to_process in records:
            # Get the required fields

            timestamp = record_to_process.get(MessageStorer._TIMESTAMP)
            publisher = record_to_process.get(MessageStorer._PUBLISHER)
            topic = record_to_process.get(MessageStorer._TOPIC)
            payload = record_to_process.get(MessageStorer._PAYLOAD)

            # Build the documents and store

            filters.append({MessageStorer._TIMESTAMP: timestamp,
                            MessageStorer._PUBLISHER: publisher,
                            MessageStorer._TOPIC: topic})

            documents.append({MessageStorer._TIMESTAMP: timestamp,
                              MessageStorer._PUBLISHER: publisher,
                              MessageStorer._TOPIC: topic,
                              MessageStorer._PAYLOAD: payload})

            # Generate the logging messages

            message = f"Stored in the database an event published by '{publisher}' on the Kafka topic '{topic}' at '{timestamp}' containing the payload {payload}."
            messages.append(message)

        self._database_manager.store_unique_documents(collection_name=self._database_collection, filters=filters, documents=documents, logger=MessageStorer.LOGGER, messages=messages)

    def run(self):
        """
        Run the services supported by the component.
        """
        # If necessary, create the Kafka topic

        try:
            admin_client = AdminClient({MessageStorer._BOOTSTRAP_SERVERS: self._kafka_servers})
            topic_list = [NewTopic(self._kafka_topic, MessageStorer._DEFAULT_PARTITIONS, MessageStorer._DEFAULT_REPLICATION)]
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

        # Create the Kafka consumer

        try:
            config = {MessageStorer._BOOTSTRAP_SERVERS: self._kafka_servers,
                      MessageStorer._GROUP_ID: self._kafka_group_id,
                      MessageStorer._RECONNECT_BACKOFF_MILLISECOND: MessageStorer._RECONNECT_BACKOFF_MILLISECOND_DEFAULT,
                      MessageStorer._RECONNECT_BACKOFF_MAX_MILLISECOND: MessageStorer._RECONNECT_BACKOFF_MAX_MILLISECOND_DEFAULT}

            if self._kafka_username is not None and self._kafka_password is not None:
                config[MessageStorer._SECURITY_PROTOCOL] = MessageStorer._SASL_SSL
                config[MessageStorer._SASL_MECHANISMS] = MessageStorer._PLAIN
                config[MessageStorer._SASL_USERNAME] = self._kafka_username
                config[MessageStorer._SASL_PASSWORD] = self._kafka_password

            if self._kafka_read_earliest:
                config[MessageStorer._AUTO_OFFSET_RESET] = MessageStorer._EARLIEST
            else:
                config[MessageStorer._AUTO_OFFSET_RESET] = MessageStorer._LATEST

            self._kafka_consumer = Consumer(config)
            self._kafka_consumer.subscribe(topics=[self._kafka_topic])

        except Exception as e:
            raise StartupError("Unable to create the Kafka consumer.", ExitCodes.COULD_NOT_CONNECT_TO_KAFKA, e)

        MessageStorer.LOGGER.info(f"Successfully created the Kafka consumer and subscribed to topic '{self._kafka_topic}'.")

        # Connect to the system database

        try:
            database_name = self._database_details.database_name
            cluster = self._database_details.cluster

            MessageStorer.LOGGER.info(f"Attempting to connect to the system database '{database_name}' located on the cluster '{cluster}'.")

            self._database_manager = MongoDatabaseManager(self._database_details, MessageStorer.LOGGER)
            self._database_manager.connect()

        except Exception as e:
            raise StartupError("Unable to connect to the database.", ExitCodes.COULD_NOT_CONNECT_TO_DATABASE, e)

        MessageStorer.LOGGER.info("Successfully connected to the system database.")

        # If required, create the database collection

        created_collection = self._database_manager.add_time_series_collection(collection=self._database_collection, granularity=MessageStorer._MINUTES_GRANULARITY)

        if created_collection:
            MessageStorer.LOGGER.info(f"Successfully created database collection '{self._database_collection}'.")
        else:
            MessageStorer.LOGGER.info(f"Database collection '{self._database_collection}' already existed so was not created.")

        # All looks good, so now wait for requests

        self._connected = True

        # Start consuming data from Kafka

        last_record_processed = {}
        keep_processing = True

        while keep_processing:
            try:
                # Inspect the available records in each shard in turn

                kafka_message = self._kafka_consumer.poll(1.0)

                if kafka_message is None:
                    # The initial message consumption may take up to `session.timeout.ms`
                    # so that the consumer group can first re-balance and start consuming
                    continue

                elif kafka_message.error():
                    error_object = kafka_message.error()
                    MessageStorer.LOGGER.error(f"An error was received when consuming an event on the Kafka topic '{self._kafka_topic}': '{error_object}'.")

                else:
                    data = kafka_message.value()
                    MessageStorer.LOGGER.info(f"On the Kafka topic '{kafka_message.topic()}' consumed the event {data}.")

                    # Check if the record is considered valid

                    if data is not None:
                        # Convert the data contained in the record to JSON

                        bytes_data = BytesIO(data)
                        json_data = json.load(bytes_data)

                        # If necessary, update our list of valid records

                        valid_record, record_parsed = self._is_valid_record(record_to_check=json_data)

                        if valid_record:
                            self._process_records(records=[record_parsed])

            except Exception as e:
                MessageStorer.LOGGER.exception(f"An exception occurred when attempting to consume and store records.", e)

        # Finished consuming messages so disconnect Kafka consumer

        try:
            self._kafka_consumer.close()
        except Exception:
            MessageStorer.LOGGER.exception("An exception was thrown when closing the Kafka consumer.")

    def close(self):
        """
        Disconnect from the database etc.
        """
        if self._connected:
            # Stop the Kafka consumer

            try:
                self._kafka_consumer.close()
            except Exception:
                MessageStorer.LOGGER.exception("An exception was thrown when closing the Kafka consumer.")

            # Stop the database manager

            try:
                self._database_manager.close()
            except Exception:
                MessageStorer.LOGGER.exception("An exception was thrown when closing the AWS Kinesis client.")

    @property
    def alert_provider(self) -> AlertProvider:
        """
        AlertProvider associated with this.
        """
        return self._alert_provider


if __name__ == "__main__":
    MessageStorer.start()
