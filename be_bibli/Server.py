from flask import Flask, render_template, request
from Research_form import researchForm
from Main import research

app = Flask(__name__)
app.config['SECRET_KEY'] = "password"

@app.route('/')
def accueil():
    return render_template('Accueil.html')

@app.route('/profile/<int:user_id>')
def profile(user_id):
    return 'this is user' + str(user_id)

@app.route("/Recherche",methods=['GET', 'POST'])
def recherche():
    form = researchForm()
    if form.is_submitted():
        result = request.form
        research(request.form.getlist('research')[0])
        return render_template('Resultats-recherche.html', result=result)
    return render_template('Recherche.html', form=form)

@app.route("/nous-joindre",methods=['GET'])
def nous_joindre():
    return render_template('Nous-joindre.html')


#load login page
@app.route("/se-connecter", methods=['GET'])
def se_connecter():
    return render_template('Se-connecter.html')

@app.route('/resultats-recherche')
def resultats_recherche():
    return render_template('Resultats-recherche.html')

@app.route('/abonnement')
def abonnement():
    return render_template('Abonnement.html')

@app.route('/Recherche-avancee', methods=['GET'])
def recherche_avancee():
    return render_template('Recherche-avancee.html')

#traitement de login page
#@app.route("/login", methods=['POST'])
#def login():
 #   if request.method == 'POST':
  #      courriel = request.form['courriel']
   #     passe = request.form['password']
    #    conn = pymysql.connect(host='localhost', user='root', password='tomato', db='library')
#
 #       cmd = "SELECT motpasse FROM utilisateurs WHERE courriel= %s"['courriel']
  #      cur = conn.cursor()
   #     cur.execute(cmd)
    #    passeVrai = cur.fetchone()
#
 #       if (passeVrai != None) and (passe == passeVrai[0]):
  #          cmd = "SELECT * FROM utilisateurs WHERE courriel= %s"['courriel']
   #         cur = conn.cursor()
    #        cur.execute(cmd)
     #       info = cur.fetchone()
      #      global ProfileUtilisateur
       #     ProfileUtilisateur["courriel"] = courriel
        #    ProfileUtilisateur["nom"] = info[2]
         #   #ProfileUtilisateur["avatar"] = info[3]
          #  return render_template('Profil-utilisateur.html', profile=ProfileUtilisateur)#crée la page profil utilisateurs
    #return render_template('login.html', message="Informations invalides!")



if __name__=='__main__':
    app.run()

