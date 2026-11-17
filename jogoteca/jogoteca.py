from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #Depois de instanciar a classe Flask, pegar a instância e definir o atributo secret_key com um valor string que será usado para encriptar os dados da sessão.
app.secret_key = 'Liverpool' #chave de criptografia da senha aos Cookies para eles não serem alterados

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{password}@{servidor}/{database}'.format(
        SGBD = "mysql+mysqlconnector",
        usuario = "joel",
        password = "1234",
        servidor = "localhost",
        database = "jogoteca"
    )
#passa o endereço com as configurações do BDD e o SQLAlchemy fará a conexão com o BDD

db = SQLAlchemy(app) #instancia o BDD do SQLAlchemy, que se conectará com a aplicação

class Jogos(db.Model): #Model: função do SQLAlchemy que representa uma instanciação do BDD. Assim, ela é filha de um objeto de banco de dados
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome = db.Column(db.String(50), nullable = False)
    descricao = db.Column(db.String(255), nullable = False)
    genero = db.Column(db.String(30), nullable = False)

    def __repr__(self):
        return '<Name %r>' % self.name
    
class Usuarios(db.Model):
    username = db.Column(db.String(40), primary_key = True)
    nome = db.Column(db.String(20), nullable = False)
    senha = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return '<Name %r>' % self.name

lista_jogos = 0
@app.route("/")
def index():
    lista_jogos = Jogos.query.order_by(Jogos.id) #busca os jogos na tabela

    if session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('index')))
    return render_template('lista.html', titulo = 'Games', jogos = lista_jogos)

    

@app.route("/adicionar-jogo")
def novojogo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None: #usuário não está logado?
        return redirect(url_for('login', proxima=url_for('novojogo'))) #url_for: mostra a próxima página a ser acessada (a própria função na qual ele está)
    #query string: guarda os dados da próxima página a ser acessada na URL, ficando visível ao usuário
    return render_template('newjogo.html', titulo = "Novo Jogo")

'''dados de um formulário da web: enviados encapsulados em forma de requisição ao servidor em modo POST.
O servidor deve processar esses dados através de uma nova rota intermediária.
Assim, ele devolve uma resposta(response) autorizando o login dele/inclusão dos dados.
'''
@app.route("/criar-jogo", methods = ['POST'])
def criarjogo():
    nome = request.form['nome'] #pega o valor inserido na caixa de texto correspondente ao nome da tag
    descricao = request.form['descricao']    
    genero = request.form['genero']

    jogo = Jogos.query.filter_by(nome = nome).first() #o primeiro corresnpondente será encontrado

    if jogo:
        flash(f'{jogo} já existente')
        return redirect (url_for('index')) 
    
    novo_jogo = Jogos(nome=nome, descricao=descricao, genero=genero)
    db.session.add(novo_jogo)
    db.session.commit() #confirma a adição do jogo

    return redirect (url_for('index')) 
#redirect: redireciona para uma rota criada anteriormente sem renderizar o html

@app.route('/login')
def login():
    proxima = request.args.get('proxima') #pega a informação da rota query string a ser acessada
    return render_template('login.html', titulo = "Login", proxima=proxima)

@app.route('/autenticar', methods = ['POST'])
def autenticar():

    usuario = Usuarios.query.filter_by(username = request.form['username']).first() #busca os jogos na tabela
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.username
            flash(f'{usuario.username} logado com sucesso')
            proxima_pagina = request.form.get('proxima')   
            if not proxima_pagina or proxima_pagina == 'None':
                return redirect(url_for('index'))     
            return redirect(proxima_pagina or url_for('index'))
        else:
            flash(f'{request.form['username']} não logado. Nome de usuário ou senha incorretos')
            return redirect(url_for('login'))    
    else:
        flash(f'{request.form['username']} não cadastrado.')
        return redirect(url_for('login'))    
    
    '''if 'VARmeiras' == request.form['senha']:
        session['usuario_logado'] = request.form['username']#chave: usuario_logado; guarda o nome do usuário 
        flash(session['usuario_logado'] + ' logado com sucesso')
        proxima_pagina = request.form.get('proxima') 
        return redirect(proxima_pagina)''' 

#inserção de dados numa sessão: Importar o objeto session na aplicação e incluir uma nova chave neste objeto, que é um dicionário.
#session: retém dados do usuário por mais de um ciclo request nos COOKIES criptografados do navegador
#flash: mostra uma mensagem curta na tela de forma eficiente

@app.route('/logout')
def logout():
    session['usuario_logado'] = None 
    flash('Logout feito com sucesso')
    return redirect (url_for('index'))
#url_for: pega o link a partir da função que o instancia 
#Session vazio: não grava o nome do usuário (chave) e sua sessão é encerrada

app.run(debug=True)