
import sqlite3
import json

from pathlib import Path
from datetime import datetime, timezone


# Database location
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "writing_assistant.db"


class DatabaseManager:

    def __init__(self):
        self.create_tables()

    def get_connection(self):

        return sqlite3.connect(DB_PATH)

    # Create database table
    def create_tables(self):

        with self.get_connection() as connection:

            connection.execute("""
                CREATE TABLE IF NOT EXISTS generations (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    task TEXT NOT NULL,

                    user_input TEXT NOT NULL,

                    generated_content TEXT NOT NULL,

                    tone TEXT,

                    output_length TEXT,

                    evaluation TEXT,

                    latency REAL,

                    model TEXT,

                    created_at TEXT NOT NULL

                )
            """)

    # Save generated content
    def save_generation(
        self,
        task,
        user_input,
        generated_content,
        tone=None,
        output_length=None,
        evaluation=None,
        latency=None,
        model=None
    ):

        created_at = datetime.now(
            timezone.utc
        ).isoformat()

        evaluation_data = (
            json.dumps(evaluation)
            if evaluation is not None
            else None
        )

        with self.get_connection() as connection:

            cursor = connection.execute("""
                INSERT INTO generations (
                    task,
                    user_input,
                    generated_content,
                    tone,
                    output_length,
                    evaluation,
                    latency,
                    model,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task,
                user_input,
                generated_content,
                tone,
                output_length,
                evaluation_data,
                latency,
                model,
                created_at
            ))

            return cursor.lastrowid

    # Retrieve generation history
    def get_history(self, limit=50):

        with self.get_connection() as connection:

            connection.row_factory = sqlite3.Row

            rows = connection.execute("""
                SELECT *
                FROM generations
                ORDER BY id DESC
                LIMIT ?
            """, (limit,)).fetchall()

            return [dict(row) for row in rows]

    # Search previous generations
    def search_history(self, keyword):

        with self.get_connection() as connection:

            connection.row_factory = sqlite3.Row

            rows = connection.execute("""
                SELECT *
                FROM generations
                WHERE task LIKE ?
                   OR user_input LIKE ?
                   OR generated_content LIKE ?
                ORDER BY id DESC
            """, (
                f"%{keyword}%",
                f"%{keyword}%",
                f"%{keyword}%"
            )).fetchall()

            return [dict(row) for row in rows]

    # Delete a generation
    def delete_generation(self, generation_id):

        with self.get_connection() as connection:

            connection.execute("""
                DELETE FROM generations
                WHERE id = ?
            """, (generation_id,))
            
    def update_evaluation(self, generation_id, evaluation):

        with self.get_connection() as connection:

            connection.execute("""
                UPDATE generations
                SET evaluation = ?
                WHERE id = ?
            """, (
                json.dumps(evaluation),
                generation_id
            ))
    