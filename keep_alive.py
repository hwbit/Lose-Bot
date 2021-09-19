from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def index():
  return "Bot is alive!"

app.run(host='0.0.0.0', port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()