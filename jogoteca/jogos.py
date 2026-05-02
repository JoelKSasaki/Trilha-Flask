class Jogo:
    def __init__(self, nome, descricao, genero):
        self.nome = nome
        self.descricao = descricao
        self.genero = genero
    
jogo1 = Jogo('Tetris', 'Jogo casual', 'Puzzle')
jogo2 = Jogo('Campo minado', 'Deve encontrar as minas', 'Raciocínio lógico')
jogo3 = Jogo('Mortal Kombat', 'Jogo baseado em artes marciais', 'Luta')
jogo4 = Jogo('Mario Kart', 'Corrida com personagens do Mario', 'Corrida')
lista_jogos = [jogo1, jogo2, jogo3, jogo4]