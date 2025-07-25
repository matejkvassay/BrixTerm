import socket

from brixterm.constants import PHOENIX_HOST, PHOENIX_PORT


def configure_phoenix():
    def phoenix_available(host=PHOENIX_HOST, port=PHOENIX_PORT):
        try:
            socket.create_connection((host, port), timeout=0.5).close()
            return True
        except OSError:
            return False

    if phoenix_available():
        try:
            from openinference.instrumentation.openai import OpenAIInstrumentor
            from phoenix.otel import register

            OpenAIInstrumentor().instrument(tracer_provider=register())
            print("Phoenix tracing enabled.")
        except Exception as e:
            print(f"Tracing setup failed: {e}")
    else:
        print("Phoenix not running — tracing disabled.")
