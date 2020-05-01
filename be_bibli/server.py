from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def accueil():
    return render_template('Accueil.html')

@app.route('/nous-joindre')
def nous_joindre():
    return render_template('nous-joindre.html')



@app.route('/profile/<int:user_id>')
def profile(user_id):
    return 'this is user' + str(user_id)

if __name__=='__main__':
    app.run()

