from flask import Flask, request, redirect, url_for, render_template
import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials
import requests  # pour Discord si nécessaire

app = Flask(__name__)

# --- GOOGLE SHEETS ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
gc = gspread.authorize(creds)
SHEET = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vT_SSgZErgKHyjQPtXa0dCep8jEnEYsAKqXqcNePdtlNWLs6mMy9MJbQrKB2Sy0mJCkNac7s6qHlaoS/pubhtml?gid=0"
).sheet1

# --- EXCEL LOCAL ---
EXCEL_PATH = "leads.xlsx"
if not os.path.exists(EXCEL_PATH):
    df = pd.DataFrame(columns=["Nom", "Prénom", "Email", "Téléphone", "Code Postal", "Endroit", "Surface (m2)", "Détails"])
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
    row = list(data.values())
    SHEET.append_row(row)

    return redirect(url_for("thank_you"))

@app.route('/thank_you')
def thank_you():
    return "<h1>Merci ! Les données ont été enregistrées ✅</h1>"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
