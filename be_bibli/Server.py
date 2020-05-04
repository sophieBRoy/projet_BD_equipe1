from flask import Flask, render_template, request,redirect
from Research_form import researchForm
from log import LogForm
from Main import research, getBook, getMagazine

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
        formData = request.form.getlist('research')
        bookSelected = request.form.getlist('bookCheck')
        magazineSelected = request.form.getlist('magazineCheck')
        result = research(formData[0], len(bookSelected), len(magazineSelected))
        return render_template('Resultats-recherche.html', result=result)
    return render_template('Recherche.html', form=form)

#load login page
@app.route("/se-connecter", methods=['GET','POST'])
def se_connecter():
    form = LogForm()
    if form.is_submitted():
        result = request.form
        #courrielSaisie = request.form.getlist('nomUser')
        #MdpSaisie = request.form.getlist('passUser')
        #fonction qui traite les saisie
        return render_template('Profil_utilisateur.html', result=result)
    return render_template('Se-connecter.html', form=form)

@app.route("/nous-joindre",methods=['GET'])
def nous_joindre():
    return render_template('Nous-joindre.html')

@app.route("/books",methods=['GET'])
def books():
    result = research('', 1, 0)
    return render_template('Resultats-recherche.html', result=result)

@app.route("/magazines",methods=['GET'])
def magazines():
    result = research('', 0, 1)
    return render_template('Resultats-recherche.html', result=result)

@app.route("/Profil_utilisateur.html")
def utilisateur():
    return render_template('Profil_utilisateur.html')

@app.route('/resultats-recherche')
def resultats_recherche():
    return render_template('Resultats-recherche.html')

@app.route('/abonnement')
def abonnement():
    return render_template('Abonnement.html')

@app.route('/Recherche-avancee', methods=['GET'])
def recherche_avancee():
    return render_template('Recherche-avancee.html')

@app.route('/location/<bookId>', methods=['GET'])
def location(bookId):
    result = getBook(bookId)
    return render_template('Location.html', result=result)


if __name__=='__main__':
    app.run(debug=True)

