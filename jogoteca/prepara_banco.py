import mysql.connector
from mysql.connector import errorcode

conn = None

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='joel',
            password='1234'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

if conn == None:
    exit()

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `jogoteca`;")

cursor.execute("CREATE DATABASE `jogoteca`;")

cursor.execute("USE `jogoteca`;")

# criando tabelas
TABLES = {}
TABLES['Jogos'] = ('''
      CREATE TABLE `jogos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `descricao` varchar(255) NOT NULL,
      `genero` varchar(30) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `username` varchar(40) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`username`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')


# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, username, senha) VALUES (%s, %s, %s)'
usuarios = [
    ("Joel", "Joellinton", "oH@iyo"),
    ("Kaka", "Kaka22", "Ballondor"),
    ("Louro", "Louro José", "maisvoce")
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from jogoteca.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
jogos_sql = 'INSERT INTO jogos (nome, descricao, genero) VALUES (%s, %s, %s)'
jogos = [
    ('Tetris', 'Jogo casual', 'Puzzle'),
    ('Campo minado', 'Deve encontrar as minas', 'Raciocínio lógico'),
    ('Mortal Kombat', 'Jogo baseado em artes marciais', 'Luta'),
    ('Mario Kart', 'Corrida com personagens do Mario', 'Corrida')
]
cursor.executemany(jogos_sql, jogos)

cursor.execute('select * from jogoteca.jogos')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
