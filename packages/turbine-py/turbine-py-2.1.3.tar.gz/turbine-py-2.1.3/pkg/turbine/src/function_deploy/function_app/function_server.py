import logging
import os
import sys

import grpc.aio
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc
from grpc_reflection.v1alpha import reflection
from .proto_gen import add_FunctionServicer_to_server
from .proto_gen import FunctionServicer
from .proto_gen import ProcessRecordRequest
from .proto_gen import ProcessRecordResponse
from .record import proto_records_to_turbine_records
from .record import turbine_records_to_proto_records

# from importlib.resources import path

"""
Process function given to GRPC server
"""

FUNCTION_ADDRESS = os.getenv("MEROXA_FUNCTION_ADDR")
PATH_TO_DATA_APP = os.getcwd()

# Coroutines to be invoked when the event loop is shutting down.
_cleanup_coroutines = []


class FunctionServer(FunctionServicer):
    def __init__(self, function_name) -> None:
        self.function_name = function_name
        super().__init__()

    @staticmethod
    def _obtain_client_data_app_function(path_to_data_app: str, function_name: str):
        sys.path.append(path_to_data_app)
        import main

        return main.__getattribute__(function_name)

    async def Process(
        self,
        request: ProcessRecordRequest,
        context: grpc.aio.ServicerContext,
    ) -> ProcessRecordResponse:
        # map from rpc => something we can work with
        input_records = proto_records_to_turbine_records(request.records)

        # Get the data app function
        data_app_function = self._obtain_client_data_app_function(
            path_to_data_app=PATH_TO_DATA_APP, function_name=self.function_name
        )

        # Generate output
        output_records = data_app_function(input_records)

        # Serialize and return
        grpc_records = turbine_records_to_proto_records(output_records)

        return ProcessRecordResponse(records=grpc_records)


async def serve(function_name) -> None:
    server = grpc.aio.server()
    add_FunctionServicer_to_server(FunctionServer(function_name), server)

    # Create a health check servicer. We use the non-blocking implementation
    # to avoid thread starvation.
    health_servicer = health.HealthServicer(experimental_non_blocking=True)

    # Create a tuple of all the services we want to export via reflection.
    services = tuple(
        service.full_name for service in health_pb2.DESCRIPTOR.services_by_name.values()
    ) + (reflection.SERVICE_NAME, "function")

    # Mark all services as healthy.
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    for service in services:
        health_servicer.set(service, health_pb2.HealthCheckResponse.SERVING)
    reflection.enable_server_reflection(services, server)
    server.add_insecure_port(FUNCTION_ADDRESS)

    logging.info(f"Starting server on {FUNCTION_ADDRESS}")

    await server.start()

    async def shutdown():
        logging.info("Shutting python gRPC server down..")
        await server.stop(grace=5)

    _cleanup_coroutines.append(shutdown())
    await server.wait_for_termination()
