import requests
import numpy as np
import time
import cv2
import glob

def encode_image(image: np.ndarray) -> str:
    # s = time.time()
    # success, image = cv2.imencode('.jpeg', image)
    b_img = image.tobytes()
    # print("enc t=", time.time() - s)
    return b_img

def upload_image_to_server(image: np.ndarray) -> np.ndarray:
    url = "http://localhost:8056/"
    encoded_image = encode_image(image)
    files = {"file": ("image.jpeg", encoded_image)}
    start = time.time()
    response = requests.post(url, files=files)
    print("t=", time.time() - start)
    print(response.content)

def upload_image_to_server_v2(image: np.ndarray) -> np.ndarray:
    h,w,c = image.shape
    config_param = {
    "crop_size": 112,
    "headpose": 0,
    "yaw_thresh": 30,
    "pitch_thresh": 30,
    "skip_frame_ratio": 0,
    "maxkeep": 20,
    "crop_region": [],
    "roi_list": [],
    "conf_thres": 0.5,
    "iou_thres": 0.6,
    "img_size": 640,
    "visualize": 0,
    "facedb_name": "frs_new_collection",
    "face_thresh": 0.5,
    "limit": 5
    }
    k = str(config_param)
    url = "http://localhost:8056/upload"
    encoded_image = encode_image(image)
    start = time.time()
    response = requests.post(url, data = encoded_image, params={"h": h, "w": w, "c": c, "k":k})
    print("t=", time.time() - start)
    print(response.content)


root = "../images"
filepaths = glob.glob(root+ str("/*"))
for filepath in filepaths:
    img = cv2.imread(filepath)
    print(filepath)
    # upload_image_to_server(img)
    upload_image_to_server_v2(img)
print('done')