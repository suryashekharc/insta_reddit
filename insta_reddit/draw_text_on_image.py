"""
Read CSV of posts and generate images for them
"""
import csv
import json
import os
from pathlib import Path

from insta_reddit.image_utils import ImageText


# Download and install fonts from: https://www.cufonfonts.com/font/helvetica-neue-9


def get_title_and_self_text(
        record=None):  # Ensure title < 400 characters, self_text < 830 characters
    if record is None:
        title = " Get in the habit of playing Rock Paper Scissors with people, but make sure you " \
                "consistently lose with the same throw. Eventually they will learn to expect the same " \
                "throw and you can win any game you actually care about."
        print(len(title))
        self_text = "My girlfriend and I play random rock paper scissors games for little prizes. " \
                    "Whoever loses has to do X, take out the trash, go to the store for cigs, whatever. " \
                    "I noticed after a bit that I habitually throw rock %90 of the time unless " \
                    "I'm actively trying not to. She figured it out and nearly always wins. " \
                    "So now when I want to win I just throw scissors, but I keep losing most of the time " \
                    "so I can win when it matters(to me)."
        print(len(self_text))
    else:
        title, self_text = record['title'], record['selftext']

    if self_text is None or self_text == "" or len(self_text) < 5:
        if title is None or len(title) >= 400 or len(self_text) >= 830:
            return None, None
        else:
            return title, None
    return title, self_text


def get_bg_img():
    # Returns a white background ImageText object
    img = ImageText((1500, 1500), background=(255, 255, 255))
    return img


def get_format():
    # Format of the text, courtesy Avishek Rakshit
    return {'subreddit_font': 'Helvetica95Black.ttf',
            'title_font': 'Helvetica65Medium_22443.ttf',
            'self_text_font': 'Helvetica55Roman_22439.ttf',
            'subreddit_color': (159, 4, 4),
            'title_color': (33, 32, 32),
            'self_text_color': (0, 0, 0)
            }


def get_img_output_file_paths(record):
    # File paths to save the generated images to
    cur_folder_path = os.path.dirname(os.path.realpath(__file__))
    title_path = "".join(
        [cur_folder_path, "/content/images/generated/title_", record['id'], ".jpg"])
    self_text_path = "".join(
        [cur_folder_path, "/content/images/generated/self_text_", record['id'], ".jpg"])
    # creating directory structure if needed
    Path("/".join(title_path.split('/')[:-1])).mkdir(parents=True, exist_ok=True)
    return title_path, self_text_path


def image_generated(record):
    # Returns True if image has already been generated or uploaded
    cur_folder_path = os.path.dirname(os.path.realpath(__file__))
    title_path = "".join(
        [cur_folder_path, "/content/images/generated/title_", record['id'], ".jpg"])
    if Path(title_path).is_file() or \
            Path(title_path.replace("generated/title_", "uploaded/title_")).is_file():
        return True


def write_on_img(record=None):
    # Generates image(s) for a record with the specified text
    record = json.loads(json.dumps(record))
    if image_generated(record):
        return
    title, self_text = get_title_and_self_text(record)
    title_op, self_text_op = get_img_output_file_paths(record)

    # Write title_img by default for everything, unless either title or self text cross the threshold.
    # Save it as img_title_<<id>>.jpg
    # Write self_text_img only if there's some sizeable self_text.
    # img_self_text_<<id>>.jpg
    if title:
        title_img = get_bg_img()
        title_img.write_vertically_centred_text_box(left_padding=150, upper=0, lower=750,
                                                    text="ULPT:",
                                                    box_width=1200,
                                                    font_filename=get_format()['subreddit_font'],
                                                    font_size=180,
                                                    color=get_format()['subreddit_color'],
                                                    place='center')
        title_img.write_vertically_centred_text_box(left_padding=150, upper=450, lower=1350,
                                                    text=title,
                                                    box_width=1200,
                                                    font_filename=get_format()['title_font'],
                                                    font_size=60, color=get_format()['title_color'],
                                                    place='left')

        title_img.save(title_op)
        print("Image generated.")

    if self_text:
        self_text_img = get_bg_img()
        self_text_img.write_vertically_centred_text_box(left_padding=150, upper=300, lower=1200,
                                                        text=self_text, box_width=1200,
                                                        font_filename=get_format()[
                                                            'self_text_font'],
                                                        font_size=60,
                                                        color=get_format()['self_text_color'],
                                                        place='left')
        self_text_img.save(self_text_op)


def main(csv_path="/content/posts/downloaded_posts.csv"):
    cur_folder_path = os.path.dirname(os.path.realpath(__file__))
    cur_file_path = cur_folder_path + csv_path
    input_file = csv.DictReader(open(cur_file_path))
    for row in input_file:
        write_on_img(row)


if __name__ == "__main__":
    main()
