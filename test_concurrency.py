from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import httpx

BASE_URL = "http://127.0.0.1:8000"
PRODUCT_ID = 1  # Change to an existing product ID

# Prepare exactly 10 units of stock
response = httpx.patch(
    f"{BASE_URL}/products/{PRODUCT_ID}",
    json={"quantity": 10},
)
response.raise_for_status()

barrier = Barrier(2)


def place_order():
    # Make both threads wait, then release them together
    barrier.wait()

    return httpx.post(
        f"{BASE_URL}/orders/",
        json={
            "product_id": PRODUCT_ID,
            "quantity": 7,
        },
        timeout=15,
    )


with ThreadPoolExecutor(max_workers=2) as executor:
    futures = [
        executor.submit(place_order)
        for _ in range(2)
    ]

    responses = [future.result() for future in futures]

for i, response in enumerate(responses, start=1):
    print(f"Request {i}: {response.status_code}")
    print(response.text)

product_response = httpx.get(
    f"{BASE_URL}/products/{PRODUCT_ID}"
)
product_response.raise_for_status()

print("Final stock:", product_response.json()["quantity"])
