*** Settings ***
Resource   ../resources/resource.robot


*** Test Cases ***
Test client balance after connected service
    [Documentation]  Проверка баланса клиента после подключения сервиса
    ${client_id}  ${initial_balance}  Get Client with positive balance
    ${client_services}  Get services by client id  ${client_id}
    ${all_services}  Get all services
    ${service_id}  ${cost}  Find unconnected service  ${client_id}
    Add service  ${client_id}  ${service_id}
    Check client service  ${client_id}  ${service_id}
    ${current_balance}  Get client balance  ${client_id}
    ${expected_balance}  Evaluate  ${initial_balance} - ${cost}
    Should be equal as numbers  ${expected_balance}  ${current_balance}  Разница баланса до и после подключения услуги отличается от стоимости услуги  ${false}
