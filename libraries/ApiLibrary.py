# -*- coding: utf-8 -*-
import requests
import json
import settings


class ApiLibrary(object):
    """
    Класс содержит методы для работы с API
    """
    # Headers for request
    _HEADERS = {'content-type': 'application/json'}

    @staticmethod
    def get_services_by_client_id(client_id):
        """
        Возвращает сервисы клиента
        :param client_id: идентификатор клиента
        :return: dict. JSON со списком сервисов клиента
        """
        response = requests.post(
            url='{host}/client/services'.format(host=settings.HOST),
            data=json.dumps({"client_id": client_id}),
            headers=ApiLibrary._HEADERS)
        return response.json()

    @staticmethod
    def get_all_services():
        """
        Возвращает все доступные сервисы
        :return: dict. JSON со списком всех сервисов
        """
        response = requests.get(url='{host}/services'.format(
            host=settings.HOST), headers=ApiLibrary._HEADERS)
        return response.json()

    @staticmethod
    def add_service(client_id, service_id):
        """
        Метод для подключения клиенту сервиса
        :param client_id: идентификатор клиента
        :param service_id: идентификатор сервиса
        :return: string, возвращает строку со статусом о
        добавлении сервиса клиенту.
        """
        response = requests.post(
            url='{host}/client/add_service'.format(host=settings.HOST),
            data=json.dumps({"client_id": client_id,
                             "service_id": service_id}),
            headers=ApiLibrary._HEADERS)
        return response.text
