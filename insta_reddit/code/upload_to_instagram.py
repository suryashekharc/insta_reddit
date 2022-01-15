"""
Upload to instagram
Check GSheets for images not uploaded yet
Check if those IDs are available in images/generated
If found, check if it also contains a self_text
Upload them together, move them to uploaded, and update GSheets with post ID
"""

# TODO: See if multiple photo uploads is supported
import os
import shutil
import glob
import argparse
import sys
from pathlib import Path
git_root = str(Path(__file__).parent.parent.parent.resolve())
sys.path.append(git_root)
import html

import nltk
from nltk.stem import WordNetLemmatizer

from instabot import Bot
from insta_reddit import credentials
from insta_reddit.code.sheets_db import SheetsDb

DEFAULT_CAPTION_PREFIX = "Unethical life pro tips be like... "
DEFAULT_HASHTAGS = " #lifeprotips #lpt"
MAX_NUM_HASHTAGS = 18


def get_hashtags(text):
    """
    Returns a string of hashtags generated from the text
    :param str text:    The text of the title
    :return:            Space separated hashtags generated
    :rtype:             str
    """
    """
    # NOTE: Run the following lines from a Python console to enable hashtag generation:
    import nltk
    nltk.download("punkt")
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    """
    # TODO: Remove stopwords
    lemmatizer = WordNetLemmatizer()
    hashtags = list(set([lemmatizer.lemmatize(word)
                         for (word, pos) in nltk.pos_tag(nltk.word_tokenize(text))
                         if pos[0] == 'N']))  # use nouns to get hashtags
    hashtag_string = "#" + " #".join(hashtags[:min(len(hashtags), (MAX_NUM_HASHTAGS - 4))]) \
        if len(hashtags) > 0 \
        else ""  # total upto 15+4 = 19 hashtags (any more and Instagram starts lowering SEO)
    hashtag_string += DEFAULT_HASHTAGS
    print("Hashtags generated: {}".format(hashtag_string))
    return hashtag_string


def get_caption(record):
    """
    Return the complete caption for a post
    :param dict record: dict containing 'title', 'author', 'url' in its keys
    :return:            caption for the post to be uploaded
    :rtype:             str
    """
    hashtags = get_hashtags(record['title'])
    author, url = record['author'], record['url']
    prefix_text = DEFAULT_CAPTION_PREFIX
    if record['selftext']:
        st = html.unescape(record['selftext'])
        prefix_text = st
    return prefix_text + hashtags + \
           "  Author: u/{}  URL: {}".format(author, url)


def move_to_uploaded(file_path):
    shutil.move(file_path, "uploaded".join(file_path.rsplit("generated", 1)))
    # This syntax is to replace the last occurrence of generated in the file path with uploaded
    # to avoid a potential "generated" string in some other part of the filepath getting replaced
    pass


def get_image_location(post_id):
    """
    Returns a list of image file paths for a given post ID
    :param str post_id: To be found in file name
    :return:            List of image file paths in /content/images/generated/title with the post ID
    :rtype:             list(str)
    """
    cur_folder_path = "/".join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])
    title_path = "".join([cur_folder_path, "/content/images/generated/title"])
    all_images_paths = glob.glob(title_path + "*" + post_id + ".jpg")
    return all_images_paths


def upload_posts(record):
    """

    :param record:
    :return:
    """
    bot = Bot()
    bot.login(username=credentials.instabot_username,
              password=credentials.instabot_password)

    images = get_image_location(record['id'])
    if not images:
        print("Image file not found for ID: {}".format(record['id']))
        return False

    if len(images) == 1:  # contains only title
        bot.upload_photo(images[0], caption=get_caption(record))
        return True
    elif len(images) == 2:  # contains title + selftext
        print("No support yet for multiple image uploads.")
        return False


def main(args):
    credentials_path = "/".join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1]) + \
                       "/service_account.json"
    sdb = SheetsDb(sheet_id=credentials.sheets_url,
                   credentials_path=credentials_path)
    unuploaded_posts = sdb.get_unuploaded_rows()
    for unuploaded_post in unuploaded_posts[:int(args.post_count)]:
        post_id = unuploaded_post['id']
        upload_posts(unuploaded_post)
        sdb.update_image_uploaded(post_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--post_count', dest='post_count', default=1,
                        help="""Number of posts to post at one call""")
    main(args=parser.parse_args())
    sys.exit(0)
