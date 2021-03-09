#!/bin/bash

/Users/$USER/Documents/insta_reddit/venv/bin/python3 insta_reddit/code/download_from_reddit.py --post_count 15 --subreddit_name LifeProTips
/Users/$USER/Documents/insta_reddit/venv/bin/python3 insta_reddit/code/draw_text_on_image.py
/Users/$USER/Documents/insta_reddit/venv/bin/python3 insta_reddit/code/upload_to_instagram.py --post_count 1

