CREATE TABLE users (
    user_id char(12) PRIMARY KEY,
    name varchar(50),
    surname varchar(50),
    patronymic varchar(50),
    phone_number varchar(20),
    email varchar(50),
    country varchar(50),
    date_created timestamp with time zone,
    date_modified timestamp with time zone
);