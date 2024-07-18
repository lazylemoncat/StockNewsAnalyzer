import sqlite3

class SQLite:
  _inistance = None
  # 实现单例模式
  def __new__(cls, *args, **kwargs):
    if not cls._inistance:
      cls._inistance = super(SQLite, cls).__new__(cls)
    return cls._inistance
  
  def __init__(self, db_path='database.db'):
    self.db_path = db_path
    self.connection = self.get_connection()
    self.cursor = self.connection.cursor()
    self.create_table()

  def get_connection(self):
    return sqlite3.connect(self.db_path)

  def create_table(self):
    self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          date TEXT,
          title TEXT,
          description TEXT,
          notes TEXT
        )
    ''')
    self.connection.commit()

  def insert(self, date, title, description, notes=''):
    self.cursor.execute('''
        INSERT INTO news (date, title, description, notes)
        VALUES (?, ?, ?, ?)
    ''', (date, title, description, notes))
    self.connection.commit()

  def get_all_news(self):
    self.cursor.execute("SELECT * FROM news")
    news = self.cursor.fetchall()
    return news

  def get_news_by_id(self, news_id):
    self.cursor.execute("SELECT * FROM news WHERE id = ?", (news_id,))
    news = self.cursor.fetchone()
    return news
  
  def get_news_by_ids(self, news_ids):
    news_ids_string = ', '.join(['?'] * len(news_ids))
    query = f"SELECT * FROM news WHERE id IN ({news_ids_string})"
    self.cursor.execute(query, news_ids)
    return self.cursor.fetchall()
  
  def get_news_ids_by_date(self, date):
    self.cursor.execute("SELECT id FROM news WHERE date=?", (date,))
    return [row[0] for row in self.cursor.fetchall()]
  
  def get_news_by_dates(self, dates):
    dates_string = ', '.join(['?'] * len(dates))
    query = f"SELECT id FROM news WHERE date IN ({dates_string})"
    self.cursor.execute(query, dates)
    return [row[0] for row in self.cursor.fetchall()]

  def update_news(self, news_id, date=None, title=None, description=None, notes=None):
    update_fields = []
    update_values = []

    if date:
      update_fields.append("date = ?")
      update_values.append(date)
    if title:
      update_fields.append("title = ?")
      update_values.append(title)
    if description:
      update_fields.append("description = ?")
      update_values.append(description)
    if notes:
      update_fields.append("notes = ?")
      update_values.append(notes)

    if update_fields:
      update_query = f"UPDATE news SET {', '.join(update_fields)} WHERE id = %s"
      self.cursor.execute(update_query, tuple(update_values))
      self.connection.commit()

  def delete_news(self, news_id):
    self.cursor.execute("DELETE FROM news WHERE id = ?", (news_id,))
    self.connection.commit()

  def delete_all(self):
    self.cursor.execute("DELETE FROM news")
    self.connection.commit()