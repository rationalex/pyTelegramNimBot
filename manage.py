import argparse
import requests

import config


def set_hook():
    url = "https://api.telegram.org/bot{token}/{method}".format(
        token=config.AUTH_TOKEN,
        method="setWebhook"
    )
    data = {
        "url": "https://w65i2jwmhb.execute-api.us-west-2.amazonaws.com/v0"
    }

    response = requests.post(url, data=data)
    print(response.json())


def remove_hook():
    url = "https://api.telegram.org/bot{token}/{method}".format(
        token=config.AUTH_TOKEN,
        method="deleteWebhook"
    )

    response = requests.post(url)
    print(response.json())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action",
                        help='set_hook | remove_hook')
    args = parser.parse_args()
    if args.action == 'set_hook':
        set_hook()
    elif args.action == 'remove_hook':
        remove_hook()

if __name__ == "__main__":
    main()
