from PIL import Image
import os

path = "src/streamlit_dashboard/assets/logo.png"
if os.path.exists(path):
    img = Image.open(path)
    img.thumbnail((200, 200))
    img.save(path)
    print("Resized successfully.")
else:
    print("Logo not found.")
