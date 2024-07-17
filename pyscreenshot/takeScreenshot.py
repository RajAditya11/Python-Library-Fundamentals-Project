import pyscreenshot
from PIL import Image

image = pyscreenshot.grab()

image.show()

image.save("screen.png")