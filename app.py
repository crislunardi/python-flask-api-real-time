from flask import Flask, jsonify, request
from repository.database import db
from db_models.payment import Payment
from datetime import datetime, timedelta
from payments.pix import Pix

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "SECRET_KEY_WEBSOCKET"

db.init_app(app)

@app.route("/payments/pix", methods=["POST"])
def create_payment_pix():
    data = request.get_json()

    if "value" not in data:
        return jsonify({"message": "Invalid value"}), 400
    
    expiration_date = datetime.now() + timedelta(minutes=30)
    new_payment = Payment(value=data["value"], 
                          expiration_date=expiration_date)
    
    pix_obj = Pix()

    data_payment_pix = pix_obj.create_payment()
    new_payment.bank_payment = data_payment_pix["bank_payment"]
    new_payment_qr_code = data_payment_pix["qr_code_path"]

    db.session.add(new_payment)
    db.session.commit()

    return jsonify({"message": "The payment has been created",
                    "payment": new_payment.to_dict()})

@app.route("/payments/pix/confirmation", methods=["POST"])
def confirmation_pix():
    return jsonify({"message": "The payment has been confirmed"})

@app.route("/payments/pix/<int:payment_pix>", methods=["GET"])
def payment_pix_page(payment_pix):
    return "Payment PIX"

if __name__ == "__main__":
    app.run(debug=True)