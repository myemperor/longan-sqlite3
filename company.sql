CREATE TABLE IF NOT EXISTS COMPANY(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   name           TEXT    NOT NULL,
   age            INT     NOT NULL,
   address        CHAR(50),
   salary         REAL
);