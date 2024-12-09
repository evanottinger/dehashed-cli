#!/usr/bin/env python3

from requests_ratelimiter import LimiterSession
from requests.auth import HTTPBasicAuth
from pprint import pprint as pp
from datetime import datetime
import argparse
import json
import sys


class DehashedClient:
    def __init__(self, email, api_key):
        self.email = email
        self.api_key = api_key
        self.api_url = "https://api.dehashed.com/search?query="
        self._session = LimiterSession(per_second=5)
        self._session.auth = HTTPBasicAuth(username=self.email, password=self.api_key)
        self._session.headers = {"accept": "application/json"}

    def get(self, query):
        res = self._session.get(f"{self.api_url}{query}")

        if res.status_code == 200:
            return res
        elif res.status_code in [400, 401, 404]:
            pp(res.json)
            exit(1)
        elif res.status_code == 302:
            pp("[!] Invalid/missing query")
            exit(1)


def get_args():
    parser = argparse.ArgumentParser(
        prog="Dehashed CLI",
        description="Query Dehashed's API from the CLI",
        add_help=False,
    )

    parser.add_argument("-e", "--email", required=True)
    parser.add_argument("-k", "--api-key", required=True)
    parser.add_argument("-q", "--query", required=True)
    parser.add_argument(
        "-s",
        "--size",
        type=int,
        default=100,
        help="The number of results to return per query. An integer from 1-10000.",
        required=False,
    )
    parser.add_argument(
        "-o", "--out-file", default=f"./data/{datetime.now()}.json", required=False
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    # Manually error check the range for size so that the argparse help output
    # doesn't contain a list of all possible values.
    if args.size not in range(1, 10001):
        print(f"[!] size must be an integer value between 1 and 10000")
        sys.exit(1)

    return args


def do_query(client, query):
    print("[-] Querying DeHashed API")
    res = client.get(query)
    print("[+] Done!")
    return res.json()


def write_data(data, file_path):
    print("[-] Writing data to file")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("[+] Done!")


def main():
    args = get_args()
    client = DehashedClient(email=args.email, api_key=args.api_key)

    data = do_query(client, args.query)

    if args.verbose:
        pp(data)

    write_data(data, args.out_file)
    print("[+] Operation successful!")


if __name__ == "__main__":
    main()
