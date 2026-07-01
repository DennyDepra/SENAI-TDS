import serial
import time
import mysql.connector
from datetime import datetime

import os
# No topo do arquivo, após os imports
ultimo_status = [None, None, None]  # guarda o último estado de cada vaga

def registrar_entrada(cursor, vaga):
    agora = datetime.now()
    cursor.execute("""
        INSERT INTO historico (id_vaga, entrada)
        VALUES (%s, %s)
    """, (vaga, agora))

def registrar_saida(cursor, vaga):
    agora = datetime.now()

    cursor.execute("""
        SELECT id_historico, entrada FROM historico
        WHERE id_vaga = %s AND saida IS NULL
        ORDER BY id_historico DESC LIMIT 1
    """, (vaga,))

    resultado = cursor.fetchone()

    if resultado:
        id_registro, entrada = resultado

        # 🔹 calcula tempo
        tempo = int((agora - entrada).total_seconds())

        # 🔹 calcula valor
        valor = tempo * 5

        # 🔹 atualiza tudo no banco
        cursor.execute("""
            UPDATE historico
            SET saida = %s, tempo_segundos = %s, valor = %s
            WHERE id_historico = %s
        """, (agora, tempo, valor, id_registro))

def abrir_conexao():
    conn = conectar()
    cursor = conn.cursor()
    return conn, cursor

def fechar_conexao(conn,cursor):
    cursor.close()
    conn.close()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def pressEnter():
    input("Pressione um tecla para continuar...")

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="estacionamento_iot"
    )
# 🔹 READ
def listar_vagas():
    conn, cursor = abrir_conexao()

    cursor.execute("SELECT numero_vaga, status_vaga FROM vaga;")
    resultados = cursor.fetchall()

    print("\n📋 LISTA DE VAGAS:")
    for numero, status in resultados:
        print(f"Vaga {numero}: {status}")

    fechar_conexao(conn, cursor)
    pressEnter()
# 🔹 UPDATE
def atualizar_status(cursor, conn, id_vaga, novo_status):
    sql = "UPDATE vaga SET status_vaga = %s WHERE id_vaga = %s"
    cursor.execute(sql, (novo_status, id_vaga))

def vagas_livres_ocupadas():
    conn, cursor = abrir_conexao()

    cursor.execute("SELECT COUNT(*) FROM vaga WHERE status_vaga = 'livre';")
    livres = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM vaga WHERE status_vaga = 'ocupada';")
    ocupadas = cursor.fetchone()[0]

    print("\nLivres:", livres)
    print("Ocupadas:", ocupadas,"\n")

    fechar_conexao(conn, cursor)
    print("\n")
    pressEnter()

def ler_serial():
    global ultimo_status

    try:
        ser = serial.Serial('COM5', 9600, timeout=1)
        time.sleep(2)

        while True:
            if ser.in_waiting:
                linha = ser.readline().decode().strip()

                if linha:
                    estados = linha.split(',')

                    if len(estados) == 3:
                        conn, cursor = abrir_conexao()  # abre aqui

                        for i, e in enumerate(estados):
                            status = "livre" if e == "1" else "ocupada"

                            if ultimo_status[i] != status:
                                vaga = i + 1

                                if status == "ocupada":
                                    registrar_entrada(cursor, vaga)
                                else:
                                    registrar_saida(cursor, vaga)

                                atualizar_status(cursor, conn, vaga, status)

                                ultimo_status[i] = status

                        conn.commit()
                        fechar_conexao(conn, cursor)  # fecha aqui

                    else:
                        print(f"⚠️ Dado inválido: {linha}")

            time.sleep(0.2)

    except Exception as e:
        print("Erro:", e)
   
def ver_historico():
    conn, cursor = abrir_conexao()

    cursor.execute("""
        SELECT id_vaga, entrada, saida, tempo_segundos, valor
        FROM historico
        ORDER BY id_historico DESC
    """)

    resultados = cursor.fetchall()

    print("\n📜 HISTÓRICO:")
    for vaga, entrada, saida, tempo, valor in resultados:
        print(f"Vaga {vaga} | Entrada: {entrada} | Saída: {saida} | Tempo: {tempo} seg | Valor: R$ {valor:.2f}")

    fechar_conexao(conn, cursor)
    print("\n")
    pressEnter()

def ver_historico_vaga(id_vaga):
    conn, cursor = abrir_conexao()

    cursor.execute("""
        SELECT entrada, saida, tempo_segundos
        FROM historico
        WHERE id_vaga = %s
        ORDER BY id_historico DESC
    """, (id_vaga,))

    resultados = cursor.fetchall()

    print(f"\n📜 HISTÓRICO DA VAGA {id_vaga}:")

    if resultados:
        for entrada, saida, tempo in resultados:
            if tempo is not None:
                valor = calcular_valor(tempo)
                print(f"Entrada: {entrada} | Saída: {saida} | Tempo: {tempo}s | Valor: R$ {valor:.2f}")
            else:
                print(f"Entrada: {entrada} | Saída: {saida} | Tempo: em aberto")
    else:
        print("Nenhum registro encontrado.")

    fechar_conexao(conn, cursor)
    pressEnter()

def limpar_historico_vaga(id_vaga):
    conn, cursor = abrir_conexao()

    cursor.execute("""
        DELETE FROM historico
        WHERE id_vaga = %s
    """, (id_vaga,))

    conn.commit()

    print(f"\n🗑 Histórico da vaga {id_vaga} apagado!")

    fechar_conexao(conn, cursor)
    pressEnter()

def calcular_valor(tempo_segundos):
    valor = tempo_segundos * 5
    return valor