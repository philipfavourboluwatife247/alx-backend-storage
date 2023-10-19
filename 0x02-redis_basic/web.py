#!/usr/bin/env python3
import requests
import time
import redis
from functools import wraps

# Initialize a Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def cache_with_expiry(seconds):
    def decorator(func):
        @wraps(func)
        def wrapped(url):
            key = f"cached:{url}"
            cached_result = redis_client.get(key)
            if cached_result:
                return cached_result.decode('utf-8')

            result = func(url)
            redis_client.setex(key, seconds, result)
            return result

        return wrapped

    return decorator


@cache_with_expiry(10)
def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to retrieve page: {response.status_code}"


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    for _ in range(3):
        print(get_page(url))
