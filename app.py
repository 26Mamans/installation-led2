from flask import Flask, request, redirect, url_for, render_template
import requests

app = Flask(__name__)

# --- CONFIGURATION DISCORD ---
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1420723717440540725/PPWGm_2WDVZgxIJQSTek7wJZXBzPyCy1YrDjxWk6uuW0YcATMfqRjb489TwYRatlKnPg"  # Remplace par ton webhook Discord

@app.route('/')
def index():
    return render_template('formulaire.html')  # Ton fichier HTML avec le formulaire

@app.route('/submit', methods=['POST'])
def submit():
    # Récupération des données du formulaire
    data = {
        "Nom": request.form.get('nom'),
        "Prénom": request.form.get('prenom'),
        "Email": request.form.get('email'),
        "Téléphone": request.form.get('tel'),
        "Surface": request.form.get('surface')
    }

    # --- ENVOI SUR DISCORD ---
    message = (
        f"Nouvelle demande d'éligibilité :\n"
        f"Nom : {data['Nom']}\n"
        f"Prénom : {data['Prénom']}\n"
        f"Email professionnel : {data['Email']}\n"
        f"Téléphone : {data['Téléphone']}\n"
        f"Surface : {data['Surface']}"
    )

    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print("Erreur lors de l'envoi sur Discord :", e)

    # --- REDIRECTION VERS LA PAGE DE REMERCIEMENT ---
    return redirect(url_for("thank_you"))

@app.route('/thank_you')
def thank_you():
    return "<h1>Merci ! Votre demande a bien été prise en compte ✅</h1>"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
