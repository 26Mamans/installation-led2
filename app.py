from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('formulaire.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Ici on ne fait rien, juste rediriger vers merci
    return "<h1>Merci ! Votre formulaire a été soumis ✅</h1>"

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
