import pandas as pd
import numpy as np



def get_user_session(sessions, user_id):
    if user_id not in sessions['user_id'].values:
        return -1
    return sessions.index[sessions['user_id'] == user_id][0]


def create_new_session(sessions, user_id):
    session_id =  get_user_session(sessions, user_id)
    if session_id != -1:
        sessions.loc[session_id, sessions.columns[2:]] = np.nan
        return session_id
    
    new_session = {
         'user_id': user_id, 'is_active': 0 ,
        **{col: np.nan for col in sessions.columns[2:]}
    }

    sessions.loc[sessions.shape[0]] = new_session

    return sessions.shape[0] - 1
    


def load_or_create_sessions():
    try:
        result = pd.read_csv("telegram-bot/sessions.csv")
    except FileNotFoundError:
        result = pd.DataFrame(columns=[
            'user_id', 'is_active', 'attr_1', 'attr_2'
        ])
        result.to_csv("telegram-bot/sessions.csv", index=False)
    
    return result

