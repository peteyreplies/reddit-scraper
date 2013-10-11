# pull a list of the top 25 submissions in r/pics
import praw
import json
from pprint import pprint
import sqlite3
import top_redditdb

#set user agent to identify to reddit
my_user_agent = ("tracking top submissions to /r/pics by /u/peteyMIT - email petey [at] mit [dot] edu")

#login to reddit 
r = praw.Reddit(user_agent=my_user_agent)
r.login('peteybot','beepboopboopreddit')

#create a top submissions bin
top_submissions_generator = r.get_subreddit('pics').get_top(limit=25)

#connect to & prep database 
top_redditdb.connect()

for submission in top_submissions_generator:
	
	#store attributes of each submission in a dictionary 
	info = {
		'author_name': submission.author.name,
		'created_time': submission.created_utc,
		'reddit_id': submission.id,
		#'downvotes': submission.downs,
		#'upvotes': submission.ups,
		#'comment_count': submission.num_comments,
		#'score': submission.score,
		'title': submission.title,
		'submitted_url': submission.url,
		'domain': submission.domain,
		'reddit_shortlink': submission.short_link,
		'imgur': None
		}

	#parse imgur ids to catch direct links 
	if "http://i.imgur.com" in submission.url:
		this_url = submission.url[19:]
		imgur_id = this_url[:-4]
		info['imgur'] = imgur_id
	if "http://imgur.com/" in submission.url:
		if "/a/" in submission.url:
			imgur_id = submission.url[19:]
			info['imgur'] = imgur_id
		else:
			imgur_id = submission.url[17:]
			info['imgur'] = imgur_id

	#write to database
	top_redditdb.insert(info) 
	
top_redditdb.close()
