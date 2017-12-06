from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/scanner')
def scanner():
    return render_template('scanner.html')

@app.route('/ourproduct')
def ourproduct():
    return render_template('ourproduct.html')

@app.route('/popularitem')
def popularitem():
    return render_template('popularitem.html')

@app.route('/healthyrecipe')
def healthyrecipe():
    return render_template('healthyrecipe.html')

@app.route('/healthevent')
def healthevent():
    return render_template('healthevent.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    app.run()

