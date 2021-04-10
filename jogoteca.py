from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)
app.secret_key = 'Paulo_Rubens'

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo("Super Mario","Ação","SNES")
jogo2 = Jogo("Pokemon","RPG","GBA")
jogo3 = Jogo("Mortal Kombat","Luta","SNES")
lista = [jogo1, jogo2, jogo3]

@app.route('/')
def index():
    return render_template('lista.html',titulo = 'Jogos',
                           jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=novo')
    return render_template('novo.html', titulo = 'novo jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect('/')

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if 'mestra' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(request.form['usuario'] + ' logou com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect('/{}'.format(proxima_pagina))
    else :
        flash('Credenciais inválidas, por favor tente novamente!')
        return redirect('/login')

@app.route('/logout')
def logout():
    flash('O usuário ' + session['usuario_logado'] + ' foi desconectado do sistema!')
    session['usuario_logado'] = None
    return redirect('/')


app.run(debug=True)