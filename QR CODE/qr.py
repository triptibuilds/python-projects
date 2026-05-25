import qrcode
import qrcode.constants

qr = qrcode.QRCode(
    version = None,
    error_correction = 0,
    box_size = 10,
    border = 4,
    mask_pattern = None,
    image_factory = None
)

qr.add_data("https://www.youtube.com", optimize=True) # storing data in the memory, optimize --> chunks

qr.make(fit = True) # encoding the data, fit --> chooses best size for your qr, if false uses vision size

image = qr.make_image(fill_color = 'black', back_color = "white") # finally making the image, [image_factory],[embbedded_image_path]

image.save("QR_CODE.png")