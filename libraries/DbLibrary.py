# -*- coding: utf-8 -*-
import sqlite3
import time
import settings


class DbException(Exception):
    pass


class TimeoutException(Exception):
    pass


class DbLibrary(object):
    """
    Класс содержит методы для работы с базой данных
    """

    @staticmethod
    def get_client():
        """
        Метод повзоляет получить клиента с положительным балансом из бд
        :return: dict {"client_id": <идентификатор_клиента>,
                       "client_balance": <баланс_клиента>}
                None, если клиент не найден
        """
        query = """SELECT c.CLIENT_ID, b.BALANCE FROM CLIENTS as c, 
                           BALANCES as b 
                           WHERE b.BALANCE > 0 AND 
                           c.CLIENT_ID = b.CLIENTS_CLIENT_ID
                           ORDER BY RANDOM() LIMIT 1"""

        with sqlite3.connect(settings.DB_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            try:
                return {"client_id": result[0], "client_balance": result[1]}
            except (IndexError, TypeError):
                return None

    @staticmethod
    def add_client_with_balance(client_name, client_balance):
        """
        Метод позволяет добавить клиента и его баланс в базу данных
        :param client_name: имя клиента, string
        :param client_balance: баланс клиента, float
        :return: dict {"client_id": <идентификатор_клиента>,
                       "client_balance": <баланс_клиента>}
        """
        with sqlite3.connect(settings.DB_NAME) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO CLIENTS VALUES(null, "{client_name}");
                               """.format(client_name=client_name)
            cursor.execute(query)
            connection.commit()
            client_id = cursor.lastrowid
            if client_id:
                balance_query = """INSERT INTO BALANCES VALUES({client_id}, 
                                {client_balance});""".format(
                    client_id=client_id,
                    client_balance=client_balance)
                cursor.execute(balance_query)
                connection.commit()
                return {"client_id": client_id,
                        "client_balance": client_balance}
            else:
                raise DbException('Client was not create.')

    @staticmethod
    def get_client_balance(client_id):
        """
        Метод позволяет получить баланс клиента
        :param client_id: идентификатор клиента
        :return: баланс клиента
        """
        with sqlite3.connect(settings.DB_NAME) as connection:
            cursor = connection.cursor()
            query = """SELECT BALANCE from BALANCES
                                WHERE CLIENTS_CLIENT_ID={client_id}""".format(
                client_id=client_id)
            cursor.execute(query)
            result = cursor.fetchone()
            try:
                return result[0]
            except IndexError:
                raise DbException('Can not get client balance.')

    @staticmethod
    def check_client_service(client_id, service_id):
        """
        Метод проверяет, проверяет, добавился ли клиент в базу данных.
        Таймаут 1 минута.
        :param client_id: идентификатор_клиента
        :param service_id: идентификатор_сервиса
        """
        query = """SELECT * FROM SERVICES AS S INNER JOIN CLIENT_SERVICE AS CS
                ON S.SERVICE_ID = CS.SERVICES_SERVICE_ID 
                WHERE CLIENTS_CLIENT_ID = {client_id} AND 
                CS.SERVICES_SERVICE_ID = {service_id}""".format(
            client_id=client_id,
            service_id=service_id)
        with sqlite3.connect(settings.DB_NAME) as connection:
            cursor = connection.cursor()
            timeout = time.time() + 60
            while time.time() < timeout:
                cursor.execute(query)
                client_service = cursor.fetchone()
                if client_service:
                    return
                time.sleep(3)
            raise TimeoutException('Can not add service')

    @staticmethod
    def create_client_if_not_exist(client_name, balance):
        current_client = DbLibrary.get_client()
        if not current_client:
            return DbLibrary.add_client_with_balance(client_name, balance)
        else:
            return current_client
