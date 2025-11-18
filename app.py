from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

EXCEL_FILE = "data.xlsx"  # Le fichier Excel où tu stockes les demandes

# Page principale avec le formulaire
@app.route('/')
def index():
    return render_template('formulaire.html')

# Route pour gérer le formulaire
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

    # Création de la nouvelle ligne
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

    # Lecture ou création du fichier Excel
    try:
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([new_row])

    # Enregistrement dans Excel
    df.to_excel(EXCEL_FILE, index=False)

    # Redirection vers la page principale après submission
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
