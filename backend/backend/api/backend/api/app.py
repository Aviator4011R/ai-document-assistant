from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "It works! Flask is live on Vercel."

if __name__ == "__main__":
    app.run()
