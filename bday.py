# Thanking everyone who wished me on my birthday

import requests

import json


# Aman's post time

AFTER = 1353233754

TOKEN='CAACEdEose0cBAKVz94LoDIKZCTUKrQPGkQBFUu6knjkqO5ZBQT8WWBoB1yWIKxmsJVtsjK6Opl0vX2g10rKY0GNHf5cKdpB3TYUvZAnjK7TBURXuerMAgGe1Y1ZBJdC3yl9aoSoSyvo2j8yZB4fO3S3T3CDZBYehHJt43jUNVzZA4MgscZBMn7ZAYCZCTCL8XqdvEZD'


def get_posts():

    """Returns dictionary of id, first names of people who posted on my wall

    between start and end time"""

    query = ("SELECT post_id, actor_id, message FROM stream WHERE "

            "filter_key = 'others' AND source_id = me() AND "

            "created_time > 1353233754 LIMIT 200")


    payload = {'q': query, 'access_token': TOKEN}

    r = requests.get('https://graph.facebook.com/fql', params=payload)

    result = json.loads(r.text)

    return result['data']


def commentall(wallposts):

    """Comments thank you on all posts"""

    #TODO convert to batch request later

    for wallpost in wallposts:

        print wallpost

        r = requests.get('https://graph.facebook.com/%s' %

                wallpost['actor_id'])

        url = 'https://graph.facebook.com/%s/comments' % wallpost['post_id']
        print url
        exit(1)
        user = json.loads(r.text)

        message = 'Thanks %s :)' % user['first_name']

        payload = {'access_token': TOKEN, 'message': message}

        s = requests.post(url, data=payload)


        print "Wall post %s done" % wallpost['post_id']


if __name__ == '__main__':

    commentall(get_posts())
