import util
import threading


def menu():
    # Inicia a thread da serial
    threading.Thread(target=util.ler_serial, daemon=True).start()
    
    while True:
        util.clear()
        print("===== MENU =====")
        print("1 - Listar vagas")
        print("2 - Ver vagas livres")
        print("3 - Historico")
        print("0 - Sair")
        opcao = input("Escolha: ")
        if opcao == "1":
            util.listar_vagas()
        elif opcao == "2":
            util.vagas_livres_ocupadas()
        elif opcao == "3":
            menu_historico()
        elif opcao == "0":
            break
        else:
            print("❗ Opção inválida")


def menu_historico():
    while True:
        print("\n===== HISTÓRICO =====")
        print("1 - Ver vaga 1")
        print("2 - Ver vaga 2")
        print("3 - Ver vaga 3")
        print("4 - Historico Geral")
        print("5 - Limpar histórico de vaga")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            util.ver_historico_vaga(1)

        elif op == "2":
            util.ver_historico_vaga(2)

        elif op == "3":
            util.ver_historico_vaga(3)

        elif op == "4":
            util.ver_historico()

        elif op == "5":
            vaga = input("Digite o número da vaga (1,2,3): ")
            if vaga in ["1", "2", "3"]:
                util.limpar_historico_vaga(int(vaga))
            else:
                print("❌ Vaga inválida")

        elif op == "0":
            break

        else:
            print("❌ Opção inválida")


if __name__ == "__main__":
    menu()

