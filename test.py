import pytesseract
from PIL import Image

# Test a blank image
text = pytesseract.image_to_string(Image.new('RGB', (100, 30), color = (255, 255, 255)))
print(text)
