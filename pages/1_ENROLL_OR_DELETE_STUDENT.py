import streamlit as st
import cv2
import os
import time
import csv
import pickle
from pathlib import Path
# import streamlit_authenticator as stauth

# names = ["Tavish Gupta","Gatik Arya"]
# usernames=["tavish17","gatik4"]
# file_path = Path(__file__).parent / "hashed_pw.pkl"
# with file_path.open("rb") as file:
#     hashed_passwords = pickle.load(file)

# authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "student_dashboard", "abcdef", cookie_expiry_days=0) 
# name, authentication_status, username = authenticator.login(" Student Login", "main")

# if authentication_status == False:
#     st.error("Username/Password is incorrect")
# if authentication_status == None:
#      st.warning("Please enter your username and password")
# if authentication_status:
st.sidebar.title(f"Welcome")
root_dir = Path(__file__).parent.parent / "captured_images"
csv_file = None

if not root_dir.exists():
    root_dir.mkdir(parents=True, exist_ok=True)

# def main():
#     st.title("ENROLL STUDENT")
#     global name, regno, branch, sec,cap

#     # Define session state for camera feed if not already defined
#     if 'run_camera' not in st.session_state:
#         st.session_state.run_camera = False
#     if 'cap' not in st.session_state:
#         st.session_state.cap = None
#     if 'frame' not in st.session_state:
#         st.session_state.frame = None

#     name = st.text_input("Enter Name")
#     regno = st.text_input("Enter Registration Number")
#     branch = st.text_input("Enter Branch").upper()
#     sec = st.text_input("Enter Section").upper()

#     st.text("Capture Image")
#     authenticator.logout("Logout", "sidebar")

#     # Checkbox to run the camera feed
#     run = st.checkbox('Run', value=st.session_state.run_camera)
#     st.session_state.run_camera = run

#     FRAME_WINDOW = st.empty()

#     if st.session_state.run_camera:
#         if st.session_state.cap is None:
#             st.session_state.cap = cv2.VideoCapture(0)

#         ret, frame = st.session_state.cap.read()
#         if ret:
#             st.session_state.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             FRAME_WINDOW.image(st.session_state.frame)
#     else:
#         if st.session_state.cap:
#             st.session_state.cap.release()
#             st.session_state.cap = None

#     if st.button("Capture"):
#         create_directories()
#         # If you have a frame from the live feed, use that for capture
#         if st.session_state.frame is not None:
#             st.image(st.session_state.frame, caption="Captured Image", use_column_width=True)
#             image_path = save_image(st.session_state.frame)
#             save_to_csv(image_path)
#         else:
#             # If not, then capture a new frame as before
#             if st.session_state.cap is None:
#                 st.session_state.cap = cv2.VideoCapture(0)
#             ret, frame = st.session_state.cap.read()
#             if ret:
#                 frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 st.image(frame_rgb, caption="Captured Image", use_column_width=True)
#                 image_path = save_image(frame_rgb)
#                 save_to_csv(image_path)

#     if st.button('Delete'):
#         delete_entry(regno)

def main():
    st.title("ENROLL STUDENT")
    global name, regno, branch, sec, cap
    name = st.text_input("Enter Name")
    regno = st.text_input("Enter Registration Number")
    branch = st.text_input("Enter Branch")
    sec = st.text_input("Enter Section")
    branch = branch.upper()
    sec = sec.upper()
    st.text("Capture Image")
    # authenticator.logout("Logout","sidebar")
    run = st.checkbox('Run')
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    while run:
        _, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)

    if st.button("Capture"):
        create_directories()
        cap = cv2.VideoCapture(0)
        time.sleep(1)
        capture_image()
    
    if st.button('Delete'):
        delete_entry(regno)

def create_directories():
    global csv_file
    branch_sec = branch + sec
    branch_sec_dir = root_dir / branch_sec
    branch_sec_dir.mkdir(parents=True, exist_ok=True)
    csv_file = branch_sec_dir / f"{branch_sec}.csv"
    
    if not csv_file.is_file():
        with csv_file.open('w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Image Path", "Registration Number", "Name", "Class"])

def check_duplicate_registration_number(regno):
    with csv_file.open('r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if row[1] == regno:
                return True
    return False

def capture_image():
    if not cap.isOpened():
        st.error("Unable to access the camera. Please make sure it is connected and not in use by another application.")
        return

    if check_duplicate_registration_number(regno):
        st.warning(f"Registration number {regno} already exists")
        cap.release()
        return

    ret, frame = cap.read()

    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame_rgb, caption="Captured Image", use_column_width=True)
        image_path = save_image(frame)
        save_to_csv(image_path)
    else:
        st.warning("No image captured")

    cap.release()

def save_image(image):
    image_path = root_dir / (branch + sec) / f"{regno}.jpg"
    cv2.imwrite(str(image_path), image)
    st.success(f"Image saved at {image_path}")
    return str(image_path)

def save_to_csv(image_path):
    with csv_file.open('a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([image_path, regno, name, branch + sec])

def delete_entry(regno):
    branch_sec = branch + sec
    branch_sec_dir = root_dir / branch_sec
    csv_file_path = branch_sec_dir / f"{branch_sec}.csv"

    if not csv_file_path.is_file():
        st.error("Record not found. Cannot proceed with deletion.")
        return

    temp_file = branch_sec_dir / "temp.csv"
    image_path_to_delete = None

    with csv_file_path.open('r') as infile, temp_file.open('w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        headers = next(reader)  # Copy headers
        writer.writerow(headers)
        
        for row in reader:
            if row[1] != regno:  # Compare with the registration number
                writer.writerow(row)
            else:
                image_path_to_delete = row[0]

    if image_path_to_delete:
        csv_file_path.unlink()
        temp_file.rename(csv_file_path)

        try:
            Path(image_path_to_delete).unlink()
            st.success(f"Deleted image at {image_path_to_delete}")
        except Exception as e:
            st.error(f"Error deleting image: {e}")
    else:
        st.warning(f"No entry found for registration number {regno}")

if __name__ == "__main__":
    main()
