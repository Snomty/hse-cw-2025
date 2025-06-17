import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
from io import BytesIO


def get_user_session(sessions, user_id):
    if user_id not in sessions['user_id'].values:
        return -1
    return sessions.index[sessions['user_id'] == user_id][0]


def create_series_table_image(series, title="Данные"):
    series = series[1:]
    df = pd.DataFrame({
        'Параметр': series.index,
        'Значение': series.values
    })
    df['Значение'] = df['Значение'].apply(lambda x: '' if pd.isna(x) else str(x))
    df.iloc[0] = ("Фотографии ремонта", "" if pd.isna(series['last_mesage_photo']) else "Добавлены")

    fig, ax = plt.subplots(figsize=(8, len(series)*0.5 + 1))
    ax.axis('off')
    plt.title(title, pad=20, fontsize=14)
    
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.8)
    
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=120, bbox_inches='tight')
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer
    

def create_new_session(sessions, user_id):
    session_id =  get_user_session(sessions, user_id)
    if session_id != -1:
        sessions.loc[session_id, sessions.columns[1:]] = np.nan
        return session_id
    
    new_session = { 'user_id': user_id }
    for col in sessions.columns[1:]:
        if pd.api.types.is_object_dtype(sessions[col]):
            new_session[col] = "" 
        else:
            new_session[col] = np.nan 

    sessions.loc[sessions.shape[0]] = new_session
    return sessions.shape[0] - 1
    

data_types = {
    'user_id':              'float64',
    'last_mesage_photo':    'float64',
    'city':                 'object',
    'street':               'object',
    'seller':               'object',
    'kitchen_space':        'float64', 
    'rooms':                'float64',
    'area':                 'float64',
    'floor':                'float64',
    'floorsTotal':          'float64',
    'nearest_metro':        'object',
    'time_to_metro':        'float64',
    'nearest_pond':         'object',
    'distance_pond':        'float64',
    'distance_airport':     'float64',
    'time_airport_via_car': 'float64'
}

def load_or_create_sessions():
    try:
        result = pd.read_csv("telegram-bot/sessions.csv").astype(data_types)
    except FileNotFoundError:
        result = pd.DataFrame(columns=data_types.keys()).astype(data_types)
        result.to_csv("telegram-bot/sessions.csv", index=False)

    return result

