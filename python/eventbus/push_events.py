import argparse
import time

import requests

from eventbus.redis import RedisConsumer


def main(args: argparse.Namespace):
    consumer = RedisConsumer(args.parttion_keys)
    while True:
        for event in consumer.get_events():
            requests.post(args.consumer_url, json=event)

        time.sleep(5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Event consumer",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-u", "--consumer-url")
    parser.add_argument("-p", "--partition-keys")
    main(parser.parse_args())
