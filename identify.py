from deepface import DeepFace
import os
import pandas as pd
from pathlib import Path
import csv
import streamlit as st

def recognize(branch_sec,file_path):
    models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "Dlib", "ArcFace"]
    detectors = ["opencv", "ssd", "mtcnn", "dlib","retinaface"]
    #verification=DeepFace.verify("gatik.jpg","IMG_3855.jpg",models[1])
    #print(verification)
    project_dir = Path(__file__).parent
    folder_path="/Users/tavishgupta/Desktop/AP_Project/captured_images/"+branch_sec+""
    all_files=os.listdir(folder_path)
    image_files = [file for file in all_files if file.lower().endswith((".jpg", ".png", ".jpeg", ".gif","webp"))]
    list1=[]
    for x in image_files:
        image_path=os.path.join(folder_path,x)
        recognition = DeepFace.find(image_path,file_path,models[1])
        s=str(recognition)
        if "Empty DataFrame" not in s:
            list1.append(image_path)
    csv_file_path = "/Users/tavishgupta/Desktop/AP_Project/captured_images/"+branch_sec+"/"+branch_sec+".csv"
    df=pd.read_csv(csv_file_path)
    filtered_data=df[df["Image Path"].isin(list1)][["Registration Number", "Name"]]
    output_csv_file = "/Users/tavishgupta/Desktop/AP_Project/output.csv"
    filtered_data.to_csv(output_csv_file, index=False)
    data=pd.read_csv(output_csv_file)
    st.text("Students Present in "+branch_sec+"")
    st.write(data)
    with open(output_csv_file, mode='w', newline='') as file:
        file.write('')
    directory_path = '/Users/tavishgupta/Desktop/AP_Project/cropped_images'
    file_list = os.listdir(directory_path)
    for filename in file_list:
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)