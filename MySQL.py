import mysql.connector

class MySQL:
  _instance = None
  # 实现单例模式
  def __new__(cls, *args, **kwargs):
    if not cls._instance:
      cls._instance = super(MySQL, cls).__new__(cls)
    return cls._instance

  def __init__(self, host='localhost', user='root', password='123456', database='database'):
    self.host = host
    self.user = user
    self.password = password
    self.database = database
    self.connection = self.get_connection()
    self.cursor = self.connection.cursor()
    self.create_table()

  def get_connection(self):
    return mysql.connector.connect(
      host=self.host,
      user=self.user,
      password=self.password,
      database=self.database
    )

  def create_table(self):
    self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
          id INT AUTO_INCREMENT PRIMARY KEY,
          date DATE,
          title VARCHAR(255),
          description TEXT,
          notes TEXT
        )
    ''')
    self.connection.commit()

  def insert(self, date, title, description, notes=''):
    self.cursor.execute('''
        INSERT INTO news (date, title, description, notes)
        VALUES (%s, %s, %s, %s)
    ''', (date, title, description, notes))
    self.connection.commit()

  def get_all_news(self):
    self.cursor.execute("SELECT * FROM news")
    news = self.cursor.fetchall()
    return news

  def get_news_by_id(self, news_id):
    self.cursor.execute("SELECT * FROM news WHERE id = %s", (news_id,))
    news = self.cursor.fetchone()
    return news
  
  def get_news_by_ids(self, news_ids):
    news_ids_string = ', '.join(['%s'] * len(news_ids))
    query = f"SELECT * FROM news WHERE id IN ({news_ids_string})"
    self.cursor.execute(query, tuple(news_ids))
    return self.cursor.fetchall()
  
  def get_news_ids_by_date(self, date):
    self.cursor.execute("SELECT id FROM news WHERE date=?", (date,))
    return [row[0] for row in self.cursor.fetchall()]
  
  def get_news_by_dates(self, dates):
    dates_string = ', '.join(['%s'] * len(dates))
    query = f"SELECT id FROM news WHERE date IN ({dates_string})"
    self.cursor.execute(query, tuple(dates))
    return [row[0] for row in self.cursor.fetchall()]
  
  def update_news_notes(self, news_id, notes):
    self.cursor.execute("UPDATE news SET notes = %s WHERE id = %s", (notes, news_id))
    self.connection.commit()

  def delete_news(self, news_id):
    self.cursor.execute("DELETE FROM news WHERE id = %s", (news_id,))
    self.connection.commit()

  def delete_all(self):
    self.cursor.execute("DELETE FROM news")
    self.connection.commit()