from flask import Flask, render_template, request
from Forms import researchForm, advancedResearchForm
from Main import research, advancedResearch, getBook, getMagazine, getUser, getAuthor, getBooksFromAuthor


app = Flask(__name__)
app.config['SECRET_KEY'] = "password"


user = getUser('james@gmail.com', 'james')
adminPass = user[0][7]

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

@app.route('/location/<bookId>', methods=['GET'])
def location(bookId):
    if bookId[0] == "b":
        result = getBook(bookId)
        return render_template('Location.html', result=result)
    else:
        result=getMagazine(bookId)
        return render_template('Achat.html', result=result)

@app.route('/auteur/<authorName>', methods=['GET'])
def author(authorName):
    result = getAuthor(authorName)
    booksResult = getBooksFromAuthor(authorName)
    return render_template('AuthorProfile.html', result=result, booksResult=booksResult)

@app.route('/admin', methods=['GET'])
def admin():
    print(adminPass)
    if adminPass == 0:
        return render_template('AdminPage.html')
    else:
        return "Erreur: vous ne pouvez pas accéder à cette page car vous n'êtes pas administrateur :("

if __name__=='__main__':
    app.run()

