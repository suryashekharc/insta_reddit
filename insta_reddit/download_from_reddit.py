"""
# IMP - Have a credentials.py file in the same directory containing the following text:
client_id='your_client_id'
client_secret='your_client_secrety'
user_agent='your_user_agent'
username='your_user_name'
"""

import argparse
import os
import sys

import pandas as pd
import praw
from insta_reddit import credentials

"""
1. Keep a record of all posts downloaded
2. Download the top K posts over the last T time period
3. Strip it down to the ULPT itself
4. Append to downloaded if not already covered
5. Add link to post and username for credits on the post
6. Bam!

TODO: If the post itself has selftext, add it to a separate image clubbed together
TODO: If it is a ULPT request, add the top comment as the next image
"""
reddit = None  # Reddit instance


def initialize():
    # NOTE: Ensure the credentials.py file is present in the current directory
    global reddit
    reddit = praw.Reddit(client_id=credentials.client_id,
                         client_secret=credentials.client_secret,
                         user_agent=credentials.user_agent,
                         username=credentials.username)
    if not reddit.read_only:  # Flag to ensure this object has been correctly configured
        raise Exception("Reddit object not configured correctly to be read_only.")


def get_posts(subreddit_name="unethicallifeprotips",
              post_count=20,
              time_filter="month",
              fields=None):
    """
    Get all the posts as a pandas dataframe
    :param subreddit_name:  Name of the subreddit
    :param post_count:      Number of posts
    :param time_filter:     day/month/week etc since we are sorting by top
    :param fields:          List of fields to return (Refer: sample_object_json.txt)
    :return:                Pandas DF with "count" rows and "len(kwargs)" columns
    """
    # TODO: Add support for hot along with top
    global reddit

    if fields is None:  # To avoid passing mutable default args
        fields = ["title", "selftext", "author", "url", "id"]
    if "id" not in fields:  # To ensure the unique ID of a post is always captured
        fields.append("id")
    content_dict = {field: [] for field in fields}  # Initializing dict

    # Metadata of the fields of a submission are available here:
    # https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
    # PRAW uses lazy objects so that network requests to ...
    # ... Reddit’s API are only issued when information is needed.
    for submission in reddit.subreddit(subreddit_name).top(limit=post_count,
                                                           time_filter=time_filter):
        for field in fields:
            content_dict[field].append(getattr(submission, field))
    return pd.DataFrame(content_dict)


def cleanup_content(content_df, colnames=None):
    """
    Read the dumped posts and clean up the text
    :param content_df:  Dataframe containing columns in colnames to clean up
    :param colnames:    Which columns to clean up
    :return:
    """
    if colnames is None:
        colnames = ['title']

    def cleanup_ulpt_text(text):
        if "request" not in text.lower():
            text = text[text.find(' '):]
            return None if len(text) < 20 or len(text) > 500 else text
        return None  # TODO: Add support for ULPT request

    for colname in colnames:
        content_df[colname] = content_df.apply(lambda row: cleanup_ulpt_text(row[colname]), axis=1)
    return content_df.dropna()


def save_posts(content_df, output_file="/content/posts/downloaded_posts.csv"):
    """
    Save posts in the content df at an output path after checking if they already exist
    :param content_df:
    :param output_file:
    :return:
    """
    cur_folder_path = os.path.dirname(os.path.realpath(__file__))
    cur_file_path = cur_folder_path + output_file
    dir_path = "/".join(cur_file_path.split('/')[:-1])
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    if os.path.exists(cur_file_path):  # To ensure we don't write the same post multiple times
        original_df = pd.read_csv(cur_file_path)
        combined_df = pd.concat([original_df, content_df]).drop_duplicates(
            subset=["id"])
        # Interestingly, without reset_index, the original indices will be added e.g. 0,1,2,0,1
        combined_df.to_csv(cur_file_path, mode='w', header=True, index=False)
    else:
        content_df.to_csv(cur_file_path, mode='w', header=True, index=False)


def main(args):
    initialize()
    content_df = get_posts(args.subreddit_name,
                           args.post_count,
                           args.time_filter,
                           args.fields.replace(" ", "").split(","))
    save_posts(cleanup_content(content_df), args.output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--subreddit_name', dest='subreddit_name', default="unethicallifeprotips",
                        help="""Name of the subreddit""")
    parser.add_argument('--post_count', dest='post_count', default=5,
                        help="""Number of posts to fetch""")
    parser.add_argument('--time_filter', dest='time_filter', default="month",
                        help="""day/month/week etc since we are sorting by top""")
    parser.add_argument('--fields', dest='fields', default="title,selftext,author,url,id",
                        help="""Comma-separated list of fields to save""")
    parser.add_argument('--output_file', dest='output_file',
                        default="/content/posts/downloaded_posts.csv",
                        help="""Name of output file""")
    main(args=parser.parse_args())
    sys.exit(0)
