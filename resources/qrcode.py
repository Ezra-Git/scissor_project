import qrcode

def generate_qr_code(input_url):
    """Function to generate qr_code"""
    img = qrcode.make(input_url)
    return img

qr_code = generate_qr_code("https://www.google.com/")
print (type(qr_code), dir(qr_code))