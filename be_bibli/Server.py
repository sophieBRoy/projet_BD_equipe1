from flask import Flask, render_template, request,redirect,url_for
from Forms import researchForm, advancedResearchForm
from log import LogForm
from abonnement import AbonnementForm
from Main import research, advancedResearch, getBook, getAuthor, getBooksFromAuthor, GetInfoUtilisateur, \
    SetUtilisateur, GetUser, getMagazine, addMagToPurchases, addBookToLocations, getUserLocations, getUserPurchases

app = Flask(__name__)
app.config['SECRET_KEY'] = "password"


courriel=""
motdePass=""
adminPass= 0
resultat1=[]
lastItemId = ""
userId = ''


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
        resultat= GetUser(courriel[0], motdePass[0])
        if resultat:
            resultat1.append(resultat[0])
            return redirect(url_for('utilisateur'))
        else:

            message += "Erreur dans votre courriel ou dans votre mot de passe"
    if not courriel:
        return render_template('Se-connecter.html', form=form, message=message)
    else:
        return redirect(url_for('utilisateur'))


@app.route('/abonnement')
def abonnement():
    result=[]
    form = AbonnementForm()
    if form.is_submitted():
        nom = request.form.getlist('nomUtilisateurs')
        prenom = request.form.getlist('prenomUtilisateurs')
        age = request.form.getlist('utilisateursAge')
        adresse = request.form.getlist('utilisateursAddresse')
        Courriel = request.form.getlist('utilisateursCourriel')
        motPass =request.form.getlist('utilisateursMdp')
        #fonction qui traite les entrée
        #result = SetUtilisateur(nom[0], prenom[0], age[0], adresse[0], courriel[0], motPass[0],)
    return render_template('Abonnement.html', form=form, result=result)

@app.route("/Profil_utilisateur")
def utilisateur():
    global userId
    global adminPass
    userId = resultat1[0]
    resultat = GetInfoUtilisateur(resultat1[0])
    adminPass = resultat[5]
    print(adminPass)
    locations = getUserLocations(userId)
    purchases = getUserPurchases(userId)
    return render_template('Profil_utilisateur.html', resultat=resultat, locations=locations, purchases=purchases)

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
    global lastItemId
    lastItemId = bookId
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
    if adminPass:
        return render_template('AdminPage.html')
    else:
        return "Erreur: vous ne pouvez pas accéder à cette page car vous n'êtes pas administrateur"

@app.route('/temp')
def achatComplet():
    global courriel
    if courriel:
        addMagToPurchases(userId, lastItemId)
    return redirect(url_for('se_connecter'))

@app.route('/temp2')
def locationComplet():
    global courriel
    if courriel:
        addBookToLocations(userId, lastItemId)
    return redirect(url_for('se_connecter'))

if __name__=='__main__':
    app.run(debug=True)

