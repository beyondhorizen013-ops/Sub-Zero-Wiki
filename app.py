from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# This is our "Database" file
DB_FILE = 'wiki_data.json'

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/')
def home():
    data = load_data()
    return render_template('home.html', articles=data.keys())

@app.route('/wiki/<name>')
def view_article(name):
    data = load_data()
    article = data.get(name)
    if not article:
        return f"<h1>Article not found</h1><p><a href='/edit/{name}'>Create this page</a></p>"
    return render_template('wiki.html', name=name, content=article)

@app.route('/edit/<name>', methods=['GET', 'POST'])
def edit_article(name):
    data = load_data()
    if request.method == 'POST':
        data[name] = request.form['content']
        save_data(data)
        return redirect(url_for('view_article', name=name))
    
    current_content = data.get(name, "")
    return render_template('edit.html', name=name, content=current_content)

if __name__ == "__main__":
    app.run(debug=True)
