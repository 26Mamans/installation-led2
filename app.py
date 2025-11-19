from flask import Flask, request, redirect, url_for, render_template
import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials
import json
import requests

app = Flask(__name__)

# ---------------- GOOGLE SHEETS ----------------
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Credentials depuis variable d'environnement Render
google_creds_json = os.environ.get("GOOGLE_CREDS")
if not google_creds_json:
    raise Exception("Variable d'environnement GOOGLE_CREDS manquante !")

creds_dict = json.loads(google_creds_json)
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
gc = gspread.authorize(creds)

# Google Sheet ID (pas le pubhtml)
SHEET_ID = "TON_SHEET_ID_ICI"
sheet = gc.open_by_key(SHEET_ID).sheet1

# ---------------- EXCEL LOCAL ----------------
EXCEL_PATH = "leads.xlsx"
if not os.path.exists(EXCEL_PATH):
    df = pd.DataFrame(columns=[
        "Nom", "Prénom", "Email", "Téléphone",
        "Code Postal", "Endroit", "Surface (m2)", "Détails"
    ])
    df.to_excel(EXCEL_PATH, index=False)


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

    # --- SAUVEGARDE EXCEL ---
    df = pd.read_excel(EXCEL_PATH)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_excel(EXCEL_PATH, index=False)

    # --- SAUVEGARDE GOOGLE SHEETS ---
    sheet.append_row(list(data.values()))

    # --- DISCORD (optionnel) ---
    discord_webhook_url = os.environ.get("DISCORD_WEBHOOK")  # mettre webhook en variable Render
    if discord_webhook_url:
        requests.post(discord_webhook_url, json={"content": f"Nouvelle soumission: {data}"})

    return redirect(url_for("thank_you"))


@app.route('/thank_you')
def thank_you():
    return "<h1>Merci ! Les données ont été enregistrées ✅</h1>"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
