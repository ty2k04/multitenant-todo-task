import os, time
import mysql.connector

def config():
    return {"host": os.getenv("DB_HOST", "localhost"), "database": os.getenv("DB_NAME", "todo_app"), "user": os.getenv("DB_USER", "todo_user"), "password": os.getenv("DB_PASSWORD", "todo_password")}

def process_once():
    connection = mysql.connector.connect(**config()); cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, user_id, title FROM todos WHERE notified=0 ORDER BY id LIMIT 50"); todos = cursor.fetchall()
    for todo in todos:
        cursor.execute("INSERT INTO notifications (user_id, message) VALUES (%s, %s)", (todo["user_id"], f"Todo created: {todo['title']}"))
        cursor.execute("UPDATE todos SET notified=1 WHERE id=%s", (todo["id"],))
    connection.commit(); cursor.close(); connection.close(); return len(todos)

def main():
    while True:
        try: process_once()
        except mysql.connector.Error as error: print(f"worker database retry: {error}", flush=True)
        time.sleep(int(os.getenv("POLL_SECONDS", "5")))

if __name__ == "__main__": main()

