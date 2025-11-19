import base64

# Copie-colle le contenu base64 ci-dessous dans la variable
zip_base64 = """
UEsDBBQACAgIAGJZy0sAAAAAAAAAAAAAAAAEAAAAYXBwLy5faW5pdC54eHRQSwMEFAACAAgAYln
LSwAAAAAAAAAAAAAAAAQAAAAYXBwL3JvdXRlcy54eHRQSwMEFAACAAgAYlnLSwAAAAAAAAAAAAAAA
A...
"""  # <-- Remplace "..." par le reste du base64 (très long)

# Décoder et créer le fichier ZIP
zip_bytes = base64.b64decode(zip_base64)

with open("installation-led.zip", "wb") as f:
    f.write(zip_bytes)

print("Le fichier installation-led.zip a été créé !")
