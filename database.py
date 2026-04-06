import sqlite3
import hashlib
import os
from datetime import datetime

class UserDB:
    def __init__(self, db_path="sprite_manager.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Inicializa as tabelas se não existirem."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Tabela de Usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL
                )
            ''')
            # Tabela de Ações (Logs)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    action TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            conn.commit()

    def _hash_password(self, password, salt=None):
        """Gera um hash SHA-256 com salt."""
        if salt is None:
            salt = os.urandom(16).hex()
        
        hash_obj = hashlib.sha256((password + salt).encode('utf-8'))
        return hash_obj.hexdigest(), salt

    def register_user(self, username, password):
        """Registra um novo usuário. Retorna True se sucesso, False se já existir."""
        password_hash, salt = self._hash_password(password)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                    (username, password_hash, salt)
                )
                conn.commit()
            return True, "Usuário registrado com sucesso!"
        except sqlite3.IntegrityError:
            return False, "Nome de usuário já existe."
        except Exception as e:
            return False, str(e)

    def authenticate_user(self, username, password):
        """Autentica o usuário. Retorna (user_id, username) se sucesso, senão None."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password_hash, salt FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            
            if user:
                user_id, stored_hash, salt = user
                test_hash, _ = self._hash_password(password, salt)
                if test_hash == stored_hash:
                    return {"id": user_id, "username": username}
            return None

    def log_action(self, user_id, action):
        """Registra uma ação realizada pelo usuário."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO user_actions (user_id, action) VALUES (?, ?)",
                    (user_id, action)
                )
                conn.commit()
        except Exception as e:
            print(f"Erro ao logar ação: {e}")

    def get_user_logs(self, user_id, limit=50):
        """Retorna os logs de ações mais recentes de um usuário."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT action, timestamp FROM user_actions WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
                (user_id, limit)
            )
            return cursor.fetchall()

if __name__ == "__main__":
    # Teste básico
    db = UserDB()
    # db.register_user("admin", "1234")
    user = db.authenticate_user("admin", "1234")
    if user:
        print(f"Autenticado: {user}")
        db.log_action(user['id'], "Teste de Login")
        print("Log registrado.")
    else:
        print("Falha na autenticação ou usuário não registrado.")
