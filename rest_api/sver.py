from fastapi import FastAPI, UploadFile, File, Request, Query, Body
from PIL import Image
from io import BytesIO
import numpy as np
import uvicorn
import time

app = FastAPI()

def load_image_into_numpy_array(data,h,w,c):
    a = np.frombuffer(data, dtype=np.uint8)
    a = a.reshape((h,w,c))
    return a
    a = np.array(Image.open(BytesIO(data)).convert('RGB'))
    print(a.shape)
    return a

@app.post("/")
async def read_root(file: UploadFile = File(...)):
    print(file.filename)
    s = time.time()
    image = load_image_into_numpy_array(await file.read())
    return {"Hello": str(image.shape) + str(time.time() - s)}

import json
@app.post("/upload")
async def upload(request: Request):
    params = request.query_params
    config_param = params["k"]
    config_param = config_param.replace("'", "\"")
    config = json.loads(config_param)
    print(config)
    h = int(params["h"])
    w = int(params["w"])
    c = int(params["c"])
    data = await request.body()
    s = time.time()
    image = load_image_into_numpy_array(data, h,w,c)
    return {"Hello": str(image.shape) + str(time.time() - s)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8056)