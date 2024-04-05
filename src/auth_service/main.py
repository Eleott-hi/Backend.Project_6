import asyncio
from database.database import init_db

from grpc import aio
import proto.auth.auth_pb2_grpc as auth_pb2_grpc

from routers.AuthGRPCRouter import AuthenticationServicer


async def serve():
    server = aio.server()
    auth_pb2_grpc.add_AuthenticationServicer_to_server(
        AuthenticationServicer(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    await server.start()
    print(f"Server started. Listening on port {listen_addr}...", flush=True)
    await server.wait_for_termination()




async def main():
    await init_db()
    await serve()

if __name__ == "__main__":
    asyncio.run(main())

