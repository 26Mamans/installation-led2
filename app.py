from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
from discord_webhook import DiscordWebhook, DiscordEmbed

app = Flask(__name__)

# Fichier Excel pour sauvegarder les demandes
EXCEL_FILE = os.path.join(os.getcwd(), "data.xlsx")

# Ton webhook Discord
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1420723717440540725/PPWGm_2WDVZgxIJQSTek7wJZXBzPyCy1YrDjxWk6uuW0YcATMfqRjb489TwYRatlKnPg"

# Fonction pour envoyer la notification Discord
def send_discord_notification(data):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)
    
    embed = DiscordEmbed(title="💡 Nouvelle demande LED !", color='03b2f8')
    embed.add_embed_field(name="Nom", value=f"{data['Nom']} {data['Prénom']}", inline=False)
    embed.add_embed_field(name="Email", value=data['Email'], inline=False)
    embed.add_embed_field(name="Téléphone", value=data['Téléphone'], inline=False)
    embed.add_embed_field(name="Code Postal", value=data['Code Postal'], inline=False)
    embed.add_embed_field(name="Lieu", value=data['Endroit'], inline=False)
    embed.add_embed_field(name="Surface", value=data['Surface (m2)'], inline=False)
    embed.add_embed_field(name="Détails", value=data['Détails'], inline=False)
    
    webhook.add_embed(embed)
    
    try:
        response = webhook.execute()
        print("Notification Discord envoyée ✅", response)
    except Exception as e:
        print("Erreur en envoyant Discord:", e)
        # Optionnel : log dans un fichier fallback
        with open("discord_error.log", "a", encoding="utf-8") as f:
            f.write(f"{data}\nErreur: {e}\n\n")

# Route principale avec formulaire
@app.route('/')
def index():
    return render_template('formulaire.html')  # Ton formulaire HTML

# Route de soumission du formulaire
@app.route('/submit', methods=['POST'])
def submit():
    # Récupérer les données du formulaire
    data = {
        "Nom": request.form.get('nom'),
        "Prénom": request.form.get('prenom'),
        "Email": request.form.get('email'),
        "Téléphone": request.form.get('tel'),
        "Code Postal": request.form.get('postal'),
        "Endroit": request.form.get('endroit'),
        "Surface (m2)": request.form.get('surface'),
        "Détails": request.form.get('details')
    }

    # Sauvegarder dans Excel
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    else:
        df = pd.DataFrame([data])
    df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

    # Envoyer notification Discord
    send_discord_notification(data)

    # Redirection vers page de confirmation
    return redirect(url_for('thank_you'))

# Page de confirmation
@app.route('/thank_you')
def thank_you():
    return "<h1>Merci ! Votre demande a été envoyée ✅</h1>"

# Lancer le serveur
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
