from datetime import datetime
from multiprocessing import Pool

import cv2
import numpy as np
from PIL import Image
import os
from rembg import remove

source_folder_path = r'C:\Users\Administrator\Desktop\product_images'
result_folder_path = r'C:\Users\Administrator\Desktop\post_images2'


# source_folder_path = r'C:\Users\Administrator\Desktop\post_images2'
# result_folder_path = r'C:\Users\Administrator\Desktop\test'


def has_white_background(image_path: str, target: float = 0.4) -> bool:
    white_color = np.array([255, 255, 255])
    image = cv2.imread(image_path)
    percent = (image == white_color).sum() / image.size

    return percent >= target


def process_chunks(images_list: list[str]) -> None:
    for path in images_list:
        if not has_white_background(path):
            Image.open(path).save(os.path.join(result_folder_path, os.path.basename(path)))


def split_images_in_chunks(raw_list: list[str], size: int) -> list[list[str]]:
    return [raw_list[i:i + size] for i in range(0, len(raw_list), size)]


def remove_background_by_chunk(images_list: list[str]) -> None:
    for path in images_list:
        input_path = output_path = path
        input = cv2.imread(input_path)
        output = remove(input, bgcolor=(255, 255, 255, 255))
        cv2.imwrite(output_path, output)


if __name__ == '__main__':
    chunk_size = 100
    all_images = [os.path.join(source_folder_path, file) for file in os.listdir(source_folder_path)]
    image_chunks = split_images_in_chunks(all_images, chunk_size)

    if image_chunks:
        with Pool(20) as p:
            chunk_start = datetime.now()
            p.map(process_chunks, image_chunks)
            chunk_delta = datetime.now() - chunk_start
            print(chunk_delta)
        print('finished images selection')
    selected_chunk_size = 10
    selected_images = [os.path.join(result_folder_path, file) for file in os.listdir(result_folder_path)]
    selected_chunks = split_images_in_chunks(selected_images, selected_chunk_size)
    if selected_chunks:
        with Pool(20) as p:
            chunk_start = datetime.now()
            p.map(remove_background_by_chunk, selected_chunks)
            chunk_delta = datetime.now() - chunk_start
            print(chunk_delta)
        print('finished background removal')
