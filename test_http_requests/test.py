import config
from requests_oauthlib import OAuth1Session

### Constants
OAUTH_KEY = {
    "consumer_key": config.CONSUMER_KEY, 
    "consumer_secret": config.CONSUMER_SECRET,
    "access_token": config.ACCESS_TOKEN,
    "access_token_secret": config.ACCESS_TOKEN_SECRET
}

### Functions
def main():
    status = input("What's happening?: ")
    update_status(status)

def create_oauth_session(oauth_key):
    oauth = OAuth1Session(
        oauth_key["consumer_key"],
        oauth_key["consumer_secret"],
        oauth_key["access_token"],
        oauth_key["access_token_secret"]
    )
    return oauth

def update_status(status):
    url = "https://api.twitter.com/1.1/statuses/update.json"
    params = { "status": status }

    oauth = create_oauth_session(OAUTH_KEY)
    res = oauth.post(url, params = params)

    # エラーが出た時はエラーコードを表示する
    if res.status_code != 200:
        print("ERROR: %d" % res.status_code)
    else:
        print("Tweet Success!")

### Excute
if __name__ == "__main__":
    main()
