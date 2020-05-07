from flask import Flask, render_template, request,redirect,url_for
from Forms import researchForm, advancedResearchForm
from log import LogForm
from abonnement import AbonnementForm
from Main import research, advancedResearch, getBook, getAuthor, getBooksFromAuthor, GetInfoUtilisateur, SetUtilisateur,  GetUserId, getMagazine
from cryptography.fernet import Fernet
import os.path
app = Flask(__name__)
app.config['SECRET_KEY'] = "password"


courriel=""
motdePass=""
adminPass=""
resultat1=[]


@app.route('/')
def accueil():
    return render_template('Accueil.html')

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
    global courriel
    global motdePass
    message=""
    form = LogForm()
    if form.is_submitted():
        courriel = request.form.getlist('nomUser')
        motdePass = request.form.getlist('passUser')
        mdp = motdePass[0]
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        motdePassCrypted = cipher_suite.encrypt(bytes(mdp, encoding='utf8'))
        with open("keys.txt", "wb") as f:
            f.write(bytes(key))
        resultat= GetUserId(courriel[0], motdePassCrypted)

        if resultat is not False:
            resultat1.append(resultat[0])
            return redirect(url_for('utilisateur'))
        else:
            message += "veuillez saisir les données de nouveau"
    return render_template('Se-connecter.html', form=form, message=message)


@app.route('/abonnement',  methods=['GET','POST'])
def abonnement():
    message = " "
    form = AbonnementForm()
    if form.is_submitted():
        nom = request.form.getlist('nomUtilisateurs')
        prenom = request.form.getlist('prenomUtilisateurs')
        age = request.form.getlist('utilisateursAge')
        numero= request.form.getlist('utilisateursAddresseNumero')
        rue = request.form.getlist('utilisateursAddresseRue')
        code = request.form.getlist('utilisateursAddresseCode')
        email = request.form.getlist('utilisateursCourriel')
        password = request.form.getlist('utilisateursMdp')
        #fonction qui traite les entrée
        result = SetUtilisateur(nom[0], prenom[0], age[0], numero[0], rue[0], code[0],  email[0], password[0])
        print(result)
        if result is True:
            return redirect(url_for('accueil'))
        else:
            message += "il y'a des champs vides, veuillez remplir tous les champs"
            return render_template('Abonnement.html', form=form, message=message)

    return render_template('Abonnement.html', form = form)


@app.route("/Profil_utilisateur")
def utilisateur():
    resultat=[]
    resultat += GetInfoUtilisateur(resultat1[0])
    return render_template('Profil_utilisateur.html', resultat=resultat)

@app.route('/Recherche-avancee', methods=['GET', 'POST'])
def recherche_avancee():
    form = advancedResearchForm()
    if form.is_submitted():
        book = request.form.getlist('researchB')
        author = request.form.getlist('researchA')
        origin = request.form.getlist('researchO')
        #-------------------------------------------------
        checkList = ['fantaisieCheck', 'sFCheck', 'polarCheck', 'classiqueCheck', 'horreurCheck', 'bDCheck', 'overratedCheck']
        boolList = []
        for i in checkList:
            if request.form.getlist(i) != []:
                boolList.append(True)
            else:
                boolList.append(False)
        result=advancedResearch(book[0], author[0], boolList)
        return render_template('Resultats-recherche.html', result=result)
    return render_template('Recherche-avancee.html', form=form)

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




@app.route('/resultats-recherche')
def resultats_recherche():
    
    return render_template('Resultats-recherche.html')


@app.route('/location/<bookId>', methods=['GET'])
def location(bookId):

    if bookId[0] == "b":
        result = getBook(bookId)
        return render_template('Location.html', result=result)
    else:
        result= getMagazine(bookId)
        return render_template('Achat.html', result=result)

@app.route('/auteur/<authorName>', methods=['GET'])
def author(authorName):
    result = getAuthor(authorName)
    booksResult = getBooksFromAuthor(authorName)
    return render_template('AuthorProfile.html', result=result, booksResult=booksResult)

@app.route('/admin', methods=['GET'])
def admin():
    print(adminPass)
    if not adminPass:
        return render_template('AdminPage.html')
    else:
        return "Erreur: vous ne pouvez pas accéder à cette page car vous n'êtes pas administrateur :("

if __name__=='__main__':
    app.run(debug=True)

