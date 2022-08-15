from config import VK_API_KEY
import vk_api
from PIL import Image
import os


def get_base_resize_coords(image: Image, columns: int = 2) -> tuple:
    image_width, image_height = image.size
    image_width = int(image_width)
    image_height = int((image_width / 3) * columns)
    return image_width, image_height


def get_parts_crop_coords(step: int) -> tuple:
    crop_coords = ((0, 0, step, step),
                   (step, 0, step * 2, step),
                   (step * 2, 0, step * 3, step),
                   (0, step, step, step * 2),
                   (step, step, step * 2, step * 2),
                   (step * 2, step, step * 3, step * 2),
                   (0, step, step, step * 2),
                   (step, step, step * 2, step * 2),
                   (step * 2, step, step * 3, step * 2)
                   )
    return crop_coords


def crop(image_id: int, columns: int = 2) -> None:
    image_id = str(image_id)

    # Open image and resize
    base_image_path = 'wrapper_images/images/image{}.jpg'.format(image_id)
    image = Image.open(base_image_path).convert('RGB')
    image = image.resize(get_base_resize_coords(image, columns))

    # create path from save crop images
    results_path = 'wrapper_images/results/image{}'.format(image_id).encode('utf-8')
    os.makedirs(results_path, exist_ok=True)

    # save full crop image
    processed_image_path = 'wrapper_images/results/image{}/full__processed.jpg'.format(image_id)
    image.save(processed_image_path)

    # save image parts

    # get coords
    base_processed_path = 'wrapper_images/results/image{}/'.format(image_id)
    crop_img = Image.open(processed_image_path)
    width, height = crop_img.size
    step = int(height / 2)

    # crop and save
    for num, coords in enumerate(get_parts_crop_coords(step), 1):
        img = crop_img.crop(coords)
        img.save(base_processed_path + '{}__processed.jpg'.format(num))


def load_picture(image_id: int, columns: int = 2) -> None:
    """ Загрузка разделённых изображений в ваш профиль ВКонтакте. """
    
    crop(image_id, columns)

    image_id = str(image_id)

    api_session = vk_api.VkApi(token=VK_API_KEY)

    upload_session = vk_api.upload.VkUpload(api_session)

    path = 'wrapper_images/results/image{}/'.format(image_id)
    photos = ['{}{}__processed.jpg'.format(path, item) for item in range(1, 7)][::-1]
    upload_session.photo(photos=photos,
                         album_id=284596525,
                         caption='⛈')
