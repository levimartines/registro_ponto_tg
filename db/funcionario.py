import sqlite3  
  
con = sqlite3.connect("db/funcionario.db")  
print("O Banco de dados funcionario.py foi criado com Sucesso !!! ")    
con.execute("create table COLABORADORES (COL_ID INTEGER PRIMARY KEY AUTOINCREMENT, COL_RG TEXT, COL_NOME TEXT NOT NULL, COL_EMAIL TEXT UNIQUE NOT NULL)")
print("Tabelas Criadas com Sucesso.")   
con.close()  

