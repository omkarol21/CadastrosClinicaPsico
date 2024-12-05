from flask import Flask, render_template, request, redirect, g
import sqlite3

app = Flask(__name__)

# ----- Conexão com o banco de dados -----
def ligar_banco():
    if 'db' not in g:
        g.db = sqlite3.connect('ClinicaPsico.db')
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db

@app.teardown_appcontext
def fechar_banco(exc):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# ----- Rotas de páginas -----
@app.route('/')
def home():
    return render_template('Home.html', Titulo='Home')

@app.route('/importancia')
def importancia():
    return render_template('Importancia.html', Titulo='Importância')

@app.route('/cadastroPac')
def cadastro():
    return render_template('CadastroPac.html', Titulo='Cadastro de Pacientes')

# ----- Funcionalidades: Pacientes -----
@app.route('/criarPac', methods=['POST'])
def criar():
    banco = ligar_banco()
    cursor = banco.cursor()
    nome = request.form['nome']
    dataNas = request.form['dataNas']
    genero = request.form['genero']
    rg = request.form['rg']
    endereco = request.form['endereco']
    email = request.form['email']
    telefone = request.form['telefone']
    cursor.execute(
        'INSERT INTO Pacientes (Nome, DataNas, Genero, RG, Endereco, Email, Telefone) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (nome, dataNas, genero, rg, endereco, email, telefone)
    )
    banco.commit()
    return redirect('/cadastroPac')

@app.route('/exibirPaciente')
def exibir_Pac():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT * FROM Pacientes')
    pacientes = cursor.fetchall()
    return render_template('ExibirPacientes.html', Titulo='Exibir Paciente', ListaPac=pacientes)

@app.route('/editarPac/<int:ID_Pac>', methods=['GET'])
def editar(ID_Pac):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT * FROM Pacientes WHERE ID_Pac = ?', (ID_Pac,))
    paciente = cursor.fetchone()
    return render_template('EditarPac.html', paciente=paciente, Titulo="Editar Pacientes")

@app.route('/alterarPac', methods=['POST'])
def alterar():
    banco = ligar_banco()
    cursor = banco.cursor()
    nome = request.form['nome']
    dataNas = request.form['dataNas']
    genero = request.form['genero']
    rg = request.form['rg']
    endereco = request.form['endereco']
    email = request.form['email']
    telefone = request.form['telefone']
    ID_Pac = request.form['idpac']
    cursor.execute(
        'UPDATE Pacientes SET Nome = ?, DataNas = ?, Genero = ?, RG = ?, Endereco = ?, Email = ?, Telefone = ? WHERE ID_Pac = ?',
        (nome, dataNas, genero, rg, endereco, email, telefone, ID_Pac)
    )
    banco.commit()
    return redirect('/exibirPaciente')

@app.route('/excluirPac/<int:ID_Pac>', methods=['GET'])
def deletar(ID_Pac):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('DELETE FROM Pacientes WHERE ID_Pac = ?', (ID_Pac,))
    banco.commit()
    return redirect('/exibirPaciente')

# ----- Funcionalidades: Consultas -----
@app.route('/cadastroCon')
def cadastroConsulta():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT ID_Pac, Nome FROM Pacientes')
    Nome_Pacs = cursor.fetchall()
    return render_template('CadastroConsultas.html', Titulo='Cadastro de Consulta', listaPacientes=Nome_Pacs)

@app.route('/criarConsulta', methods=['POST'])
def criar_Consulta():
    banco = ligar_banco()
    cursor = banco.cursor()
    nomePac = request.form['nomePac']
    horario = request.form['horario']
    dataCons = request.form['dataCon']
    cursor.execute(
        'INSERT INTO Consultas (Horario, DataCon, ID_Pac) VALUES (?, ?, ?)',
        (horario, dataCons, nomePac)
    )
    banco.commit()
    return redirect('/cadastroCon')

@app.route('/exibirConsultas')
def exibir_Con():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT * FROM Consultas')
    consultas = cursor.fetchall()
    cursor.execute('SELECT ID_Pac, Nome FROM Pacientes')
    total_pacientes = cursor.fetchall()
    return render_template('ExibirConsultas.html', Titulo='Exibir Consultas', ListaCon=consultas, pacientes=total_pacientes)

@app.route('/excluirCon/<int:ID>', methods=['GET'])
def deletar_Con(ID):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('DELETE FROM Consultas WHERE ID = ?', (ID,))
    banco.commit()
    return redirect('/exibirConsultas')

if __name__ == '__main__':
    app.run()
