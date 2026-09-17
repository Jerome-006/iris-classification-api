import concurrent.futures
import time
import requests

URL = "http://localhost:8000/api/v1/predict"

HEADERS = {
    "X-API-Key": "my-dev-api-key-2026",
    "Content-Type": "application/json",
}

PAYLOAD = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2,
}

TOTAL_REQUESTS = 50


def send_request():
    start = time.perf_counter()

    try:
        response = requests.post(
            URL,
            json=PAYLOAD,
            headers=HEADERS,
            timeout=10,
        )

        duration = time.perf_counter() - start

        return response.status_code, duration

    except requests.RequestException:
        return "ERROR", None


def main():
    start_time = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=50
    ) as executor:
        results = list(
            executor.map(
                lambda _: send_request(),
                range(TOTAL_REQUESTS),
            )
        )

    total_duration = time.perf_counter() - start_time

    successful = [
        duration
        for status, duration in results
        if status == 200
    ]

    failed = [
        status
        for status, _ in results
        if status != 200
    ]

    print(f"Total requests: {TOTAL_REQUESTS}")
    print(f"Successful requests: {len(successful)}")
    print(f"Failed requests: {len(failed)}")

    if successful:
        print(f"Average response time: {sum(successful) / len(successful):.4f}s")
        print(f"Maximum response time: {max(successful):.4f}s")

    print(f"Total test duration: {total_duration:.4f}s")

    if failed:
        print(f"Failure statuses: {failed}")


if __name__ == "__main__":
    main()