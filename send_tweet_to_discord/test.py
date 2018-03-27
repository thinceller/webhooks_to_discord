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

### Function
def main():
    """This is a main function.
    """

    # 検索したいユーザのscreen_nameを設定
    screen_name = "kohe_cuthah"
    # Tweet検索用URL
    url = "https://stream.twitter.com/1.1/statuses/filter.json"
    # webhook url
    webhook_url = "https://discordapp.com/api/webhooks/428220246315237377/ywfPka1_sUcHDLUqNrYHMVX3DtMiWFN6Q8OnVIGP2GqyBZmyYjmsenN_7-G8kxURlQh2"

    auth = create_oauth_session(AUTH_KEY)

    # REST APIからuser_idを取得
    user_id = get_user_id(screen_name, auth)

    while(True):
        try:
            res = requests.post(url, auth=auth, stream=True, data={"follow": user_id})

            if res.status_code == 200:
                print("connect succeed!")

                if res.encoding is None:
                    res.encoding = "utf-8"

                for line in res.iter_lines(chunk_size=1, decode_unicode=True):
                    try:
                        if line:
                            stream = json.loads(line)

                            if "delete" in stream:
                                id = stream["delete"]["status"]["id"]
                                requests.post(webhook_url, data={
                                    "content": "この人はツイ消しをしました。\nTweet id: {0}",
                                    "username": "ツイ消し警察"
                                })
                            else:
                                id = stream["id"]
                                text = "Tweet id: {0}\nhttps://twitter.com/".format(id) + screen_name + "/status/" + stream["id_str"]
                                user_name = stream["user"]["name"]
                                avatar_url = stream["user"]["profile_image_url"]
                                requests.post(webhook_url, data={
                                    "content": text,
                                    "username": user_name,
                                    "avatar_url": avatar_url
                                })
                    
                    except UnicodeEncodeError:
                        print("tweetを取得出来ませんでした。")
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

def get_user_id(screen_name, auth):
    """ Get user_id from screen_name by Twitter REST API
    """

    users_show_url = "https://api.twitter.com/1.1/users/show.json"
    params = {"screen_name": screen_name}

    res = requests.get(users_show_url, auth=auth, params=params)
    user_info = json.loads(res.text)

    return user_info["id"]

### Excute
if __name__ == "__main__":
    main()
