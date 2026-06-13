import base64
try:
    with open("src/streamlit_dashboard/assets/logo.png", "rb") as img_file:
        print("Success! Length:", len(base64.b64encode(img_file.read()).decode()))
except Exception as e:
    print("Error:", e)
