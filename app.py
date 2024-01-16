from flask import Flask, render_template, request, redirect
import random
import string

app = Flask(__name__)
url_mapping = {}

def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']
    custom_alias = request.form['custom_alias'].strip()
    if custom_alias:
        if custom_alias in url_mapping:
            return render_template('index.html', error='Your alias already exists. Please choose another.')
        short_url = custom_alias
    else:
        short_url = generate_short_url()
    url_mapping[short_url] = long_url
    return render_template('index.html', short_url=short_url)

@app.route('/<short_url>')
def redirect_to_original(short_url):
    long_url = url_mapping.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return render_template('index.html', error='Short URL not found')

if __name__ == '__main__':
    app.run(debug=True)


