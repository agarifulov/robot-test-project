*** Settings ***
Library    ../libraries/DbLibrary.py
Library    ../libraries/ApiLibrary.py
Library    ../libraries/Utils.py
Library    Collections

*** Keywords ***
Get client with positive balance
    [Documentation]  Возвращает клиента с положительным балансом (при необходимости - создает)
    ${client}  Create client if not exist  John  ${5.0}
    ${initial_balance}  Get From Dictionary  ${client}  client_balance
    ${client_id}  Get from dictionary  ${client}  client_id
    [Return]  ${client_id}  ${initial_balance}

Find unconnected service
    [Documentation]  Возвращает неподключенный у клиента сервис и стоимость
    [Arguments]  ${client_id}
    ${service}  Find not connected service  ${client_id}
    ${cost}  Get from dictionary  ${service}  cost
    ${service_id}  Get from dictionary  ${service}  service_id
    [Return]  ${service_id}  ${cost}
