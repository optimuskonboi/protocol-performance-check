import grpc
import image_procedure_pb2
import image_procedure_pb2_grpc
import numpy as np
import cv2
import time

# Define the maximum message size
MAX_MESSAGE_LENGTH = 1024 * 1024 * 1024  # 1 GB

# Create a gRPC channel and a stub
channel = grpc.insecure_channel('localhost:50051', options=[('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)])
stub = image_procedure_pb2_grpc.ImageProcedureStub(channel)
# Create a request message
request = image_procedure_pb2.Image()

import glob
root = "../images"
filepaths = glob.glob(root+ str("/*"))
for filepath in filepaths:
    print(filepath)
    img = cv2.imread(filepath)
    request.image = img.tobytes()
    request.width = img.shape[1]
    request.height = img.shape[0]
    # Call the server procedure
    start = time.time()
    response = stub.ImageMeanWH(request)
    print('t=', time.time() - start)
    # Print the response
    print(f"Channel: {response.channel}, Mean: {response.mean}")
print('done')