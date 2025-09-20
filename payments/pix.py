import uuid
import qrcode

class Pix:
    def __init__(self):
        pass

    def create_payment(self):
        bank_payment = str(uuid.uuid4())
        hash_payment = f"hash_payment{bank_payment}"
        img = qrcode.make(hash_payment)

        img.save(f"static/img/qr_code_payment_{bank_payment}.png")

        return {"bank_payment": bank_payment,
                "qr_code_path": f"qr_code_payment_{bank_payment}"}