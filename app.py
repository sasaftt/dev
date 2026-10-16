"""RappelVocal - service de rappel de rendez-vous par appel.

Appelle un client pour lui rappeler son rendez-vous, avec un menu simple :
1 = je confirme, 2 = je dois reporter, 3 = rappel humain souhaité.
"""

import os

from fastapi import FastAPI, Request, Response

app = FastAPI(title="RappelVocal")

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "")


@app.post("/call")
async def call(request: Request) -> dict:
    """Lance un appel de rappel vers le numéro indiqué."""
    body = await request.json()
    to = body["to"]
    rdv = body["rdv"]  # ex. "mardi 20 octobre à 14h30, 12 rue des Lilas"
    # Appel Twilio : le TwiML est servi par /twiml ci-dessous.
    import urllib.request
    import urllib.parse

    data = urllib.parse.urlencode({
        "To": to,
        "From": FROM_NUMBER,
        "Url": f"{body['public_url']}/twiml?rdv={urllib.parse.quote(rdv)}",
    }).encode()
    req = urllib.request.Request(
        f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Calls.json",
        data=data,
        auth=(TWILIO_SID, TWILIO_TOKEN),
    )
    with urllib.request.urlopen(req) as r:
        return {"status": "appelé", "reponse": r.read().decode()}


@app.api_route("/twiml", methods=["GET", "POST"])
async def twiml(request: Request) -> Response:
    """TwiML joué au client : rappel du rendez-vous + menu de confirmation."""
    rdv = request.query_params.get("rdv", "votre rendez-vous")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say language="fr-FR">Bonjour, ceci est un rappel pour votre rendez-vous : {rdv}.</Say>
  <Gather numDigits="1" action="/confirme" method="POST">
    <Say language="fr-FR">Appuyez sur un pour confirmer, deux pour reporter,
    trois pour être rappelé par un conseiller.</Say>
  </Gather>
</Response>"""
    return Response(content=xml, media_type="text/xml")


@app.post("/confirme")
async def confirme(request: Request) -> Response:
    form = await request.form()
    touche = form.get("Digits", "")
    reponses = {"1": "confirme", "2": "reporte", "3": "rappel humain"}
    resultat = reponses.get(touche, "sans réponse")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say language="fr-FR">Merci, votre réponse a été enregistrée. Au revoir.</Say>
</Response>"""
    # TODO : journaliser {resultat} pour le rapport au professionnel.
    return Response(content=xml, media_type="text/xml")
