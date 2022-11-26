import argparse
from datetime import datetime, timedelta
import magic
import os
import random
import sys
import time

from mastodon import Mastodon

# A Mastodon bot script to post a random bunny every hour.
# (Currently runs at the half hour mark.)

def run_client_loop(username, password, bunny_folder):
    mime = magic.Magic(mime=True)
    while True:
        try:
            mastodon_client = Mastodon(
                client_id=client_secret,
                api_base_url="https://" + args.instance
            )
            mastodon_client.log_in(
                username=username,
                password=password,
                scopes=["read", "write"],
                to_file=username + ".secret"
            )
            print(f"Successfully logged in as {args.username}")
            bunny_pictures = os.listdir(bunny_folder)
            random_bunny = f"{bunny_folder}/{random.choice(bunny_pictures)}"
            print(f"Time to post a bunny! I choose: {random_bunny}")
            media_posted = mastodon_client.media_post(
                random_bunny, mime_type=mime.from_file(random_bunny))
            status = mastodon_client.status_post("", media_ids=[media_posted])
            if status:
                print(f"  ... posted! toot id: {status['url']}")
            else:
                print("  ... failed. :-(")
        except:
            print(f"login failed!")
            
        # Now wait an hour before we post again.
        dt = datetime.now() + timedelta(hours=1)
        dt = dt.replace(minute=1)

        while datetime.now() < dt:
            time.sleep(1)

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

    print("Bunnybot activated!")
    run_client_loop(args.username, args.password, args.bunny_folder)


    
        
