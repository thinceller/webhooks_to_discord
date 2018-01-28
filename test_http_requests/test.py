from requests_oauthlib import OAuth1Session
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

    status = input("What's happening?: ")
    update_status(status)

def create_oauth_session(auth_key):
    """Performs authentication.

    :param auth_key: Value and key for authentication
    """

    auth = OAuth1Session(
        auth_key["consumer_key"],
        auth_key["consumer_secret"],
        auth_key["access_token"],
        auth_key["access_token_secret"]
    )
    return auth

def update_status(status):
    """Tweet content entered at the console.

    :param status: Input text.
    """

    url = "https://api.twitter.com/1.1/statuses/update.json"
    params = {"status": status}

    auth = create_oauth_session(AUTH_KEY)
    res = auth.post(url, params=params)

    # エラーが出た時はエラーコードを表示する
    if res.status_code != 200:
        print("ERROR: %d" % res.status_code)
    else:
        print("Tweet Success!")

### Excute
if __name__ == "__main__":
    main()
