import os
import requests
import warnings
import time
import json
import openai.api_requestor
from timeplus import Environment, Stream

api_key = os.environ.get("TIMEPLUS_API_KEY")
api_address = os.environ.get("TIMEPLUS_ADDRESS")
stream_name = "openai_api_calls"
env = Environment().address(api_address).apikey(api_key)


class MonitoringAdapter(requests.adapters.HTTPAdapter):
    def send(self, request, **kwargs):
        payload = {}
        payload["request_method"] = request.method
        payload["request_url"] = request.url
        payload["request_headers"] = {
            str(key): value
            for key, value in request.headers.items()
            if (key != "Authorization")
        }

        if "X-OpenAI-Client-User-Agent" in payload["request_headers"]:
            payload["request_headers"]["X-OpenAI-Client-User-Agent"] = json.loads(
                payload["request_headers"]["X-OpenAI-Client-User-Agent"]
            )

        payload["request_body"] = json.loads(request.body.decode("utf-8"))
        payload["request_timestamp"] = time.time()

        response = super().send(request, **kwargs)

        payload["response_status_code"] = str(response.status_code)
        payload["response_headers"] = {
            str(key): value for key, value in response.headers.items()
        }
        payload["response_text"] = json.loads(response.text)
        payload["response_timestamp"] = time.time()

        _ingest_api_call_raw(payload)
        return response


def _make_session():
    if not openai.verify_ssl_certs:
        warnings.warn("verify_ssl_certs is ignored; openai always verifies.")
    s = requests.Session()
    proxies = openai.api_requestor._requests_proxies_arg(openai.proxy)
    if proxies:
        s.proxies = proxies
    s.mount(
        "https://",
        MonitoringAdapter(),
    )
    return s


def _create_monitor_stream():
    if not Stream(env=env).name(stream_name).exist():
        # create a new stream
        try:
            Stream(env=env).name(stream_name).column("raw", "string").create()
        except Exception as e:
            print(f"failed to create stream {e}")


def _ingest_api_call_raw(call):
    payload = json.dumps(call)
    try:
        Stream(env=env).name(stream_name).ingest(payload=payload, format="raw")
    except Exception as e:
        print(f"failed to ingest event {call} to stream {stream_name} due to {e}")


def start():
    _create_monitor_stream()
    openai.api_requestor._make_session = _make_session
