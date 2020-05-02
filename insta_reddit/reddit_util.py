import praw

reddit = praw.Reddit(client_id='74a3xOgxuVg7GA', client_secret='eZs_q8Znv9_Sy4n3PvitM2raeWY',
                     user_agent='ulpt', username='Kindafunny2510')

print(reddit.read_only)

for submission in reddit.subreddit('learnpython').hot(limit=10):
    print(submission.title)
