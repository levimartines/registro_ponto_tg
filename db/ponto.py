import sqlite3
import datetime

con = sqlite3.connect("ponto.db")

con.execute("DROP TABLE IF EXISTS REGISTRO")
con.execute("DROP TABLE IF EXISTS COLABORADORES")
print("TABELAS DROPADAS")

con.execute(
    "CREATE TABLE COLABORADORES ("
    "COL_ID INTEGER PRIMARY KEY AUTOINCREMENT,"
    "COL_MATRICULA INTEGER NOT NULL,"
    "COL_NOME TEXT NOT NULL,"
    "COL_CPF TEXT NOT NULL,"
    "COL_RG TEXT NOT NULL,"
    "COL_SENHA TEXT NOT NULL,"
    "COL_EMAIL TEXT NOT NULL UNIQUE,"
    "COL_ADMIN INTEGER NOT NULL)"
)

con.execute(
    "CREATE TABLE REGISTRO ("
    "REG_ID INTEGER PRIMARY KEY AUTOINCREMENT,"
    "COL_ID INTEGER,"
    "REG_NOME TEXT NOT NULL,"
    "REG_DATA DATE NOT NULL,"
    "FOREIGN KEY(COL_ID) REFERENCES COLABORADORES(COL_ID))"
)
print("TABELAS CRIADAS")

con.execute(
    "INSERT INTO COLABORADORES (COL_MATRICULA, COL_NOME,COL_CPF,COL_RG,COL_SENHA,COL_EMAIL,COL_ADMIN) "
    "VALUES (?,?,?,?,?,?,?)",
    (1, "Renan Alcolea", "00000014141", "123", "renan", "renan@domain.com", 1)
)

con.execute(
    "INSERT INTO COLABORADORES (COL_MATRICULA, COL_NOME,COL_CPF,COL_RG,COL_SENHA,COL_EMAIL,COL_ADMIN) "
    "VALUES (?,?,?,?,?,?,?)",
    (2, "Sandra Lucia", "99999999999", "444", "sandra", "sandra@domain.com", 2)
)

con.execute(
    "INSERT INTO REGISTRO (COL_ID, REG_NOME, REG_DATA) VALUES (?,?,?)",
    (1, "Renan Alcolea", datetime.datetime.now())
)

con.execute(
    "INSERT INTO REGISTRO (COL_ID, REG_NOME, REG_DATA) VALUES (?,?,?)",
    (2, "Sandra Lucia", datetime.datetime.now())
)

con.commit()
print("DADOS INSERIDOS")

con.close()
