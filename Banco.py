import sqlite3

conexao = sqlite3.connect('ClinicaPsico.db')
cursor = conexao.cursor()

# cursor.execute('CREATE TABLE IF NOT EXISTS Pacientes('
#                'ID_Pac INTEGER PRIMARY KEY,'
#                'Nome TEXT,'
#                'DataNas TEXT,'
#                'Genero TEXT,'
#                'RG INTEGER,'
#                'Endereco TEXT,'
#                'Email TEXT,'
#                'Telefone INTEGER)')
#
# cursor.execute('''CREATE TABLE IF NOT EXISTS Consultas(
#                ID INTEGER PRIMARY KEY,
#                Horario TEXT,
#                DataCon TEXT,
#                ID_Pac INTEGER,
#                FOREIGN KEY (ID_Pac) REFERENCES Pacientes(ID_Pac)
#                );''')