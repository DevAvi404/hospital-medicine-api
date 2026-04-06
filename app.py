from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --------------------
# Database config
# --------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medicine.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --------------------
# Medicine Model
# --------------------
class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(200))

# --------------------
# Seed 100 Medicines
# --------------------
def seed_medicines():
    if Medicine.query.first():
        return  # Already seeded

    medicines_list = [
        {"name": "Paracetamol", "price": 5, "quantity": 100, "description": "Pain & fever relief"},
        {"name": "Ibuprofen", "price": 8, "quantity": 80, "description": "Anti-inflammatory"},
        {"name": "Amoxicillin", "price": 12, "quantity": 50, "description": "Antibiotic"},
        {"name": "Ciprofloxacin", "price": 15, "quantity": 60, "description": "Antibiotic"},
        {"name": "Naproxen", "price": 10, "quantity": 70, "description": "Pain & inflammation"},
        {"name": "Aspirin", "price": 7, "quantity": 90, "description": "Pain & blood thinner"},
        {"name": "Cetirizine", "price": 6, "quantity": 100, "description": "Antihistamine"},
        {"name": "Loratadine", "price": 6, "quantity": 100, "description": "Allergy relief"},
        {"name": "Omeprazole", "price": 10, "quantity": 80, "description": "Stomach acid reducer"},
        {"name": "Pantoprazole", "price": 12, "quantity": 70, "description": "Stomach acid reducer"},
    ]

    # Fill until 100
    for i in range(len(medicines_list)+1, 101):
        medicines_list.append({
            "name": f"Medicine {i}",
            "price": 5 + i,
            "quantity": 50 + i,
            "description": f"Description for Medicine {i}"
        })

    for med in medicines_list:
        db.session.add(Medicine(
            name=med['name'],
            price=med['price'],
            quantity=med['quantity'],
            description=med['description']
        ))
    db.session.commit()
    print("✅ 100 medicines added to database!")

# --------------------
# API Routes
# --------------------
@app.route('/api/medicine', methods=['POST'])
def add_medicine():
    data = request.json
    med = Medicine(
        name=data['name'],
        price=data['price'],
        quantity=data['quantity'],
        description=data['description']
    )
    db.session.add(med)
    db.session.commit()
    return jsonify({"message": "Medicine added!"})

@app.route('/api/medicine', methods=['GET'])
def get_medicines():
    meds = Medicine.query.all()
    result = []
    for m in meds:
        result.append({
            "id": m.id,
            "name": m.name,
            "price": m.price,
            "quantity": m.quantity,
            "description": m.description
        })
    return jsonify(result)

@app.route('/api/medicine/<int:id>', methods=['GET'])
def get_medicine(id):
    m = Medicine.query.get(id)
    if not m:
        return jsonify({"error": "Medicine not found"}), 404
    return jsonify({
        "id": m.id,
        "name": m.name,
        "price": m.price,
        "quantity": m.quantity,
        "description": m.description
    })

@app.route('/api/medicine/<int:id>', methods=['PUT'])
def update_medicine(id):
    m = Medicine.query.get(id)
    if not m:
        return jsonify({"error": "Medicine not found"}), 404
    data = request.json
    m.name = data['name']
    m.price = data['price']
    m.quantity = data['quantity']
    m.description = data['description']
    db.session.commit()
    return jsonify({"message": "Updated successfully"})

@app.route('/api/medicine/<int:id>', methods=['DELETE'])
def delete_medicine(id):
    m = Medicine.query.get(id)
    if not m:
        return jsonify({"error": "Medicine not found"}), 404
    db.session.delete(m)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"})

# --------------------
# Run Server
# --------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()      # Create tables
        seed_medicines()     # Seed 100 medicines
    app.run(debug=True)