"""
Download top K posts from Reddit and save them to GSheets DB if not already saved.
"""
import argparse
import sys
import os
import html

import pandas as pd
import praw
from insta_reddit import credentials
from insta_reddit.code.sheets_db import SheetsDb  # To append records to sheets


def initialize():
    # NOTE: Ensure the credentials.py file is present in the current directory
    reddit_obj = praw.Reddit(client_id=credentials.client_id,
                             client_secret=credentials.client_secret,
                             user_agent=credentials.user_agent,
                             username=credentials.username)
    if not reddit_obj.read_only:  # Flag to ensure this object has been correctly configured
        raise Exception("Reddit object not configured correctly to be read_only.")
    return reddit_obj


def get_posts(reddit_obj,
              subreddit_name="unethicallifeprotips",
              post_count=20,
              time_filter="month",
              fields=None):
    """
    Get all the posts as a pandas dataframe
    :param reddit_obj:      Instance of PRAW API
    :param subreddit_name:  Name of the subreddit
    :param post_count:      Number of posts
    :param time_filter:     day/month/week etc since we are sorting by top
    :param fields:          List of fields to return (Refer: sample_object_json.txt)
    :return:                Pandas DF with "count" rows and "len(kwargs)" columns
    """
    # TODO: Add support for hot along with top

    if fields is None:  # To avoid passing mutable default args
        fields = ["title", "selftext", "author", "url", "id"]
    if "id" not in fields:  # To ensure the unique ID of a post is always captured
        fields.append("id")
    content_dict = {field: [] for field in fields}  # Initializing dict

    # Metadata of the fields of a submission are available here:
    # https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
    # PRAW uses lazy objects so that network requests to ...
    # ... Reddit's API are only issued when information is needed.
    for submission in reddit_obj.subreddit(subreddit_name).top(limit=post_count,
                                                               time_filter=time_filter):
        for field in fields:
            content_dict[field].append(getattr(submission, field))
    return pd.DataFrame(content_dict)


def cleanup_content(content_df, colnames=None):
    """
    Read the dumped posts and clean up the text
    Also convert the HTML entities to characters, e.g. '&gt;' to '>'
    :param content_df:  Dataframe containing columns in colnames to clean up
    :param colnames:    Which columns to clean up
    :return:
    """
    # TODO: Filter out selftext containing 'edit', 'thanks', 'upvote'
    # NOTE: Selftext containing the above keywords are not uploaded as caption
    if colnames is None:
        colnames = ['title']

    def cleanup_ulpt_text(text):
        if "request" not in text.lower():
            text = text[text.find(' '):]
            return None if len(text) < 20 or len(text) > 500 else html.unescape(text)
        return None  # TODO: Add support for ULPT request

    for colname in colnames:
        content_df[colname] = content_df.apply(lambda row: cleanup_ulpt_text(row[colname]), axis=1)
    return content_df.dropna()


def save_posts_to_gsheets(content_df):
    # Iterate through rows of content_df. If id not in GSheet, append row.
    credentials_path = "/".join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1]) + \
                       "/service_account.json"
    sdb = SheetsDb(sheet_id=credentials.sheets_url,
                   credentials_path=credentials_path)
    for index, row in content_df.iterrows():
        my_list = [row.title, row.selftext, row.author.name, row.url, row.id]
        print("Trying {}".format(row.id))
        if sdb.get_row_for_id(row.id) == -1:  # i.e. ID not found
            sdb.append_row(my_list)
        else:
            print("Found at {}".format(sdb.get_row_for_id(row.id)))


def main(args):
    reddit_obj = initialize()
    content_df = get_posts(reddit_obj,
                           str(args.subreddit_name),
                           int(args.post_count),
                           str(args.time_filter),
                           args.fields.replace(" ", "").split(","))
    cleaned_content_df = cleanup_content(content_df)
    save_posts_to_gsheets(cleaned_content_df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--subreddit_name', dest='subreddit_name', default="unethicallifeprotips",
                        help="""Name of the subreddit""")
    parser.add_argument('--post_count', dest='post_count', default=15,
                        help="""Number of posts to fetch""")
    parser.add_argument('--time_filter', dest='time_filter', default="month",
                        help="""day/month/week etc since we are sorting by top""")
    parser.add_argument('--fields', dest='fields', default="title,selftext,author,url,id",
                        help="""Comma-separated list of fields to save""")

    main(args=parser.parse_args())
    sys.exit(0)
