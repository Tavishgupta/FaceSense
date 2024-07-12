import pickle
from pathlib import Path
import streamlit_authenticator as stauth
names = ["Tavish Gupta","Gatik Arya"]
usernames=["tavish17","gatik4"]
passwords=["Tavish@1234","Gatik@1234"]
hashed_passwords=stauth.Hasher(passwords).generate()
file_path=Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords,file)

 