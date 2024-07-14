from flask import Flask, request, jsonify, render_template, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'info@sauber-weg.de'
app.config['MAIL_PASSWORD'] = os.getenv('TRANSPORTER_PASSWORD')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/agb')
def agb():
    return render_template('agb.html')

@app.route('/impressum')
def impressum():
    return render_template('impressum.html')

@app.route('/datenschutz')
def datenschutz():
    return render_template('datenschutz.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.json
    print(data)
    jetzt = data[0]['Jetzt']
    email = data[0]['email']
    first_name = data[0]['firstName']
    last_name = data[0]['lastName']
    message = data[0]['message']
    print(jetzt, email, first_name, last_name, message)
    
    email_text = f'Vorname: {first_name}\nZuname: {last_name}\nEmail-Adresse: {email}\nNachricht: {message}\n'

    if jetzt == 'Umzug':
        stratort = data[0]['Stratort']
        zielort = data[0]['zielort']
        datum = data[0]['datum']
        anzahl = data[0]['anzahl']
        quadratmeter = data[0]['quadratmeter']
        umzug_art = data[0]['umzugArt']
        kostentraeger = data[0]['kostentraeger']
        email_text += f'Jetzt: {jetzt}\nStratort: {stratort}\nZielort: {zielort}\nDatum: {datum}\nAnzahl: {anzahl}\nQuadratmeter: {quadratmeter}\nUmzugArt: {umzug_art}\nKostentraeger: {kostentraeger}'
    elif jetzt == 'Entrumpelung':
        freigabetyp = data[0]['Freigabetyp']
        beschreibung = data[0]['Beschreibung']
        email_text += f'Jetzt: {jetzt}\nFreigabetyp: {freigabetyp}\nBeschreibung: {beschreibung}'

    msg = Message(subject="Thank you for your submission!",
                  sender="info@sauber-weg.de",
                  recipients=[email],
                  body=email_text)
    
    second_msg = Message(subject="Thank you for your submission!",
                         sender="info@sauber-weg.de",
                         recipients=["info@sauber-weg.de"],
                         body=email_text)

    try:
        mail.send(msg)
        mail.send(second_msg)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

@app.route('/submit_main', methods=['POST'])
def submit_main():
    data = request.json
    email = data[0]['email']
    first_name = data[0]['firstName']
    last_name = data[0]['lastName']
    message = data[0]['message']
    tel = data[0]['tel']

    email_text = f'Vorname: {first_name}\nZuname: {last_name}\nEmail-Adresse: {email}\nNachricht: {message}\nMobilfunknummer: {tel}'

    msg = Message(subject="Thank you for your submission!",
                  sender="info@sauber-weg.de",
                  recipients=[email],
                  body=email_text)
    
    second_msg = Message(subject="Thank you for your submission!",
                         sender="info@sauber-weg.de",
                         recipients=["info@sauber-weg.de"],
                         body=email_text)

    try:
        mail.send(msg)
        mail.send(second_msg)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
