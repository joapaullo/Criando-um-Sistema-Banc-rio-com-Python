## criar um programa bancário que leia e execute as funções básicas do cliente.

class Cliente:
    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone

class Conta:
    def __init__(self, clientes, número, saldo=0):
        self.saldo = 0
        self.clientes = clientes
        self.número = número
        self.operações = []
        self.cartao_bloqueado = False  # Adicionando um atributo para controlar o status do cartão
        self.deposito(saldo)

    def resumo(self):
        print(f"CC N°{self.número} Saldo: {self.saldo:10.2f} - Cartão {'BLOQUEADO' if self.cartao_bloqueado else 'ATIVO'}")

    def pode_sacar(self, valor):
        return self.saldo >= valor and not self.cartao_bloqueado

    def saque(self, valor):
        if not self.cartao_bloqueado:
            if self.pode_sacar(valor):
                self.saldo -= valor
                self.operações.append(["SAQUE", valor])
                return True
            else:
                print("Saldo insuficiente!")
                return False
        else:
            print("Cartão bloqueado. Não é possível realizar saques.")
            return False

    def deposito(self, valor):
        if not self.cartao_bloqueado:
            self.saldo += valor
            self.operações.append(["DEPÓSITO", valor])
        else:
            print("Cartão bloqueado. Não é possível realizar depósitos.")

    def extrato(self):
        print(f"Extrato CC N° {self.número} - Cartão {'BLOQUEADO' if self.cartao_bloqueado else 'ATIVO'}\n")
        for o in self.operações:
            print(f"{o[0]:10s}  {o[1]:10.2f}")
        print(f"\n        Saldo: {self.saldo:10.2f}\n")

    def comunicar_perda_cartao(self):
        if not self.cartao_bloqueado:
            self.cartao_bloqueado = True
            print("Cartão bloqueado com sucesso.")
        else:
            print("O cartão já está bloqueado.")

    def pedir_novo_cartao(self):
        if self.cartao_bloqueado:
            print("Pedido de novo cartão realizado. Um novo cartão será enviado.")
            self.cartao_bloqueado = False # Consideramos que ao pedir um novo, o status volta a ativo (pode ser ajustado)
        else:
            print("Seu cartão atual está ativo. Deseja realmente pedir um novo?")
            confirmacao = input("(S/N): ").upper()
            if confirmacao == "S":
                print("Pedido de novo cartão realizado. Um novo cartão será enviado.")
                self.cartao_bloqueado = False
            else:
                print("Pedido de novo cartão cancelado.")


class ContaEspecial(Conta):
    def __init__(self, clientes, número, saldo=0, limite=0):
        Conta.__init__(self, clientes, número, saldo)
        self.limite = limite

    def pode_sacar(self, valor):
        return self.saldo + self.limite >= valor and not self.cartao_bloqueado

    def saque(self, valor):
        if not self.cartao_bloqueado:
            if self.pode_sacar(valor):
                self.saldo -= valor
                self.operações.append(["SAQUE", valor])
                return True
            else:
                print("Saldo insuficiente!")
                return False
        else:
            print("Cartão bloqueado. Não é possível realizar saques.")
            return False

    def deposito(self, valor):
        Conta.deposito(self, valor) # Chama o método deposito da classe mãe, que já verifica o bloqueio

    def extrato(self):
        print(f"Extrato CC N° {self.número} - Cartão {'BLOQUEADO' if self.cartao_bloqueado else 'ATIVO'}\n")
        for o in self.operações:
            print(f"{o[0]:10s}  {o[1]:10.2f}")
        print(f"\n Limite: {self.limite:10.2f}\n")
        print(f"\n Disponivel: {self.limite + self.saldo:10.2f}\n")

    def comunicar_perda_cartao(self):
        Conta.comunicar_perda_cartao(self) # Chama o método da classe mãe

    def pedir_novo_cartao(self):
        Conta.pedir_novo_cartao(self) # Chama o método da classe mãe


if __name__ == "__main__":
    nome_cliente = input("Digite o nome do cliente: ")
    telefone_cliente = input("Digite o telefone do cliente: ")

    cliente = Cliente(nome_cliente, telefone_cliente)

    tipo_conta = input("Deseja criar uma conta comum (C) ou especial (E)? ").upper()

    numero_conta = int(input("Digite o número da conta: "))
    saldo_inicial = float(input("Digite o saldo inicial da conta: "))

    if tipo_conta == "E":
        limite_conta = float(input("Digite o limite da conta especial: "))
        conta = ContaEspecial([cliente], numero_conta, saldo_inicial, limite_conta)
    elif tipo_conta == "C":
        conta = Conta([cliente], numero_conta, saldo_inicial)
    else:
        print("Tipo de conta inválido.")
        exit()

    print("\nDados da conta criada:")
    conta.extrato()

    while True:
        print("\nEscolha uma operação:")
        print("1 - Depósito")
        print("2 - Saque")
        print("3 - Extrato")
        print("4 - Pedido de cartão")
        print("5 - Comunicar a Perda do cartão")
        print("6 - Sair")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            valor_deposito = float(input("Digite o valor a depositar: "))
            conta.deposito(valor_deposito)
        elif opcao == "2":
            valor_saque = float(input("Digite o valor a sacar: "))
            conta.saque(valor_saque)
        elif opcao == "3":
            conta.extrato()
        elif opcao == "4":
            conta.pedir_novo_cartao()
        elif opcao == "5":
            conta.comunicar_perda_cartao()
        elif opcao == "6":
            print("Obrigado!")
            break
        else:
            print("Opção inválida. Tente novamente.")