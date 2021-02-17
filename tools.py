from sys import stderr
import hashlib


def status_decode(response):
    if response.status_code != 200 or response.status_code != 201 or response.status_code != 202:
        if response.status_code == 429:
            stderr.write(f"Server response is {response.status_code} == Too fast (more than 1 request per minute)")
        elif response.status_code == 400:
            stderr.write(f"Server response is {response.status_code} == Syntax error")
        elif response.status_code == 401:
            stderr.write(f"Server response is {response.status_code} == Auth required")
        elif response.status_code == 403:
            stderr.write(f"Server response is {response.status_code} == Forbidden")
        elif response.status_code == 404:
            stderr.write(f"Server response is {response.status_code} == Not found")
        elif response.status_code == 434:
            stderr.write(f"Server response is {response.status_code} == Offline")
        elif response.status_code == 503:
            stderr.write(f"Server response is {response.status_code} == Maintenance")
        elif response.status_code == 423:
            stderr.write(f"Server response is {response.status_code} == API key blocked")
        else:
            stderr.write(f"Server response is {response.status_code} == Something nasty happened")


def generate_hash(app_id):
    return hashlib.md5(app_id).hexdigest()