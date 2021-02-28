from googlesearch import search
from bs4 import BeautifulSoup
import requests
import praw
import time

# Two variables--one to hold website credentials and another to hold website access

creds = {"client_id": "xxxxxxxxxxxxxxxxx",
         "client_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
         "password": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
         "user_agent": "movie guide demo created by /u/IMDBInfo version: 0.2",
         "username": "IMDBInfo"}

reddit = praw.Reddit(client_id=creds["client_id"],
                     client_secret=creds["client_secret"],
                     password=creds["password"],
                     user_agent=creds["user_agent"],
                     username=creds["username"])

# Make a variable to keep track of comments made

replies = 0

# Make a list called submissions to store the top 3 new submissions from movie group

while True:

    # Get the top 5 new submissions from various movie groups

    subreddits = []
    subreddits.append("xxxxxxxxxx")
    subreddits.append("xxxxxxxxxxxxxxxx")
    subreddits.append("xxxxxxxxxxxxxxxx")
    subreddits.append("xxxxxxxxxxxx")
    subreddits.append("xxxxxxxxxx")
    subreddits.append("xxxxxxxxxx")
    subreddits.append("xxxxxxxxxxxxx")
    subreddits.append("xxxxxxxxxx")
    submissions = []
    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).__getattribute__("new")(limit=3):
            submissions.append(submission)

    for submission in submissions:

        # Reset the variables

        query = title = genre = summary = director = stars = popularity = age_rating = link = " "

        # Change the submission title into a query

        query = submission.title
        query = query.split(")")
        query = query[0] + (") + imdb")
        if "&" in submission.title:
            query = submission.title.replace("&", "")

        # Search google and refine results to get the imdb url

        search_results = search(query, 5, 'en')
        for search_result in search_results:
            if "https://www.imdb.com/title/tt" in search_result:
                link = str(search_result)
                if len(search_result) == 37:
                    break

        # Attempt to get the title, genre, and summary from the link

        try:
            source = requests.get(link).text
            soup = BeautifulSoup(source, 'lxml')

            imdb_info = soup.find("div", class_="title_wrapper")
            imdb_info = imdb_info.text
            imdb_info = imdb_info.strip()

            imdb_info = imdb_info.split("|")
            imdb_info = imdb_info[0].replace("\n", "")

            title = imdb_info.split(")")
            title = title[0].replace("\n", "")
            title = "**" + title + ")**  "
            title = title.replace("  ", "") + "  "

            genre1 = soup.find("div", class_="title_wrapper")
            genre1 = genre1.text
            genre1 = genre1.strip()
            genre1 = genre1.replace("  ", "")
            genre1 = genre1.replace("\n", "")
            genre1 = genre1.split("|")
            genre1 = genre1[2]
            genre1 = genre1.replace(", ", " | ") + "  "

            genre2 = soup.find("div", class_="subtext")
            genre2 = genre2.text
            genre2 = str(genre2)
            genre2 = genre2.split("|")
            genre2 = genre2[1]
            genre2 = genre2.replace("\n", "")
            genre2 = genre2.replace(", ", " | ")
            genre2 = genre2.strip() + "  "

            genre = genre1
            catch_words = ["Episode", "TV", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
            if any(x in genre for x in catch_words):
                genre = genre2

            summary = soup.find("div", class_="summary_text")
            summary = summary.text
            summary = summary.strip()
            summary = summary + "  "
            summary = summary.replace("  ", "")
            summary = summary.replace("See full summary »", "")
            summary = summary.replace("\n", "") + "  "

        except:
            print(" ")

        # Attempt to get the director, stars, popularity, and age rating from the link

        try:
            chunk = soup.text.replace("\n", "")
            director = chunk.split("Director:")
            director = director[1].split(" Writer")
            director = "By " + director[0] + "  "
            if len(director) > 100:
                director = " "
            stars = chunk.split("Stars:")
            stars = stars[1].split(" |")
            stars = stars[0].split("  ")
            stars = "Stars " + stars[0] + "  "

            popularity = chunk.split("Soundtracks")
            popularity = popularity[1]
            popularity = popularity.split(" user")
            popularity = popularity[0].strip() + " user ratings  "
            popularity = popularity.split("10")
            popularity = popularity[0] + "10  "
            if len(popularity) > 10:
                popularity = " "
            age_rating = imdb_info.replace("  ", "")
            age_rating = age_rating.split(") ")
            age_rating = age_rating[1] + "  "

        except:
            print(" ")
            director = stars = popularity = age_rating = " "

        try:

            # Prepare an entry for a comment reply

            if len(title) > 1:
                title = title + "\n"
            if len(genre) > 1:
                genre = genre + "\n"
            if len(summary) > 1:
                summary = summary + "\n"
            if len(director) > 1:
                director = director + "\n"
            if len(stars) > 1:
                stars = stars + "\n"
            if len(popularity) > 1:
                popularity = popularity + "\n"
            if len(age_rating) > 1:
                age_rating = age_rating + "\n"
            if len(link) > 1:
                link = link + "\n"

            entry = title + genre + summary + director + stars + popularity + age_rating + link

            # Make a comment if it has't commented yet

            task_complete = False
            for comment in submission.comments:
                if comment.author == "IMDbInfo":
                    task_complete = True
                    break
                  
            # Just take a two second break
         
            time.sleep(2)
                  
            # Submit a reply to the submission and print the reply in the output

            if not task_complete:
                submission.reply(entry)
                replies = replies + 1
                print("I just made a comment. Total: " + str(replies) + "\n")
                time.sleep(3)
                print(entry)
                print()
                  
        except:
            print("")

    # Sleep for 15 minutes to avoid spamming

    time.sleep(900)
