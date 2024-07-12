import streamlit as st
import os
import pickle
from pathlib import Path
# import streamlit_authenticator as stauth
from deepface import DeepFace
import pandas as pd

# Set up paths
current_dir = Path(__file__).parent
hashed_pw_path = current_dir / "hashed_pw.pkl"
cropped_images_path = Path(__file__).parent.parent / "cropped_images"
captured_images_path = Path(__file__).parent.parent / "captured_images"

# Ensure directories exist
cropped_images_path.mkdir(parents=True, exist_ok=True)
captured_images_path.mkdir(parents=True, exist_ok=True)

# names = ["Tavish Gupta", "Gatik Arya"]
# usernames = ["tavish17", "gatik4"]

# with hashed_pw_path.open("rb") as file:
#     hashed_passwords = pickle.load(file)

# authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "student_dashboard", "abcdef", cookie_expiry_days=0)
# name, authentication_status, username = authenticator.login("Teacher Login", "main")

# if authentication_status == False:
#     st.error("Username/Password is incorrect")
# if authentication_status == None:
#     st.warning("Please enter your username and password")
# if authentication_status:
st.sidebar.title(f"Welcome")
st.title("TAKE ATTENDANCE")

branch = st.text_input("Enter Branch")
sec = st.text_input("Enter Section")
branch = branch.upper()
sec = sec.upper()

uploaded_file = st.file_uploader("Upload The Image Of The Class", type=["jpg", "jpeg", "png", "HEIC"])
if uploaded_file:
    file_name = uploaded_file.name
    file_path = cropped_images_path / file_name
    with file_path.open("wb") as file:
        file.write(uploaded_file.read())
    st.success(f"File '{file_name}' uploaded and saved to '{file_path}'")

branch_sec = branch + sec

if st.button("Take Attendance"):
    models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "Dlib", "ArcFace"]
    detectors = ["opencv", "ssd", "mtcnn", "dlib", "retinaface"]
    folder_path = captured_images_path / branch_sec
    all_files = os.listdir(folder_path)
    image_files = [file for file in all_files if file.lower().endswith((".jpg", ".png", ".jpeg", ".gif", "webp"))]
    list1 = []
    for x in image_files:
        image_path = os.path.join(folder_path, x)
        recognition = DeepFace.find(image_path, str(cropped_images_path), models[1])
        s = str(recognition)
        if "Empty DataFrame" not in s:
            list1.append(image_path)

    csv = branch_sec + ".csv"
    csv_file_path = captured_images_path / branch_sec / csv
    df = pd.read_csv(str(csv_file_path))
    
    df["Image Path"] = df["Image Path"].str.lower()
    list1 = [path.lower() for path in list1]
    
    filtered_data = df[df["Image Path"].isin(list1)][["Registration Number", "Name"]]
    
    
    # Display the filtered data
    st.text(f"Students Present in {branch_sec}")
    st.write(filtered_data)
    
    # Save the filtered data to a new CSV file if needed
    output_csv_file = captured_images_path / "output.csv"
    filtered_data.to_csv(output_csv_file, index=False)
