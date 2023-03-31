Тестовое задание:
Необходимо создать веб сервис с использованием любого асинхронного фрейморка, в котором будут реализованы следующие ендпоинты:

POST: /save_user_data
data:

*name - Строка не более 50 символов длиной

*surname - Строка не более 50 символов длиной

patronymic (отчество) - Опциональное поле не более 50 символов длинной

*phone_number - Строка, принимает на вход только номера начинающиеся с 7 email - Опциональное поле
*country - Строка не более 50 символов длинной

*- обязательное поле

Для полей ФИО и страны должно быть ограничение по допустимым символам (разрешены только кирилица, пробельный символ и тире).

Помимо этого требуется генерировать и сохранять следующие поля:

user_id - Строковый идентификатор пользователя длиной 12 символов date_created - Дата добавления данных нового пользователя date_modified - Дата последнего обновления данных.
Если в бд уже существуют данные от этого пользователя, то их следует обновить.

POST: /get_user_data
data:

*phone_number

Должен по номеру телефона вернуть следующие данные: name
surname patronymic phone_number
email (при отсутствии вернется None) country
country_code (смотреть описание ниже)

Если данный номер телефона не найден, то в ответ отправляем 404 статус.

POST: /delete_user_data
data:

*phone_number

По номеру телефона удаляет данные пользователя в бд.

При получении от клиента данных о стране сервис должен отправить запрос в dadata на нужный ендпоинт (https://dadata.ru/suggestions/outward/country/) для получения цифрового кода страны. Для экономии запросов отправляемых в сервис нужно кешировать полученный от сервиса ответ на случай обращения другого клиента из той же страны.

Дополнительные требования к реализации:
Предполагается, что в будущем набор запрашиваемых от клиента полей будет расширен, как и получаемые от dadata данные, поэтому необходимо изначально закладывать архитектуру с расчетом на это.

Выбор базы данных (из следующих: PostgreSQL/MySQL/MongoDB) остается за исполнителем как и выбор хранилища для кеша.

Необходимо подготовить документацию в swagger. Сервис должен подниматься в докер контейнере. Наличие тестов к написанному коду.
Результатом выполнения задания должна быть ссылка на git репозиторий.
