import json
import requests
from requests_oauthlib import OAuth1
import config

### Constants
AUTH_KEY = {
    "consumer_key": config.CONSUMER_KEY,
    "consumer_secret": config.CONSUMER_SECRET,
    "access_token": config.ACCESS_TOKEN,
    "access_token_secret": config.ACCESS_TOKEN_SECRET
}

### Functions
def main():
    """This is a main function.
    """

    track = input("検索ワード？：")

    url = "https://stream.twitter.com/1.1/statuses/filter.json"
    auth = create_oauth_session(AUTH_KEY)

    while(True):
        try:
    res = requests.post(url, auth=auth, stream=True, data={"track": track})

    if res.status_code == 200:
        print("connect succeed!")

                if res.encoding is None:
                    res.encoding = "utf-8"

                for line in res.iter_lines(chunk_size=1, decode_unicode=True):
                    try:
                        if line:
                            stream = json.loads(line)

                            print(stream["user"]["name"])
                            print(stream["text"])
                            print("---------------------------------")
                    
                    except UnicodeEncodeError:
                        pass

    else:
        print("Error: ${res.status_code}")

        except KeyboardInterrupt:
            print("End")
            break

def create_oauth_session(auth_key):
    """Performs authentication.

    :param auth_key: Value and key for authentication
    """

    auth = OAuth1(
        auth_key["consumer_key"],
        auth_key["consumer_secret"],
        auth_key["access_token"],
        auth_key["access_token_secret"]
    )
    return auth

### Excute
if __name__ == "__main__":
    main()
