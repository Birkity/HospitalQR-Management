import qrcode
from io import BytesIO
from flask import send_file

def generate_qr_code(data):
    img = qrcode.make(data)
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    return send_file(byte_io, mimetype='image/png')