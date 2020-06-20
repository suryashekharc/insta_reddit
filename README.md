# insta_reddit

![insta_reddit flow](https://i.imgur.com/zrZVcCR.jpg)


1. Download top K posts from a subreddit
(chosen [r/unethicallifeprotips](https://www.reddit.com/r/UnethicalLifeProTips/) for this).
2. Generate an image out of those posts.
3. Generate a caption for those posts.
4. Upload them to [an Instagram account](https://www.instagram.com/unethical.lifeprotips/).
## Installation
#### Setting up credentials
1. Get [PRAW credentials](https://praw.readthedocs.io/en/latest/getting_started/quick_start.html) from Reddit.
2. Setup a [service account](https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account)
to use Google Sheets as a DB.
3. Download the service account JSON from the step above and add it to your repo.
Use the screenshot below for reference.

At the end of all the setup, the credentials file should look like this:
![credentials](https://i.imgur.com/mx7yeHX.jpg)

#### Support modules
Install requirements by running:
```bash
pip install -r requirements.txt
```
You'll also need `nltk`, used to generate captions.
Run the following (one-time effort) from a Python3 shell.

```python
import nltk
nltk.download("punkt")
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
```

#### How to run the entire thing:
```bash
cd insta_reddit/code
python download_from_reddit.py
python draw_text_on_image.py
python upload_to_instagram.py

```
Or run the modifiable Cron job (remember to change the venv path):
```bash
sh run_all_jobs.sh
```
Or add the above to your crontab to run at your set frequency:
```bash
crontab -e
```
Add this line your crontab: `@daily /path/to/run_all_jobs.sh`


#### End result on [Instagram](https://www.instagram.com/unethical.lifeprotips/):
![feed](https://i.imgur.com/9MmYy81.jpg)

Sample post:
![sample_post](https://i.imgur.com/1czZFFK.jpg)


## Contributing
Pull requests are welcome! 
For major changes, please open an issue first to discuss what you would like to change.

## Author
* **Surya Shekhar Chakraborty**

Much thanks to Avishek Rakshit for help with the graphic design, Puneet Jindal for brainstorming, and to you for coming here. :)

## License
This project is licensed under the MIT License - 
see the [LICENSE](https://github.com/suryashekharc/insta_reddit/blob/master/LICENSE) file for details
