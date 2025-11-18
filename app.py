from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

EXCEL_FILE = os.path.join(os.getcwd(), "data.xlsx")

@app.route('/')
def index():
    return render_template('formulaire.html')

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

    # Lire ou créer le fichier Excel
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    else:
        df = pd.DataFrame([data])

    # Sauvegarder
    df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

    # Redirection vers la page de confirmation
    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return "<h1>Merci ! Votre demande a été envoyée ✅</h1>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
