from sessions_utility import get_user_session
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from PIL import Image
import lightgbm as lgb
import xgboost as xgb
import pandas as pd
import numpy as np
import warnings
import sklearn
import pickle
import joblib
import torch
import os
import io

xgb.set_config(verbosity=0)

def load_models():

    with open('models/stacking_model.pkl', 'rb') as f:
        model = pickle.load(f)

    preprocessor = joblib.load('models/preprocessor.joblib')

    return model, preprocessor


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


def predict_pipline(message, model, preprocessor, sessions):
    user_id = message.from_user.id
    session_id = get_user_session(sessions, user_id)
    session = sessions.iloc[session_id]

    message_phot_id = session['last_mesage_photo']

    data = pd.DataFrame([session[2:]])

    data['street'] = data['street'].fillna('unknown')
    data['floor_ratio'] = data['floor'] / data['floorsTotal']
    data['is_ground_floor'] = (data['floor'] == 1).astype(int)
    data['is_top_floor'] = (data['floor'] == data['floorsTotal']).astype(int)
    data['kitchen_area_ratio'] = data['kitchen_space'] / data['area']


    data = preprocessor.transform(data)
    data = data.toarray() if hasattr(data, 'toarray') else data

    num_feature_names = num_features
    cat_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(cat_features)
    feature_names = np.concatenate([num_feature_names, cat_feature_names])

    data = pd.DataFrame(data, columns=feature_names)

    missing_columns = set(top_features) - set(data.columns)
    data = data.reindex(columns=top_features, fill_value=0)
        
    return model.predict(data)[0]




num_features = [
    'area',
    'rooms',
    'floor',
    'floorsTotal',
    'time_to_metro',
    'distance_pond',
    'distance_airport',
    'time_airport_via_car',
    'kitchen_space',
    'floor_ratio',
    'is_ground_floor',
    'is_top_floor',
    'kitchen_area_ratio'
 ]

cat_features = ['city', 'street', 'nearest_metro', 'nearest_pond', 'seller']

top_features = ['street_Ремесленная улица', 'nearest_metro_Крестовский остров',
    'street_Захарьевская улица', 'street_Воскресенская набережная',
    'nearest_metro_Чернышевская', 'nearest_pond_река Малая Невка',
    'nearest_metro_Чёрная Речка', 'nearest_metro_Чкаловская', 'area',
    'seller_DEVELOPER', 'nearest_pond_Петровский пруд', 'distance_pond',
    'city_Санкт-Петербург', 'street_улица Моисеенко',
    'nearest_metro_Петроградская', 'nearest_pond_пруды Таврического сада',
    'street_Вязовая улица', 'street_набережная Кутузова',
    'time_airport_via_car', 'street_Миргородская улица',
    'nearest_pond_река Карповка', 'distance_airport',
    'street_Алтайская улица', 'nearest_pond_река Мойка',
    'street_набережная Обводного канала', 'city_сестрорецк',
    'street_Итальянская улица', 'street_набережная реки Карповки', 'rooms',
    'street_набережная Гребного канала', 'floorsTotal',
    'nearest_metro_Приморская', 'kitchen_space', 'floor_ratio',
    'street_23-я линия Васильевского острова', 'street_2-я Берёзовая аллея',
    'city_муниципальный округ № 54',
    'nearest_metro_Площадь Александра Невского',
    'street_20-я линия Васильевского острова', 'nearest_metro_Девяткино',
    'street_Гагаринская улица', 'street_территория Петроградская сторона',
    'city_посёлок репино', 'floor', 'street_Орловская улица',
    'nearest_pond_Нижнее Большое Суздальское озеро',
    'street_Мытнинская набережная', 'street_улица Коли Томчака',
    'street_Василеостровский район', 'street_Кемская улица'
]
