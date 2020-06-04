import gspread

gc = gspread.service_account("/Users/suryasekharchakraborty/Documents/insta_reddit/"
                             "insta_reddit/google_credentials.json")

sh = gc.open("ULPT_database")  # Steps to connect to Sheets:

print(sh.sheet1.get('A1'))
