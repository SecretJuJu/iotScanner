DROP TABLE IF EXISTS MacVender;
DROP TABLE IF EXISTS Exploit;

CREATE TABLE MacVender(
    macAddr char(6),
    company char(50)
);

CREATE TABLE Exploit(
    id integer primary key autoincrement,
    name char(50),
    company char(50),
    version char(30),
    productName char(50),
    exploitMovement text,
    path char(255)
);