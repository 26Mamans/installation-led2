from flask import Flask, request, send_from_directory
import pandas as pd
import os

app = Flask(__name__)

EXCEL_FILE = "leads.xlsx"

# Création du fichier Excel s'il n'existe pas
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=[
        "Nom", "Prénom", "Email", "Téléphone", "Code Postal",
        "Endroit", "Surface (m2)", "Détails"
    ])
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/')
def home():
    return send_from_directory('.', 'leads.html')

@app.route('/submit', methods=['POST'])
def submit():
    nom = request.form.get("nom")
    prenom = request.form.get("prenom")
    email = request.form.get("email")
    tel = request.form.get("tel")
    postal = request.form.get("postal")
    endroit = request.form.get("endroit")
    surface = request.form.get("surface")
    details = request.form.get("details")

    df = pd.read_excel(EXCEL_FILE)

    new_row = {
        "Nom": nom,
        "Prénom": prenom,
        "Email": email,
        "Téléphone": tel,
        "Code Postal": postal,
        "Endroit": endroit,
        "Surface (m2)": surface,
        "Détails": details
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

    return "<h2>Merci ! Nous vous contacterons très vite pour votre installation LED. 💡</h2>"

if __name__ == "__main__":
    app.run(debug=True)
