from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

EXCEL_FILE = "data.xlsx"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Récupérer toutes les données du formulaire
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        email = request.form.get("email")
        tel = request.form.get("tel")
        postal = request.form.get("postal")
        endroit = request.form.get("endroit")
        surface = request.form.get("surface")
        details = request.form.get("details")

        # Créer un dictionnaire avec toutes les données
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

        # Transformer en DataFrame
        df = pd.DataFrame([new_row])

        # Ajouter au fichier existant si il existe
        if os.path.exists(EXCEL_FILE):
            df_existing = pd.read_excel(EXCEL_FILE, engine="openpyxl")
            df = pd.concat([df_existing, df], ignore_index=True)

        # Sauvegarder dans Excel
        df.to_excel(EXCEL_FILE, index=False, engine="openpyxl")

        return "Formulaire reçu et sauvegardé ! ✅"

    # GET → afficher le formulaire
    return render_template("formulaire.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
