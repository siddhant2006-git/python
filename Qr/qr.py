import qrcode as qr
img = qr.make(
    "https://www.youtube.com/watch?v=FOGRHBp6lvM&list=PLjVLYmrlmjGfAUdLiF2bQ-0l8SwNZ1sBl"
)
image = qr.make("https://github.com/siddhant2006-git/python")
img.save("krish.png")
image.save("python.jpg")
