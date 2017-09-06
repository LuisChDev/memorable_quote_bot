import praw, json, re, time, sqlite3
from PIL import Image
from ImagingPart import build_image

# 0. register

reddit = praw.Reddit('memorable_quote_bot')

# step 1: write the regex.

MEMORABLE_QUOTE_REGEX = '^"[^"]{50,140}\S"$'
start = 'start'
stop = 'stop'
blacklisted_users = 'blacklist.txt'

already_stopped = 'I abstain from answering you already. If you want me to respond to your comments again, message me "'+start+'".(Without the quotes.)'
stopped = 'Done. I\'ll abstain from responding to your comments from now on. If you ever want me to start again, message me "'+start+'".(Without the quotes.)'
started = 'Okay. I\'ll start responding to your comments again.'

cached_comments = [None]*20
cached_messages = []
number_comments = 0

print(reddit.read_only)
beginning = time.time()
with open("banned_subreddits.txt") as banned_subreddits:
     banned = banned_subreddits.read().split('\n')
     for j in range(0, 100):
          for comment in reddit.subreddit('test').comments(limit=100):
               regex = re.search(MEMORABLE_QUOTE_REGEX, comment.body)
               allowed = (comment.subreddit.display_name not in banned)
               if regex and allowed and (comment.id not in cached_comments):
                    cached_comments[j % 20] = comment.id
                    number_comments = number_comments + 1
                    image = build_image(regex.group(0), comment.id)
                    comment.reply(''+image)
                    print(regex.group(0)+'\n'+'-_-_-'+
                          comment.subreddit.display_name+'\n'+
                          comment.permalink()+'\n')

          time.sleep(2)
          print(j)

end = time.time()
print('\n'+str(number_comments))
print(' ')
print(end - beginning)

# check inbox to block and unblock on demand.
# message 'stop' to not reply to your comment, 'start' to begin again.
# I will always respond on direct command, though.
# def checkInbox():
#      for msg in reddit.inbox.messages(limit=100):
#           if msg not in cached_messages:
# will do this later

# Generate the comment for
# def
# later
