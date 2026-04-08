import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "estacao.db")

def conectar():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leituras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperatura REAL,
            umidade REAL,
            pressao REAL
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Banco verificado em: {DB_PATH}")

def inserir_leitura(t, u, p):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO leituras (temperatura, umidade, pressao) VALUES (?, ?, ?)", (t, u, p))
    conn.commit()
    conn.close()

def buscar_leituras():
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, timestamp, temperatura, umidade, pressao FROM leituras ORDER BY timestamp ASC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()

def buscar_uma_leitura(id_leitura):
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM leituras WHERE id = ?", (id_leitura,)).fetchone()
    conn.close()
    return dict(row) if row else None

def atualizar_leitura(id_leitura, t, u, p):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE leituras SET temperatura=?, umidade=?, pressao=? WHERE id=?", (t, u, p, id_leitura))
    conn.commit()
    conn.close()

def deletar_leitura(id_leitura):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM leituras WHERE id = ?", (id_leitura,))
    conn.commit()
    conn.close()
