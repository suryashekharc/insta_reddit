# Upload to instagram
# Check for image in images.generated, if it also exists in images.uploaded
# If not, upload it and move it to images.uploaded

from instabot import Bot
from insta_reddit import config
bot = Bot()

bot.login(username=config.instabot_username,
          password=config.instabot_password)

bot.upload_photo('/Users/suryasekharchakraborty/Documents/insta_reddit/insta_reddit/'
                 'content/images/generated/title_g76gmj.jpg',
                 caption ="#ULPT")
