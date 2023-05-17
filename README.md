# linkedinscraper
Create a scraperconfig.py , add email, password and search term as follows:

``linkedin_username = "<email>"

linkedin_password = "<pass>"

searchterm = "defender of the realm"``
  
Sometimes LinkedIn is flaky:

The format of the position changes for some people and their data is is Current: or Past: - just look for the position in the regular area, if not found, move to the next result.

Sometimes LinkedIn will return several pages and then say there are no more results. The program will just move to the next page.

Because of the above issues, you won't get all records - probably about 70%.

The program is slow - I added lots of delays, some of them random, to appear a bit more human. LinkedIn WILL start doing captchas if it suspects a bot/scraper and this will crash the program.
