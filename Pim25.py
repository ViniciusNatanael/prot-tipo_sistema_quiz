import random
import uuid
import statistics
import matplotlib.pyplot as plt
import json
import os

# Classe base
class Pessoa:
    def __init__(self, nome, email, id=None):
        self.nome = nome
        self.email = email
        self.id = id or str(uuid.uuid4())

    def exibir_dados(self):
        return f"id:{self.id}: {self.nome}\n Email: {self.email}\n"

    def to_dict(self):
        return {"nome": self.nome, "email": self.email, "id": self.id}

    @classmethod
    def from_dict(cls, data):
        return cls(data["nome"], data["email"], data["id"])

# Classe Aluno
class Aluno(Pessoa):
    def __init__(self, nome, email, matricula, id=None):
        super().__init__(nome, email, id)
        self.matricula = matricula

    def exibir_dados(self):
        return f"[Aluno] {super().exibir_dados()} | Matrícula: {self.matricula}"

    def to_dict(self):
        data = super().to_dict()
        data["matricula"] = self.matricula
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["nome"], data["email"], data["matricula"], data["id"])

# Classe Professor
class Professor(Pessoa):
    def __init__(self, nome, email, disciplina, id=None):
        super().__init__(nome, email, id)
        self.disciplina = disciplina

    def exibir_dados(self):
        return f"[Professor] {super().exibir_dados()} \n Disciplina: {self.disciplina}"

    def to_dict(self):
        data = super().to_dict()
        data["disciplina"] = self.disciplina
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["nome"], data["email"], data["disciplina"], data["id"])

# Sistema de Cadastro
class SistemaCadastro:
    ALUNOS_FILE = "alunos.json"
    PROFESSORES_FILE = "professores.json"
    NOTAS_FILE = "notas.json"

    def __init__(self):
        self.alunos = []
        self.professores = []
        self.notas_quiz = []
        self.carregar_dados()

    def salvar_dados(self):
        with open(self.ALUNOS_FILE, "w") as f:
            json.dump([aluno.to_dict() for aluno in self.alunos], f, indent=4)
        with open(self.PROFESSORES_FILE, "w") as f:
            json.dump([prof.to_dict() for prof in self.professores], f, indent=4)
        with open(self.NOTAS_FILE, "w") as f:
            json.dump(self.notas_quiz, f, indent=4)

    def carregar_dados(self):
        if os.path.exists(self.ALUNOS_FILE):
            with open(self.ALUNOS_FILE, "r") as f:
                alunos_data = json.load(f)
                self.alunos = [Aluno.from_dict(a) for a in alunos_data]
        if os.path.exists(self.PROFESSORES_FILE):
            with open(self.PROFESSORES_FILE, "r") as f:
                profs_data = json.load(f)
                self.professores = [Professor.from_dict(p) for p in profs_data]
        if os.path.exists(self.NOTAS_FILE):
            with open(self.NOTAS_FILE, "r") as f:
                self.notas_quiz = json.load(f)

    def cadastrar_aluno(self):
        nome = input("Nome do aluno: ")
        email = input("Email do aluno: ")
        matricula = input("Matrícula do aluno: ")
        aluno = Aluno(nome, email, matricula)
        self.alunos.append(aluno)
        self.salvar_dados()
        print(" Aluno cadastrado com sucesso!")

    def cadastrar_professor(self):
        nome = input("Nome do professor: ")
        email = input("Email do professor: ")
        disciplina = input("Disciplina do professor: ")
        professor = Professor(nome, email, disciplina)
        self.professores.append(professor)
        self.salvar_dados()
        print(" Professor cadastrado com sucesso!")

    def listar_todos(self):
        print("\n Lista de Alunos:")
        for aluno in self.alunos:
            print(aluno.exibir_dados())

        print("\n Lista de Professores:")
        for professor in self.professores:
            print(professor.exibir_dados())

    def listar_notas(self):
        if not self.notas_quiz:
            print("Nenhuma nota registrada ainda.")
            return

        print("\n Histórico de Notas dos Quizzes:")
        for nota in self.notas_quiz:
            print(f"Aluno: {nota['aluno']} | Nota: {nota['pontuacao']}/10")

    def calcular_estatisticas(self):
        if not self.notas_quiz:
            print("Nenhuma nota registrada para estatísticas.")
            return

        notas = [nota['pontuacao'] for nota in self.notas_quiz]

        media = statistics.mean(notas)
        mediana = statistics.median(notas)
        try:
            moda = statistics.mode(notas)
        except statistics.StatisticsError:
            moda = "Não há uma moda (valores igualmente frequentes)"

        print("\n📊 Estatísticas das Notas:")
        print(f"Média: {media:.2f}")
        print(f"Mediana: {mediana}")
        print(f"Moda: {moda}")

        # Gráfico
        plt.figure(figsize=(8, 6))
        plt.hist(notas, bins=range(0, 12), edgecolor='black', alpha=0.7)
        plt.axvline(media, color='blue', linestyle='dashed', linewidth=2, label=f"Média: {media:.2f}")
        plt.axvline(mediana, color='orange', linestyle='dashed', linewidth=2, label=f"Mediana: {mediana}")
        if isinstance(moda, (int, float)):
            plt.axvline(moda, color='green', linestyle='dashed', linewidth=2, label=f"Moda: {moda}")
        plt.title('Distribuição das Notas do Quiz')
        plt.xlabel('Notas')
        plt.ylabel('Frequência')
        plt.legend()
        plt.grid(True)
        plt.savefig("grafico_notas.png")
        plt.show()

# Classe do Quiz
class Quiz:
    def __init__(self, aluno_nome, sistema_cadastro):
        self.aluno_nome = aluno_nome
        self.sistema_cadastro = sistema_cadastro
        self.pontuacao = 0
        self.perguntas = [
            {"pergunta": "\n Qual estrutura é usada para repetir um bloco de código um número fixo de vezes? \n", "opcoes": ["if", "for", "while", "elif"], "correta": "for"},
            {"pergunta": "\n Qual estrutura repete enquanto uma condição for verdadeira? \n", "opcoes": ["for", "if", "while", "else"], "correta": "while"},
            {"pergunta": "\n Qual palavra é usada para criar uma condição em Python? \n", "opcoes": ["loop", "for", "if", "repeat"], "correta": "if"},
            {"pergunta": "\n O que será impresso?\nfor i in range(3): print(i) \n", "opcoes": ["1 2 3", "0 1 2", "0 1 2 3", "1 2"], "correta": "0 1 2"},
            {"pergunta": "\n Qual dessas opções é usada para tratar uma segunda condição? \n", "opcoes": ["elif", "else if", "otherwise", "while"], "correta": "elif"},
            {"pergunta": "\n Quando usamos 'else'? \n", "opcoes": ["Quando a condição é verdadeira", "Sempre que 'if' falha", "Quando queremos repetir algo", "Para encerrar o programa"], "correta": "Sempre que 'if' falha"},
            {"pergunta": "\n Qual é o valor final de 'x'?\nx = 0\nfor i in range(3):\n    x += 1 \n", "opcoes": ["2", "3", "0", "1"], "correta": "3"},
            {"pergunta": "\n Qual destas estruturas pode causar um loop infinito? \n", "opcoes": ["for", "while", "if", "elif"], "correta": "while"},
            {"pergunta": "\n O que esse código faz?\nif 5 > 3:\n    print('A')\nelse:\n    print('B')\n", "opcoes": ["Imprime B", "Erro", "Nada", "Imprime A"], "correta": "Imprime A"},
            {"pergunta": "\n Como encerrar um loop antecipadamente? \n", "opcoes": ["continue", "end", "break", "stop"], "correta": "break"}
        ]

    def iniciar(self):
        print("\n Iniciando o Quiz sobre Repetição e Condicionais!\n")
        random.shuffle(self.perguntas)

        explicacoes = {
            "for": " O 'for' é usado quando sabemos exatamente quantas vezes queremos repetir um bloco de código.",
            "while": " O 'while' repete enquanto a condição for verdadeira. Cuidado com loops infinitos!",
            "if": " O 'if' é usado para testar condições e decidir o fluxo do programa.",
            "0 1 2": " A função range(3) gera os valores 0, 1 e 2, por isso o print exibe 0 1 2.",
            "elif": " O 'elif' permite testar outra condição se o 'if' inicial falhar.",
            "Sempre que 'if' falha": " O 'else' é executado quando a condição do 'if' não é satisfeita.",
            "3": " O loop for é executado 3 vezes, e a variável x é incrementada em cada uma, ficando com valor 3.",
            "Imprime A": " O código verifica se 5 > 3, o que é verdadeiro, então imprime 'A'.",
            "break": " O 'break' encerra um loop imediatamente, útil para sair antes do final.",
        }

        for i, q in enumerate(self.perguntas, 1):
            print(f"\n🔹 Questão {i}")
            print(q["pergunta"])
            for idx, opcao in enumerate(q["opcoes"], 1):
                print(f"{idx}. {opcao}")
            resposta = input("Sua resposta (número): ")

            if resposta.isdigit():
                indice = int(resposta) - 1
                if 0 <= indice < len(q["opcoes"]):
                    if q["opcoes"][indice] == q["correta"]:
                        print(" Correto!")
                        self.pontuacao += 1
                    else:
                        print(f" Errado! Resposta correta: {q['correta']}")
                    print(explicacoes.get(q["correta"], " Sem explicação disponível."))
                else:
                    print(" Opção fora do alcance.")
            else:
                print(" Resposta inválida.")

        print(f"\n Fim do quiz! Sua pontuação: {self.pontuacao}/10")
        self.sistema_cadastro.notas_quiz.append({
            "aluno": self.aluno_nome,
            "pontuacao": self.pontuacao
        })
        self.sistema_cadastro.salvar_dados()

def menu():
    sistema = SistemaCadastro()

    while True:
        print("\n    MENU    \n")
        print("1. Cadastrar Aluno")
        print("2. Cadastrar Professor")

        if sistema.alunos or sistema.professores:
            print("3. Listar todos")
            print("4. Iniciar Quiz")
            print("5. Ver histórico de notas")
            print("6. Ver estatísticas e gráfico ")

        print("0. Sair \n")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            sistema.cadastrar_aluno()
        elif opcao == "2":
            sistema.cadastrar_professor()
        elif opcao == "3":
            if sistema.alunos or sistema.professores:
                sistema.listar_todos()
            else:
                print("⚠️ Primeiro cadastre um aluno ou professor.")
        elif opcao == "4":
            if sistema.alunos:
                nome = input("Digite seu nome para registrar a pontuação: ")
                quiz = Quiz(nome, sistema)
                quiz.iniciar()
            else:
                print("⚠️ Nenhum aluno cadastrado para iniciar o quiz.")
        elif opcao == "5":
            if sistema.alunos:
                sistema.listar_notas()
            else:
                print("⚠️ Primeiro cadastre um aluno para ter histórico.")
        elif opcao == "6":
            if sistema.notas_quiz:
                sistema.calcular_estatisticas()
            else:
                print("⚠️ Nenhuma nota registrada para estatísticas.")
        elif opcao == "0":
            print("Encerrando o sistema...")
            break
        else:
            print("⚠️ Opção inválida.")

if __name__ == "__main__":
    menu()
