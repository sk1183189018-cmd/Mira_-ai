"""
SQLite database layer for MIRA memory.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from threading import RLock


class MemoryDatabase:
    def __init__(self, database_path: str) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._lock = RLock()

        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.database_path,
            check_same_thread=False,
        )

        connection.row_factory = sqlite3.Row

        return connection

    def _initialize(self) -> None:
        with self._lock:
            with self._connect() as connection:
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS memories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category TEXT NOT NULL,
                        content TEXT NOT NULL,
                        importance INTEGER NOT NULL DEFAULT 1,
                        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )

                connection.execute(
                    """
                    CREATE INDEX IF NOT EXISTS
                    idx_memories_category
                    ON memories(category)
                    """
                )

                connection.commit()

    def add_memory(
        self,
        category: str,
        content: str,
        importance: int = 1,
    ) -> int:
        with self._lock:
            with self._connect() as connection:
                cursor = connection.execute(
                    """
                    INSERT INTO memories (
                        category,
                        content,
                        importance
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        category,
                        content,
                        importance,
                    ),
                )

                connection.commit()

                return int(cursor.lastrowid)

    def search_memories(
        self,
        query: str,
        limit: int = 10,
    ) -> list[dict]:
        with self._lock:
            with self._connect() as connection:
                cursor = connection.execute(
                    """
                    SELECT
                        id,
                        category,
                        content,
                        importance,
                        created_at,
                        updated_at
                    FROM memories
                    WHERE content LIKE ?
                    ORDER BY
                        importance DESC,
                        created_at DESC
                    LIMIT ?
                    """,
                    (
                        f"%{query}%",
                        limit,
                    ),
                )

                return [
                    dict(row)
                    for row in cursor.fetchall()
                ]

    def get_recent(
        self,
        limit: int = 20,
    ) -> list[dict]:
        with self._lock:
            with self._connect() as connection:
                cursor = connection.execute(
                    """
                    SELECT
                        id,
                        category,
                        content,
                        importance,
                        created_at
                    FROM memories
                    ORDER BY created_at DESC
                    LIMIT ?
                    """,
                    (limit,),
                )

                return [
                    dict(row)
                    for row in cursor.fetchall()
                ]

    def delete_memory(
        self,
        memory_id: int,
    ) -> bool:
        with self._lock:
            with self._connect() as connection:
                cursor = connection.execute(
                    """
                    DELETE FROM memories
                    WHERE id = ?
                    """,
                    (memory_id,),
                )

                connection.commit()

                return cursor.rowcount > 0

    def clear_all(self) -> None:
        with self._lock:
            with self._connect() as connection:
                connection.execute(
                    "DELETE FROM memories"
                )

                connection.commit()
