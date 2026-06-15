import qrcode
from PIL import Image  # Dhyan rahe: 'Image' ka 'I' capital hona chahiye

# 1. QR Code object banana
qr = qrcode.QRCode(
    version=1,  # 1 se 40 tak ho sakta hai (1 sabse chhota hota hai)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level (L, M, Q, H)
    box_size=10,  # QR code ke har box ka size (pixels mein)
    border=4,  # Border ki thickness (minimum 4 honi chahiye)
)

# 2. Data add karna (URL, text, kuch bhi)
qr.add_data(
    "https://www.youtube.com/watch?v=FOGRHBp6lvM&list=PLjVLYmrlmjGfAUdLiF2bQ-0l8SwNZ1sBl"
)
qr.make(fit=True)

# 3. Image generate karna (Rang aapke hisaab se change kar sakte hain)
img = qr.make_image(fill_color="black", back_color="red")

# 4. Image ko save karna
img.save("mera_qr.png")

print("QR Code safalta se 'mera_qr.png' ke naam se save ho gaya!")
