import os
import importlib
import json
from functools import wraps

from opentelemetry import trace
from opentelemetry.propagate import extract
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, DEPLOYMENT_ENVIRONMENT, SERVICE_VERSION
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor

PHASE = os.environ.get("AWS_ENV", "stg")
OTEL_EXPORTER_OTLP_ENDPOINT = {
    "dev": "http://lunar-otel-collector-nlb-54fa60fab131c635.elb.ap-northeast-2.amazonaws.com:4317",
    "stg": "http://lunar-otel-collector-nlb-a02d95c2e11f9c70.elb.ap-northeast-2.amazonaws.com:4317",
    "prd": "http://lunar-otel-collector-nlb-0cf13b13d50ff4b8.elb.ap-northeast-2.amazonaws.com:4317",
}
MSP_MODEL_VERSION = os.environ.get("MSP_MODEL_VERSION", "NONE")

model = None
carrier = None


def traced(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        global carrier
        try:
            with trace.get_tracer(f.__module__).start_as_current_span(
                f.__name__, context=extract(carrier=carrier), kind=trace.SpanKind.SERVER
            ):
                return f(*args, **kwargs)
        except Exception as e:
            raise Exception(str(e))

    return wrapper


def traced_request(f):
    @wraps(f)
    def wrapper(request_body, *args, **kwargs):
        body = json.loads(request_body)
        global carrier
        carrier = {"traceparent": body.pop("trace_parent", "00-80e1afed08e019fc1110464cfa66635c-7a085853722dc6d2-01")}
        try:
            with trace.get_tracer(f.__module__).start_as_current_span(
                f.__name__, context=extract(carrier=carrier), kind=trace.SpanKind.SERVER
            ):
                return f(json.dumps(body), *args, **kwargs)
        except Exception as e:
            raise Exception(str(e))

    return wrapper


def model_fn(model_dir):
    setup_tracing()
    try:
        global model
        module_name = "model"
        model = importlib.import_module(module_name)
        return model.model_fn(model_dir)
    except Exception as e:
        raise Exception(f"Failed to load model in model_fn: {str(e)}")


@traced_request
def input_fn(request_body, request_content_type):
    try:
        return model.input_fn(request_body, request_content_type)
    except Exception as e:
        raise Exception(f"Failed to preprocess input in input_fn: {str(e)}")


@traced
def predict_fn(input_object, model_binary):
    try:
        return model.predict_fn(input_object, model_binary)
    except Exception as e:
        raise Exception(f"Failed to get model prediction in predict_fn: {str(e)}")


@traced
def output_fn(prediction, content_type):
    try:
        output = json.loads(model.output_fn(prediction, content_type))
        if output.get("model_version") is None:
            output["model_version"] = MSP_MODEL_VERSION
        return json.dumps(output)
    except Exception as e:
        raise Exception(f"Failed to postprocess output in output_fn: {str(e)}")


def setup_tracing():
    resource = Resource.create(
        {
            SERVICE_NAME: "SageMaker",
            DEPLOYMENT_ENVIRONMENT: PHASE.lower(),
            SERVICE_VERSION: MSP_MODEL_VERSION,
        }
    )
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT.get(PHASE.lower()), insecure=True))
    )

    RequestsInstrumentor().instrument()
    AioHttpClientInstrumentor().instrument()
