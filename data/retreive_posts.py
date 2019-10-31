import json
import requests
import time
import pandas as pd
from data.config import FACEBOOK_TOKEN


def retrieve():
    post_ids_path = 'post_ids.csv'
    post_ids = pd.read_csv(post_ids_path)

    my_df = []

    for post_id in post_ids['id']:
        print(f"Retrieving post {post_id}")
        post_json = get_post(post_id)
        print(post_json)

        post = {
            "id" : post_id,
            "type" : post_json.get('type'),
            "date" : post_json.get('created_time'),
            "num_likes" : post_json['like']['summary']['total_count'] if 'like' in post_json and 'total_count' in post_json['like']['summary'] else 0,
            "num_shares" : post_json['shares']['count'] if 'shares' in post_json else 0,
            "num_comments" : post_json['comments']['summary']['total_count'] if 'comments' in post_json and 'total_count' else 0,
            "num_angry" : post_json['angry']['summary']['total_count'] if 'angry' in post_json and 'total_count' in post_json['angry']['summary'] else 0,
            "num_love" :  post_json['love']['summary']['total_count'] if 'love' in post_json and 'total_count' in post_json['love']['summary'] else 0,
            "num_haha" :  post_json['haha']['summary']['total_count'] if 'haha' in post_json and 'total_count' in post_json['haha']['summary'] else 0,
            "num_wow" :  post_json['wow']['summary']['total_count'] if 'wow' in post_json and 'total_count' in post_json['wow']['summary'] else 0,
            "num_sad" :  post_json['sad']['summary']['total_count'] if 'sad' in post_json and 'total_count' in post_json['sad']['summary'] else 0,
            "num_thankful" :  post_json['thankful']['summary']['total_count'] if 'thankful' in post_json and 'total_count' in post_json['thankful']['summary'] else 0,
            "text" : post_json.get('message'),
            "permanent_link" : post_json.get('permalink_url'),
            "name" : post_json.get('name'),
            "picture" : post_json.get('picture'),
            "full_picture" : post_json.get('full_picture'),
            "source" : post_json.get('source')
        }
        my_df.append(post)
        time.sleep(20)

    # dump posts to file
    with open('posts.json', 'w', encoding='utf-8') as f:
        json.dump(my_df, f, indent=4, ensure_ascii=False)


def get_post(post_id):
    fields = "permalink_url,name,source,picture,full_picture,type,message," \
             "created_time,shares," \
             "reactions.limit(0).summary(true),comments.limit(0).summary(true)," \
             "reactions.type(LIKE).limit(0).summary(true).as(like)," \
             "reactions.type(LOVE).limit(0).summary(true).as(love)," \
             "reactions.type(WOW).limit(0).summary(true).as(wow)," \
             "reactions.type(HAHA).limit(0).summary(true).as(haha)," \
             "reactions.type(SAD).limit(0).summary(true).as(sad)," \
             "reactions.type(ANGRY).limit(0).summary(true).as(angry)," \
             "reactions.type(THANKFUL).limit(0).summary(true).as(thankful)"

    url = f"https://graph.facebook.com/v3.2/{post_id}?fields={fields}&access_token={FACEBOOK_TOKEN}"
    result = requests.get(url)
    return result.json()


if __name__ == '__main__':
    retrieve()
