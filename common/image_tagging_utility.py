from typing import List
import concurrent.futures
import tkinter as tk
import numpy as np
import pandas as pd

from image_loading_utility import *

hint = """
    0  —  Ремнота не видно  —  не учимся на таких фотках
    
    1  —  Без ремонта  —  голые стены просто
    
    2  —  Бабушкин ремонт  —  раздолбанная, мебель очень старая и тд 
    
    3  —  Отделка  —  просто есть обои, полы, потолки
    
    4  —  Качественная  —  дефолт ремонт
    
    5  —  Премиум  —  мажорский ремонт
"""

def tagging_process(urls: List[str]) -> List[int]:
    """
    Графический интерфейс на Tkinter который облегчает жизнь в 123123123 раз
    """
    if (urls == None):
        return None
    images = get_images_optimizer(urls)

    root = tk.Tk()
    root.title("tagging helper")

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    img_frame = tk.Frame(main_frame)
    img_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    img_label = tk.Label(img_frame)
    img_label.pack()



    btn_frame = tk.Frame(root)

    control_frame = tk.Frame(main_frame, width=250, bg="#f0f0f0")
    control_frame.pack(side=tk.RIGHT, fill=tk.Y)

    tk.Label(control_frame, text=hint, bg='#f0f0f0',justify=tk.LEFT, font=('Arial', 12, 'bold')).pack(pady=20)
    status = tk.Label(control_frame, text=f"Image 1/{len(urls)}", bg='#f0f0f0')
    status.pack()
    entry = tk.Entry(control_frame)
    entry.pack(pady=10)

    btn_frame = tk.Frame(control_frame, bg="#f0f0f0")
    btn_frame.pack(pady=20)
    next_btn = tk.Button(btn_frame, text="Следующая (Enter)", command=lambda: on_enter(), bg="#e0e0e0")
    next_btn.pack(side=tk.LEFT, padx=5)
    exit_btn = tk.Button(btn_frame, text="Выход (Esc)", command=root.quit, bg="#ffcccc")
    exit_btn.pack(side=tk.LEFT, padx=5)

    idx = 0
    labels = []

    def show_image():
        try:
            img = images[idx]
            img = img.resize((600, 600))
            photo = ImageTk.PhotoImage(img)

            img_label.config(image=photo)
            img_label.image = photo
            status.config(text=f"Image {idx + 1}/{len(urls)}")
        except Exception as err:
            print(f"Ошибка: {err}")
            root.destroy()
            root.quit()

    def on_enter():
        nonlocal idx

        label = entry.get()
        if label.isdigit() and 0 <= int(label) <= 4:
            labels.append(int(label))
            idx += 1
            entry.delete(0, tk.END)

            if idx < len(urls):
                show_image()
            else:
                root.destroy()
                root.quit()

    # Размещаем элементы
    entry.bind('<Return>', on_enter)
    show_image()
    root.mainloop()

    return labels


def main():
    df = pd.read_csv("data/clear_data.csv")
    print("Succesful read data")

    ### Дальше для каждого участника команды своя строчка (раскомментируйте)
    start_row, end_row, file_name = 0, 1000, "df_train_for_cv_minacov.csv"
    # start_row, end_row, file_name = 1000, 2000, "df_train_for_cv_baryshev.csv"
    # start_row, end_row, file_name = 2000, 3000, "df_train_for_cv_almetov.csv"

    df_train_for_CV = pd.read_csv("data/" + file_name)
    allready_tagged = df_train_for_CV["url"].values

    for idx in range(start_row, end_row):
        urls = df.iloc[idx]['images']
        if pd.isna(urls):
            continue

        urls = urls.replace("\'", "").replace(",", "").replace("[", "").replace("]", "").split()
        urls = [url for url in urls if url not in allready_tagged]
        if len(urls) == 0:
            continue

        labels = tagging_process(urls)
        if labels == []:
            break

        tmp_df = pd.DataFrame({"url": urls[:len(labels)], "label": labels})
        df_train_for_CV = pd.concat([df_train_for_CV, tmp_df], ignore_index=False)

    df_train_for_CV.to_csv("data/" + file_name, index=False)


if __name__ == "__main__":
    main()
