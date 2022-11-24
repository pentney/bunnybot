import argparse
import magic
import os
import random
import sys
import time

from mastodon import Mastodon
import requests

# A Mastodon bot script to post a random bunny every hour.

def run_server_loop(mastodon_client, bunny_path, bunny_choices):
    mime = magic.Magic(mime=True)
    while True:
        random_bunny = f"{bunny_path}/{random.choice(bunny_choices)}"
        print(f"Time to post a bunny! I choose: {random_bunny}")
        media_posted = mastodon_client.media_post(
            random_bunny, mime_type=mime.from_file(random_bunny))
        status = mastodon_client.status_post("", media_ids=[media_posted])
        if status:
            print(f"  ... posted! toot id: {status['url']}")
        else:
            print("  ... failed. :-(")
        
        # Now wait an hour before we post again.
        time.sleep(3600)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", help="Mastodon server instance")
    parser.add_argument("--username", help="Account username")
    parser.add_argument("--password", help="Account password")
    parser.add_argument("--register_app", type=bool, default=False, help="Register app (only run once)")
    parser.add_argument("--bunny_folder", default="images/", help="A folder full of bunny pictures")
    args = parser.parse_args()

    client_secret = "rabbit_every_hour.secret"
    if args.register_app:
        Mastodon.create_app(
            "RabbitEveryHour",
            api_base_url = "https://" + args.instance,
            to_file = client_secret
        )

    try:
        mastodon_client = Mastodon(
            client_id=client_secret,
            api_base_url="https://" + args.instance
        )
        mastodon_client.log_in(
            username=args.username,
            password=args.password,
            scopes=["read", "write"],
            to_file=args.username + ".secret"
        )
        print(f"Successfully logged in as {args.username}")
    except:
        print(f"login failed!")
        sys.exit(1)

    bunny_pictures = os.listdir(args.bunny_folder)
    print("Bunnybot activated!")
    run_server_loop(mastodon_client, args.bunny_folder, bunny_pictures)


    
        
