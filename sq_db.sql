CREATE TABLE IF NOT EXISTS users(
id integer PRIMARY KEY AUTOINCREMENT,
reg_date DATETIME,
username text NOT NULL,
balance text NOT NULL,
email text NOT NULL,
isAdmin bool NOT NULL,
password text NOT NULL,
name text ,
surname text
);