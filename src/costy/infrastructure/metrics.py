from dataclasses import dataclass

from prometheus_client import Counter, start_http_server


@dataclass(slots=True, kw_only=True)
class Metrics:
    total_requests: Counter
    failed_requests: Counter


def create_metrics() -> Metrics:
    return Metrics(
        total_requests=Counter("total_requests", "Total requests collected"),
        failed_requests=Counter("failed_requests", "Failed requests collected"),
    )


def start_metrics_server():
    start_http_server(9090)
