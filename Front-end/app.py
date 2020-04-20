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
## Create cursor

       # cur = mysql.connection.cursor()

        #Get user by username

       # result = cur.execute("SELECT * FROM users WHERE username = %s" ,[username])
#

#traitement de login page
@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        courriel = request.form['courriel']
        passe = request.form['password']
        conn = pymysql.connect(host='localhost', user='root', password='tomato', db='mydb')

        cmd = "SELECT motpasse FROM utilisateurs WHERE courriel= %s"['courriel']
        cur = conn.cursor()
        cur.execute(cmd)
        passeVrai = cur.fetchone()

        if (passeVrai != None) and (passe == passeVrai[0]):
            cmd = "SELECT * FROM utilisateurs WHERE courriel= %s"['courriel']
            cur = conn.cursor()
            cur.execute(cmd)
            info = cur.fetchone()
            global ProfileUtilisateur
            ProfileUtilisateur["courriel"] = courriel
            ProfileUtilisateur["nom"] = info[2]
            #ProfileUtilisateur["avatar"] = info[3]
            return render_template('Profil-utilisateur.html', profile=ProfileUtilisateur)#crée la page profil utilisateurs
    return render_template('login.html', message="Informations invalides!")


@app.route('/resultats-recherches')
def resultat_recherches():
    return render_template('Resultats-recherches.html')

@app.route('/Abonnement')
def Abonnement():
    return render_template('Abonnement.html')

@app.route('/Recherche-avancee', methods=['GET'])
def recherche_avancee():
    return render_template('Recherche-avancee.html')

if __name__ == "__main__":
    app.run(debug=True)
