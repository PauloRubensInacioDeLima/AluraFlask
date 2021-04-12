from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'Paulo_Rubens'

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

jogo1 = Jogo("Super Mario", "Ação", "SNES")
jogo2 = Jogo("Pokemon", "RPG", "GBA")
jogo3 = Jogo("Mortal Kombat", "Luta", "SNES")
lista = [jogo1, jogo2, jogo3]

usuario1 = Usuario("luan", "Luan Roberto", "1234")
usuario2 = Usuario("paulo", "Paulo Rubens", "abcd")
usuario3 = Usuario("jose", "José Ricardo", "4321")
usuarios = {
    usuario1.id: usuario1,
    usuario2.id: usuario2,
    usuario3.id: usuario3
}

@app.route('/')
def index():
    return render_template('lista.html',titulo = 'Jogos',
                           jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else :
        flash('Credenciais inválidas, por favor tente novamente!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    flash('O usuário ' + session['usuario_logado'] + ' foi desconectado do sistema!')
    session['usuario_logado'] = None
    return redirect(url_for('index'))

app.run(debug=True)