from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def blocked_page():
    return render_template('blocked.html')

if __name__ == '__main__':
    app.run(port=5051)
