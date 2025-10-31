from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# ✅ Configuration de la base de données
# Render te donnera automatiquement une variable d'environnement "DATABASE_URL"
# Si elle n'existe pas (en local), on utilise SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///visiteurs.db').replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ Définition du modèle
class Visiteur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

# ✅ Création de la base
with app.app_context():
    db.create_all()

# ✅ Route d’accueil (formulaire)
@app.route('/')
def index():
    return render_template('index.html')

# ✅ Ajouter un visiteur
@app.route('/ajouter', methods=['POST'])
def ajouter():
    nom = request.form['nom']
    email = request.form['email']
    nouveau = Visiteur(nom=nom, email=email)
    db.session.add(nouveau)
    db.session.commit()
    return redirect(url_for('liste_visiteurs'))

# ✅ Afficher la liste des visiteurs
@app.route('/visiteurs')
def liste_visiteurs():
    visiteurs = Visiteur.query.all()
    return render_template('visiteurs.html', visiteurs=visiteurs)

# ✅ Modifier un visiteur
@app.route('/modifier/<int:id>', methods=['GET', 'POST'])
def modifier(id):
    visiteur = Visiteur.query.get_or_404(id)
    if request.method == 'POST':
        visiteur.nom = request.form['nom']
        visiteur.email = request.form['email']
        db.session.commit()
        return redirect(url_for('liste_visiteurs'))
    return render_template('modifier.html', visiteur=visiteur)

# ✅ Supprimer un visiteur
@app.route('/supprimer/<int:id>')
def supprimer(id):
    visiteur = Visiteur.query.get_or_404(id)
    db.session.delete(visiteur)
    db.session.commit()
    return redirect(url_for('liste_visiteurs'))

# ✅ Lancer le serveur
if __name__ == '__main__':
    app.run(debug=True , host = '0.0.0.0', port=5000)