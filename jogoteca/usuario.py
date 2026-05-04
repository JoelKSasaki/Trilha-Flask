class Usuario:
    def __init__(self, nome, username, password):
        self.nome = nome
        self.username = username
        self.password = password

usuario1 = Usuario("Joel", "Joellinton", "oH@iyo")
usuario2 = Usuario("Kaka", "Kaka22", "Ballondor")
usuario3 = Usuario("Louro", "Louro José", "maisvoce")

usuarios = {
    usuario1.username: usuario1,
    usuario2.username: usuario2,
    usuario3.username: usuario3
}

