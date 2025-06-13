from PIL import Image, ImageTk
from PIL.JpegImagePlugin import JpegImageFile
from io import BytesIO
from typing import List
import concurrent.futures
import requests

def get_image(url: str) -> JpegImageFile:
    """
    Базовая функция, принимает ссылку вида как в датасете
    (  //avatars.mds.yandex.net/get-realty-offers/14635834/79a03818/large_1242  )
    Возвращает картинку в виде    PIL.JpegImagePlugin.JpegImageFile
    """
    if ("https:" not in url):
        url = "https:" + url

    try:
        response = requests.get(url)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        return image
    except requests.exceptions.RequestException as err:
        print(f"Ошибка при загрузке изображения: {err}")
        return None


# Чтобы быстрее парсилось, можно сделать многопотоку
def get_images_optimizer(urls: List[str], num_thread: int = 5) -> List[JpegImageFile]:
    """
    Так как на каждую картинку отапрвляется запрос, ждать который долго, сделал многопоточку,
    Принимает массив ссылок как в датасете.   Возвращает список PIL.JpegImagePlugin.JpegImageFile
    """
    images = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_thread) as executor:
        future_to_url = {executor.submit(get_image, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                image = future.result()
                if image:
                    images.append(image)
            except Exception as e:
                print(f"Ошибка при обработке {url}: {e}")
    return images