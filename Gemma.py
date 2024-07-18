import ollama

class Gemma:
  _inistance = None
  # 实现单例模式
  def __new__(cls, *args, **kwargs):
    if not cls._inistance:
      cls._inistance = super(Gemma, cls).__new__(cls)
    return cls._inistance
  
  def __init__(self, model='gemma2:9b'):
    self.model = model
    self.client = ollama.Client(host='http://localhost:11434')

  def chat(self, message):
    response = self.client.chat(model=self.model, messages=[
      {
        'role': 'user',
        'content': message,
      }
    ])
    return response['message']['content']