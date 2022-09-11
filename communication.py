import requests
import argparse
import json


def get_args():
    # Argparse to get the server ip on which the json
    # request will be sent.
    parser = argparse.ArgumentParser(description="Python honeypot communication")

    # Example `--server-ip localhost:5000`
    # Which specifies the hostname and the port
    # on which the request will be sent.
    parser.add_argument("--server-ip")

    # The prod mode tell us for which logfiles the data
    # should be sent to the server.
    parser.add_argument("--prod", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    # Headers with which the request will be sent so the
    # web server will know that we are sending json data.
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    # We go through all key/values in send_list and use the key
    # as API endpoint and we get the data form the value function
    for key, get_data_fce in {}.items():
        url = f"http://{args.server_ip}/api/{key}"
        print("URL:", url)
        data = get_data_fce()
        if data:
            x = requests.post(url, data=json.dumps(data), headers=headers)
            print("Resp:", x.text)
