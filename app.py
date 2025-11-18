from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# Chemin du fichier Excel dans le répertoire courant
EXCEL_FILE = os.path.join(os.getcwd(), "data.xlsx")

@app.route('/')
def index():
    return render_template('formulaire.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Récupération des données du formulaire
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    email = request.form.get('email')
    tel = request.form.get('tel')
    postal = request.form.get('postal')
    endroit = request.form.get('endroit')
    surface = request.form.get('surface')
    details = request.form.get('details')

    # Création de la nouvelle ligne à ajouter
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

    # Vérifie si le fichier existe, sinon crée un nouveau DataFrame
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    # Sauvegarde dans Excel
    df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

    # Redirection vers une page "merci"
    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return "<h1>Merci ! Votre demande a bien été envoyée ✅</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
