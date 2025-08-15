import datetime
import pytz
import textwrap

def menu():
    menu_text = '''
    ========Menu========
                       
    Selecione uma opção:

    [1] Depositar
    [2] Sacar
    [3] Consultar Saldo
    [4] Criar Usuário
    [5] Listar Contas
    [6] Criar Conta
    [0] Sair

    Digite sua opção:'''
    return int(input(textwrap.dedent(menu_text)))

def depositar(saldo, extrato, valor_deposito, data_hora, /):
    if valor_deposito <= 0:
        print('Valor inválido! O depósito deve ser maior que zero.')
        return saldo, extrato
    else:
        print(f'Você depositou R$ {valor_deposito:.2f}')
        extrato += f'Depósito: R$ {valor_deposito:.2f} {data_hora}\n'
        saldo += valor_deposito
        return saldo, extrato
    
def sacar(*,saldo, extrato, valor_saque, limite, numero_saques, LIMITE_SAQUES, data_hora):
    exedeu_saldo = valor_saque > saldo
    exedeu_limite = valor_saque > limite    
    excedeu_saques = numero_saques >= LIMITE_SAQUES
    if exedeu_saldo:
        print('Saldo insuficiente!')
    elif exedeu_limite:
        print(f'O valor do saque não pode ser maior que R$ {limite:.2f}!')
    elif excedeu_saques:
        print(f'Número máximo de saques por dia é {LIMITE_SAQUES}.')
    else:
        numero_saques += 1
        extrato += f'Saque: R$ {valor_saque:.2f} {data_hora}\n'
        saldo -= valor_saque
        print(f'Você sacou R$ {valor_saque:.2f}')
    return saldo, extrato, numero_saques

def consultar_saldo(saldo, extrato):
    print('\n========= Extrato =========')
    print('Não foram realizadas movimentações.' if not extrato else extrato)
    print(f'Saldo: R$ {saldo:.2f}')
    print('===========================')

def criar_usuario(usuarios):
    cpf = input('Digite o CPF (somente números): ')
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print('Já existe um usuário com esse CPF!')
        return usuarios
    nome = input('Digite o nome completo: ')
    data_nascimento = input('Digite a data de nascimento (DD-MM-AAAA): ')
    endereco = input('Digite o endereço (logradouro, nro - bairro - cidade/sigla estado): ')
    usuarios.append({'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco})
    print('Usuário criado com sucesso!')
    return usuarios

def listar_contas(contas):
    if not contas:
        print('Nenhuma conta cadastrada.')
        return
    for conta in contas:
        print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {conta['titular']['nome']}")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Digite o CPF do titular da conta: ')
    usuario = next((usuario for usuario in usuarios if usuario['cpf'] == cpf), None)
    if not usuario:
        print('Usuário não encontrado, por favor crie um usuário antes de criar uma conta.')
        return None
    conta = {'agencia': agencia, 'numero_conta': numero_conta, 'titular': usuario}
    print('Conta criada com sucesso!')
    return conta

def main():
    saldo = 0
    extrato = ""
    limite = 500
    numero_saques = 0
    LIMITE_SAQUES = 3
    agencia = "0001"
    contas = []
    usuarios = []
    horario_brasilia = pytz.timezone('America/Sao_Paulo')

    while True:
        opcao = menu()
        data_hora = datetime.datetime.now(horario_brasilia)

        if opcao == 1:
            valor_deposito = float(input('Digite o valor a ser depositado: '))
            saldo, extrato = depositar(saldo, extrato, valor_deposito, data_hora)
        elif opcao == 2:
            valor_saque = float(input('Digite o valor a ser sacado: '))
            saldo, extrato, numero_saques = sacar(saldo=saldo, extrato=extrato, valor_saque=valor_saque, 
                                                  limite=limite, numero_saques=numero_saques, 
                                                  LIMITE_SAQUES=LIMITE_SAQUES, data_hora=data_hora)
        elif opcao == 3:
            consultar_saldo(saldo, extrato)
        elif opcao == 4:
            usuarios = criar_usuario(usuarios)
        elif opcao == 5:
            listar_contas(contas)
        elif opcao == 6:
            numero_conta = len(contas) + 1
            conta = criar_conta(agencia, numero_conta, usuarios)
            if conta:
                contas.append(conta)
        elif opcao == 0:
            print('Obrigado por utilizar nosso sistema!')
            break
        else:
            print('Opção inválida! Tente novamente.')

    print('Sistema encerrado. Até logo!')

main()
