# -*- coding: utf-8 -*-
from ApiLibrary import ApiLibrary


class ClientServicesException(Exception):
    pass


class Utils(object):

    @staticmethod
    def find_not_connected_service(client_id):
        """
        Метод для поиска и получения неподключенного клиентом сервиса.
        :param client_id: идентификатор клиента
        :return: dict {"service_id": <идентификатор_сервиса>,
                       "cost": <стоиомость_сервиса>}
        """
        # Call api to get all services and client services
        client_services = ApiLibrary.get_services_by_client_id(client_id)
        all_services = ApiLibrary.get_all_services()

        # Get items from services response
        client_items = Utils.get_services_items(client_services)
        all_items = Utils.get_services_items(all_services)

        # Get ids from items
        client_service_ids = Utils.get_ids(client_items)
        all_service_ids = Utils.get_ids(all_items)

        try:
            diff = set(all_service_ids).difference(client_service_ids)
            service_id = diff.pop()
            for item in all_items:
                if item['id'] == service_id:
                    return {"service_id": service_id,
                            "cost": item['cost']}
        except KeyError:
            raise ClientServicesException('Client has connected '
                                          'to all services.')

    @staticmethod
    def get_ids(services):
        """
        Метод для получения списка идентификаторов сервисов
        :param services: список сервисов
        :return: список идентификаторов сервисов
        """
        return [service.get('id') for service in services]

    @staticmethod
    def get_services_items(services):
        """
        Получние списка сервисов из ответа от сервера
        :param services: словарь, получаемый в результате ответа на запрос.
        :return: список сервисов
        """
        return services.get('items')
