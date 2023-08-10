import json
import requests

def count_words(subreddit, word_list, after=None, count=None):
    if count is None:
        count = [0] * len(word_list)
    if after is None:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?after={after}"
    headers = {'User-Agent': 'bhalut'}
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 200:
        data = response.json()
        for topic in data['data']['children']:
            title = topic['data']['title']
            for word in title.split():
                word = word.lower().strip('.,!_?')
                if word in word_list:
                    count[word_list.index(word)] += 1
        next_page = data['data']['after']
        if next_page is None:
            word_count = [(word_list[i], count[i]) for i in range(len(word_list)) if count[i] > 0]
            word_count.sort(key=lambda x: (-x[1], x[0]))
            for word, count in word_count:
                print(f"{word}: {count}")
        else:
            count_words(subreddit, word_list, next_page, count)
