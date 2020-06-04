# Upload to instagram
# Check for image in images.generated, if it also exists in images.uploaded
# If not, upload it and move it to images.uploaded

"""
# NOTE: Run the following lines from a Python console to enable hashtag generation:
import nltk
nltk.download("punkt")
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
"""
import os
import shutil

import nltk
from nltk.stem import WordNetLemmatizer

from instabot import Bot
from insta_reddit import credentials

DEFAULT_HASHTAGS = " #ULPT #unethical #lifeprotips #lpt"


def get_hashtags(text, max_num_hashtags=15):
    lemmatizer = WordNetLemmatizer()
    hashtags = list(set([lemmatizer.lemmatize(word)
                         for (word, pos) in nltk.pos_tag(nltk.word_tokenize(text))
                         if pos[0] == 'N']))
    hashtag_string = "#" + " #".join(hashtags[:min(len(hashtags), (max_num_hashtags - 4))]) \
        if len(hashtags) > 0 \
        else ""
    hashtag_string += DEFAULT_HASHTAGS
    print("Hashtags generated: {}".format(hashtag_string))
    return hashtag_string


def get_caption(author, hashtags, url):
    return hashtags + "  Author: u/{}  URL: {}".format(author, url)


def move_to_uploaded(file_path):
    shutil.move(file_path, "uploaded".join(file_path.rsplit("generated", 1)))
    # This syntax is to replace the last occurrence of generated in the file path with uploaded
    # to avoid a potential "generated" string in some other part of the filepath getting replaced
    pass


def already_uploaded():
    return True


def find_posts_to_upload():
    """
    Iterate through the "generated" folder
    Look for images there which are not there in "uploaded"
    Find their data (text/author/etc) using the file_name and by filtering the CSV for it
    Return the CSV row as a dict, and the files to upload
    """
    cur_folder_path = os.path.dirname(os.path.realpath(__file__))
    title_path = "".join([cur_folder_path, "/content/images/generated/"])

    pass

def upload_posts():
    # bot = Bot()
    #
    # bot.login(username=credentials.instabot_username,
    #           password=credentials.instabot_password)
    #
    # bot.upload_photo('/Users/suryasekharchakraborty/Documents/insta_reddit/insta_reddit/'
    #                  'content/images/generated/title_g76gmj.jpg',
    #                  caption="#ULPT")
    pass
