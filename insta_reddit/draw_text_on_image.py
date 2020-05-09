import os
from insta_reddit.image_utils import ImageText
# Download and install fonts from: https://www.cufonfonts.com/font/helvetica-neue-9

def get_title_and_self_text():
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
    return title, self_text


def get_bg_img():
    cur_folder_path = os.path.dirname(os.path.realpath(__file__))
    img_file_path = cur_folder_path + "/content/images/resources/square-frame-small.jpg"
    img = ImageText(img_file_path)
    img = ImageText((500, 500), background=(255, 255, 255))
    return img


def get_format():
    return {'subreddit_font': 'Helvetica95Black.ttf',
            'title_font': 'Helvetica65Medium_22443.ttf',
            'self_text_font': 'Helvetica55Roman_22439.ttf',
            'subreddit_color': (159,4,4),
            'title_color': (33,32,32),
            'self_text_color':(0,0,0)}


def write_on_img():
    title, self_text = get_title_and_self_text()
    img_1 = get_bg_img()
    img_2 = get_bg_img()
    # TODO: Figure out how to vertically align centrally as well
    img_1.write_text_box((50, 20), text="ULPT:", box_width=400, font_filename=get_format()['subreddit_font'],
                       font_size=60, color=get_format()['subreddit_color'], place='center')
    img_1.write_text_box((50, 140), title, box_width=400, font_filename=get_format()['title_font'],
                       font_size=15, color=get_format()['title_color'], place='justify')
    img_2.write_text_box((50, 50), self_text, box_width=400, font_filename=get_format()['self_text_font'],
                       font_size=12, color=get_format()['self_text_color'], place='justify')
    img_1.save('sample-imagetext_1.png')
    img_2.save('sample-imagetext_2.png')

write_on_img()