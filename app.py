from flask import Flask, request, render_template, redirect, url_for
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1420723717440540725/PPWGm_2WDVZgxIJQSTek7wJZXBzPyCy1YrDjxWk6uuW0YcATMfqRjb489TwYRatlKnPg"

@app.route('/')
def index():
    return render_template("formulaire.html")  # <-- ton fichier existant

@app.route('/submit', methods=['POST'])
def submit():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    email = request.form.get('email')
    telephone = request.form.get('telephone')
    surface = request.form.get('surface')

    message = f"""**Nouvelle demande d'éligibilité :**
Nom : {nom}
Prénom : {prenom}
Email professionnel : {email}
Téléphone : {telephone}
Surface du bâtiment : {surface} m²
"""

    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

    return redirect(url_for('merci'))

@app.route('/merci')
def merci():
    return "<h2>Merci ! Votre demande a bien été prise en compte.</h2>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
