from flask import Flask, request, redirect, url_for, render_template
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# --- GOOGLE SHEETS ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# Récupérer la clé JSON depuis une variable d'environnement
import os, json
creds_info = json.loads(os.environ.get("GOOGLE_CREDENTIALS_JSON"))
creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
gc = gspread.authorize(creds)

SHEET = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vT_SSgZErgKHyjQPtXa0dCep8jEnEYsAKqXqcNePdtlNWLs6mMy9MJbQrKB2Sy0mJCkNac7s6qHlaoS/pubhtml?gid=0"
).sheet1

@app.route('/')
def index():
    return render_template('formulaire.html')

@app.route('/submit', methods=['POST'])
def submit():
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
    row = list(data.values())
    SHEET.append_row(row)
    return redirect(url_for("thank_you"))

@app.route('/thank_you')
def thank_you():
    return "<h1>Merci ! Les données ont été enregistrées ✅</h1>"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
