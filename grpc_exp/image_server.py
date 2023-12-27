import grpc
import image_procedure_pb2
import image_procedure_pb2_grpc
import numpy as np
from concurrent import futures
import time 

class ImageProcedureServicer(image_procedure_pb2_grpc.ImageProcedureServicer):
    def ImageMeanWH(self, request, context):
        # Convert the request message to a numpy array
        s = time.time()
        arr = np.frombuffer(request.image, dtype=np.uint8)
        print('to np t=', time.time() - s)
        # a = np.array(BytesIO(data))
        print(arr.shape)

        # Calculate the mean of the array
        mean = 1

        # Create a response message
        response = image_procedure_pb2.Prediction()
        response.channel = 3
        response.mean = mean

        return response

MAX_MESSAGE_LENGTH = 1024 * 1024 * 1024  # 1 GB

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options = [
        ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)
    ])
image_procedure_pb2_grpc.add_ImageProcedureServicer_to_server(ImageProcedureServicer(), server)
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()