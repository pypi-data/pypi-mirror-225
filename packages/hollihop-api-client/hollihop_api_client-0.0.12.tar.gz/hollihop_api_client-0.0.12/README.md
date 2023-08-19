HolliHop API Client

Python библиотека предназначенная для интеграции с CRM HolliHop через её [REST-API](https://support.holyhope.ru/knowledge_base/item/234610?sid=42435). Чтобы воспользоваться библиотекой нужно указать субдомен школы использующей CRM и ключ доступ к API.

## Установка

```shell
pip install hollihop-api-client
```

## Использование

### Инициализация

```python
from hollihop_api_client import HolliHopAPI

hh_api = HolliHopAPI(HH_DOMAIN, HH_COMMON_API_KEY)
```

Обратите внимание, что ключи нужно получать из переменных среды:

```python
from os import environ

HH_DOMAIN = environ['HH_DOMAIN']
HH_COMMON_API_KEY = environ['HH_COMMON_API_KEY']
```

### Запрос доступных локаций

```python
locations = hh_api.locations.get_locations() #метод возвращает все доступные локации
location = hh_api.locations.get_locations(id=1) #метод возвращает данные для локации с указанным в аргументе id
location = hh_api.locations.get_locations(name='Test') #метод возвращает данные для локации с указанным именем в аргументе name
```

## Ниже по ссылкам доступны описания всех доступных методов

[locations](method_decriptions/locations.md)
[offices](method_decriptions/offices.md)
[leads](method_decriptions/leads.md)
[ed_units](method_decriptions/ed_units.md)
[ed_unit_students](method_decriptions/ed_unit_students.md)
