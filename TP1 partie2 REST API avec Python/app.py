from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- Configuration MySQL ---

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Modèle ---
class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "nom": self.nom, "age": self.age}

# --- Création de la table ---
with app.app_context():
    db.create_all()

# --- Routes ---
@app.route('/')
def home():
    return "Bienvenue sur mon API Flask !"

# Récupérer tous les étudiants
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200

# Récupérer un étudiant par ID
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Étudiant introuvable"}), 404
    return jsonify(student.to_dict()), 200

# Ajouter un étudiant
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data or 'nom' not in data or 'age' not in data:
        return jsonify({"error": "Champs 'nom' et 'age' requis"}), 400

    new_student = Student(nom=data['nom'], age=data['age'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify(new_student.to_dict()), 201



# Mettre à jour partiellement un étudiant (PATCH)
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student_patch(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Étudiant introuvable"}), 404

    data = request.get_json()
    if 'nom' in data:
        student.nom = data['nom']
    if 'age' in data:
        student.age = data['age']
    db.session.commit()
    return jsonify(student.to_dict()), 200

# Supprimer un étudiant
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Étudiant introuvable"}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Étudiant supprimé avec succès"}), 200

# --- Lancer le serveur ---
if __name__ == '__main__':
    app.run(debug=True)
