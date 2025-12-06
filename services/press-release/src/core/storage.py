import sqlite3
import json
from typing import List
from pathlib import Path
from .models import Article

DB_PATH = Path("db/scraper_pr.db")

class DocumentStore:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.ensure_tables()

    def ensure_tables(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            title TEXT,
            date TEXT,
            text TEXT,
            category TEXT,
            pdfs TEXT, -- JSON
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.conn.commit()

    def save_articles(self, articles: List[Article]) -> List[Article]:
        """
        Save only NEW articles. Return those new articles for Qdrant publishing.
        """
        new_articles = []
        cur = self.conn.cursor()

        for a in articles:
            try:
                cur.execute("""
                INSERT INTO articles (url, title, date, text, category, pdfs)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    a.url,
                    a.title,
                    a.date,
                    a.text,
                    a.category,
                    json.dumps(a.pdfs or []),
                ))
                self.conn.commit()
                new_articles.append(a)

            except sqlite3.IntegrityError:
                # URL already exists → skip (duplicate)
                pass

        return new_articles

    def get_all_articles(self) -> List[Article]:
        cur = self.conn.execute("SELECT * FROM articles ORDER BY created_at DESC")
        rows = cur.fetchall()
        return [
            Article(
                url=r["url"],
                title=r["title"],
                date=r["date"],
                text=r["text"],
                category=r["category"],
                pdfs=json.loads(r["pdfs"] or "[]"),
            )
            for r in rows
        ]
