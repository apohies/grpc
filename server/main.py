import sys
from pathlib import Path
# Agrega el directorio padre al sys.path para poder importar el módulo proto
sys.path.append(str(Path(__file__).parent.parent))

from concurrent import futures
import grpc
import logging

# Ahora puedes importar desde proto como si estuviera en el mismo directorio
import proto.my_service_pb2 as my_service_pb2
import proto.my_service_pb2_grpc as my_service_pb2_grpc

class MyService(my_service_pb2_grpc.MyServiceServicer):
    def MyFunction(self, request, context):
        return my_service_pb2.MyResponse(message='minardi, ' + request.message)
        
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_service_pb2_grpc.add_MyServiceServicer_to_server(MyService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info('El servidor ha iniciado en [::]:50051')  # Mensaje de inicio del servidor
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        logging.info('El servidor se ha detenido')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()