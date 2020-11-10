import sqlite3
import datetime

con = sqlite3.connect("ponto.db")

con.execute("DROP TABLE IF EXISTS REGISTRO")
con.execute("DROP TABLE IF EXISTS COLABORADORES")
print("TABELAS DROPADAS")

con.execute(
    "CREATE TABLE COLABORADORES ("
    "COL_ID INTEGER PRIMARY KEY AUTOINCREMENT,"
    "COL_REGISTRO INTEGER NOT NULL,"
    "COL_NOME TEXT NOT NULL,"
    "COL_EMAIL TEXT UNIQUE NOT NULL)"
)

con.execute(
    "CREATE TABLE REGISTRO ("
    "REG_ID INTEGER PRIMARY KEY AUTOINCREMENT,"
    "COL_ID INTEGER,"
    "REG_NOME TEXT NOT NULL,"
    "REG_DATA DATE NOT NULL,"
    "FOREIGN KEY(COL_ID) REFERENCES COLABORADORES(COL_ID))"
)
con.execute(
    "INSERT INTO COLABORADORES (COL_REGISTRO, COL_NOME, COL_EMAIL) VALUES (?,?,?)",
    (1, "Renan Alcolea", "renan@levi.com")
)

con.execute(
    "INSERT INTO COLABORADORES (COL_REGISTRO, COL_NOME, COL_EMAIL) VALUES (?,?,?)",
    (2, "Levi Martines", "levi@levi.com")
)

con.execute(
    "INSERT INTO REGISTRO (COL_ID, REG_NOME, REG_DATA) VALUES (?,?,?)",
    (1, "Renan Alcolea", datetime.datetime.now())
)

con.execute(
    "INSERT INTO REGISTRO (COL_ID, REG_NOME, REG_DATA) VALUES (?,?,?)",
    (2, "Levi Martines", datetime.datetime.now())
)

con.commit()
print("TABELAS CRIADAS")

con.close()
