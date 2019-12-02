# Задание 9.2

Переписанный сервер из задания 8.3 с добавлением базы данных и логированием.

## Описание 

Залогировано на уровне debug обращения к кешу и к базе. Если данных нет в кеше, то это логируется на уровне WARNING. Если данных нет в базе то это логируется на уровне ERROR.

Например:

```
2019-11-03 19:28:48,040 - DEBUG - hw8mrl.storage - get for key [8]
2019-11-03 19:28:48,040 - WARNING - hw8mrl.storage - no data in cache for key [8]
2019-11-03 19:28:48,041 - ERROR - hw8mrl.storage - no data in database for key [8]
```

Логгер берет конфигурацию из файла ```log.conf```.

## Имеющиеся файлы

- Dockerfile 

- docker-compose.yaml

- server.py

- log.conf

- unittest.py