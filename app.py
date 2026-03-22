from flask import Flask, render_template, request, abort
import requests

app = Flask(__name__)

# This function grabs the GitHub data
def get_github_stats(username):
    response = requests.get(f"https://api.github.com/users/{username}")
    if response.status_code == 200:
        return response.json()
    return None

@app.route('/')
def home():
    # A simple landing page where people can type a username
    return '''
        <h1>Welcome to Sub-Zero Wiki</h1>
        <p>The encyclopedia for people who aren't famous.</p>
        <form action="/check" method="get">
            <input type="text" name="username" placeholder="Enter GitHub Username">
            <button type="submit">Generate Wiki</button>
        </form>
    '''

@app.route('/check')
def check_notability():
    username = request.args.get('username')
    data = get_github_stats(username)

    if not data:
        return "<h1>404: Person too obscure even for us.</h1>", 404

    # THE JOKE: If they have more than 500 followers, they are "too famous"
    followers = data.get('followers', 0)
    if followers > 500:
        return f"<h1>Access Denied</h1><p>{username} has {followers} followers. That's too many. Go to the real Wikipedia, celebrity.</p>", 403

    # If they pass the "non-notable" test, show them their wiki
    return f'''
        <div style="font-family: serif; max-width: 800px; margin: auto; border: 1px solid #ccc; padding: 20px;">
            <h1 style="border-bottom: 1px solid #aaa;">{data.get('name') or username}</h1>
            <p><i>From Sub-Zero, the encyclopedia for the rest of us.</i></p>
            
            <p><b>{data.get('name') or username}</b> is a GitHub user known for having exactly <b>{followers}</b> followers. 
            They currently reside in <b>{data.get('location') or 'an undisclosed location'}</b>.</p>
            
            <h3>History</h3>
            <p>Subject has created {data.get('public_repos')} repositories. Most of which remain unstarred by anyone other than their mother.</p>
            
            <div style="float: right; border: 1px solid #aaa; padding: 10px; background: #f9f9f9;">
                <img src="{data.get('avatar_url')}" width="150"><br>
                <b>Status:</b> Non-Notable<br>
                <b>Clout Score:</b> Very Low
            </div>
        </div>
    '''

if __name__ == "__main__":
    app.run(debug=True)
