from sessions_utility import get_user_session
import sklearn
from PIL import Image
import xgboost as xgb
import pandas as pd
import pickle
import torch
import os
import io

xgb.set_config(verbosity=0)

def load_models():

    with open('models/stacking_model.pkl', 'rb') as f:
        model = pickle.load(f) 

    return model


def load_photos(bot, message, sessions):
    unique_photos = {}
    
    for photo in message.photo:
        if photo.file_unique_id not in unique_photos:
            unique_photos[photo.file_unique_id] = photo
    
    saved_photos = []
    
    for file_unique_id, photo in unique_photos.items():
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        img = Image.open(io.BytesIO(downloaded_file))


def predict_pipline(message, model, sessions):
    user_id = message.from_user.id
    session_id = get_user_session(sessions, user_id)
    session = sessions.iloc[session_id]

    message_phot_id = session['last_mesage_photo']
    if pd.isna(message_phot_id):
        print("Нет фото")
    else:
        print("Есть фото")

    test_input = pd.read_csv("test_input.csv")
    print(model.predict(test_input))

    input_data = session[2:]
