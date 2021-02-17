from sys import stderr
import hashlib


def status_decode(response):
    if response.status_code == 200 or response.status_code == 201 or response.status_code == 202:
        if response.json()['errno'] != 200 and response.json()['errno'] != 201 and response.json()['errno'] != 202:
            if response.json()['errno'] == 429:
                stderr.write(f"\nServer response is {response.json()['errno']} == Too fast | Original: "
                               f"\n{response.json()['error']}\n")
            elif response.json()['errno'] == 400:
                stderr.write(f"\nServer response is {response.json()['errno']} == Syntax error | Original: "
                               f"\n{response.json()['error']}\n")
            elif response.json()['errno'] == 401:
                stderr.write(f"\nServer response is {response.json()['errno']} == Auth required | Original: "
                               f"\n{response.json()['error']}\n")
            elif response.json()['errno'] == 403:
                stderr.write(f"\nServer response is {response.json()['errno']} == Forbidden | Original: "
                               f"\n{response.json()['error']}\n")
            elif response.json()['errno'] == 404:
                stderr.write(f"\nServer response is {response.json()['errno']} == Not found | Original: "
                               f"\n{response.json()['error']}\n")
            elif response.json()['errno'] == 434:
                stderr.write(f"\nServer response is {response.json()['errno']} == Offline | Original: "
                               f"\n{response.json()['error']}\n")
            elif response.json()['errno'] == 503:
                stderr.write(f"\nServer response is {response.json()['errno']} == Maintenance | Original: "
                               f"\n{response.json()['error']}\n")
            elif response.json()['errno'] == 423:
                stderr.write(f"\nServer response is {response.json()['errno']} == API key blocked | Original: "
                               f"\n{response.json()['error']}\n")
            else:
                stderr.write(f"\nServer response is {response.json()} == Something nasty happened\n")
    else:
        stderr.write(f"\nServer response is {response.status_code} == Something nasty happened | {response.json()}\n")


def generate_hash(app_id):
    return hashlib.md5(app_id).hexdigest()