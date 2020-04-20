import pymysql
import pymysql.cursors
from flask import Flask, render_template, request

app = Flask(__name__)
ProfileUtilisateur = {}


# the main URL of the application mapping page d'acceuil
@app.route("/")
def Accueil():
    return render_template('Accueil.html')


@app.route("/recherche",methods=['GET'])
def Recherche():
    return render_template('Recherche.html')

@app.route("/nous-joindre",methods=['GET'])
def page_joindre():
    return render_template('Nous-joindre.html')


#load login page
@app.route("/page-login", methods=['GET'])
def page_de_login():
    return render_template('Se-connecter.html')


#traitement de login page
@app.route("/login", methods=['POST','GET'])
def login():
    courriel = '"' + request.form.get('courriel') + '"'
    passe = request.form.get('motpasse')

    conn = pymysql.connect(host='localhost', user='root', password='tomato', db='mydb')
    cmd = 'SELECT motpasse FROM utilisateurs WHERE courriel=' + courriel + ';'
    cur = conn.cursor()
    cur.execute(cmd)
    passeVrai = cur.fetchone()
    if (passeVrai != None) and (passe == passeVrai[0]):
        cmd = 'SELECT * FROM utilisateurs WHERE courriel=' + courriel + ';'
        cur = conn.cursor()
        cur.execute(cmd)
        info = cur.fetchone()
        global ProfileUtilisateur
        ProfileUtilisateur["courriel"] = courriel
        ProfileUtilisateur["nom"] = info[2]
        ProfileUtilisateur["avatar"] = info[3]
        return render_template('bienvenu.html', profile=ProfileUtilisateur)

    return render_template('login.html', message="Informations invalides!")


if __name__ == "__main__":
    app.run(debug=True)
