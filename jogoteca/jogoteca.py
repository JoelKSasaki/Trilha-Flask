from flask import Flask, render_template
from jogos import Jogo

app = Flask(__name__)

@app.route("/main")
def main():
    jogo1 = Jogo('Tetris', 'Jogo casual', 'Puzzle')
    jogo2 = Jogo('Campo minado', 'Deve encontrar as minas', 'Raciocínio lógico')
    jogo3 = Jogo('Mortal Kombat', 'Jogo baseado em artes marciais', 'Luta')
    jogo4 = Jogo('Mario Kart', 'COrrida com personagens do Mario', 'Corrida')
    lista_jogos = [jogo1, jogo2, jogo3, jogo4]
    return render_template('lista.html', titulo = 'Games', jogos = lista_jogos)

@app.route("/adicionar-jogo")
def novojogo():
    return render_template('newjogo.html', titulo = "Novo Jogo")
app.run()