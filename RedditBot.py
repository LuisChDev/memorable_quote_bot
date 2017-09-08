import praw, json, re, time, sqlite3, yaml
from PIL import Image
from ImageScript import build_image, delete_image
from Utils import remove_from_list, add_to_list, get_list

# 0. register

reddit = praw.Reddit('memorable_quote_bot')

# step 1: write the regex.

MEMORABLE_QUOTE_REGEX = '^"[^"]{50,140}\S"$'
source = 'https://github.com/Luischv/memorable_quote_bot'
start = 'start'
stop = 'stop'
blacklisted_users = 'blacklist.txt'
banned_subreddits = 'banned_subreddits.txt'
message_file = 'message_file.txt'
comment_file = 'comment_file.txt'
msg_header = 'dear mr. memorable_quote_bot...'
bot_username = 'memorable_quote_bot'
delete_threshold = -2

startauto = "https://reddit.com/message/compose?to="+bot_username+"&message="+start+"&subject="+msg_header
stopauto = "https://reddit.com/message/compose?to="+bot_username+"&message="+stop+"&subject="+msg_header
PMme = "https://reddit.com/message/compose?to=positronic_nightmare"

already_stopped = 'I abstain from answering you already. If you want me to respond to your comments again, message me "'+start+'". (Without the quotes.)'
stopped = 'Done. I\'ll abstain from responding to your comments from now on. If you ever want me to start again, message me "'+start+'". (Without the quotes.)'
started = 'Okay. I\'ll start responding to your comments again. Remember you can always have me stop by messaging me "'+stop+'". (Without the quotes.)'

def main():
     with open(comment_file) as temp:
          cached_comments = yaml.load(temp).keys()
     number_comments = 0
     banned = get_list(banned_subreddits)
     check_inbox()
     delete_if_downvoted()
     for comment in reddit.subreddit('test').comments(limit=100):
          regex = re.search(MEMORABLE_QUOTE_REGEX, comment.body)
          allowed = (comment.subreddit.display_name not in banned)
          if regex and allowed and (comment.id not in cached_comments):
               number_comments = number_comments + 1
               image = build_image(regex.group(0), comment.id)
               add_to_list(comment_file, yaml.dump({comment.id: image},
                                                   default_flow_style=False))
               comment.reply(make_comment(image))
               print(regex.group(0)+'\n'+'-_-_-'+
                     comment.subreddit.display_name+'\n'+
                     comment.permalink()+'\n')
     print('next')

def make_comment(image_link):
     """
     writes a comment ready to be sent.
     """
     return(image_link+"\n\n_I am a bot._^bleep ^^bloop - [stop]("+stopauto+") | [start]("+startauto+") | [source]("+source+") | [PM me!]("+PMme+")")

# check inbox to block and unblock on demand.
# message 'stop' to not reply to your comment, 'start' to begin again.

def check_inbox():
     for msg in reddit.inbox.messages(limit=100):
          message_list = get_list(message_file)
          blacklist = get_list(blacklisted_users)
          if msg.id not in message_list:
               print(msg.body+' not in list')
               add_to_list(message_file, msg.id)
               if msg.author.name in blacklist:
                   if msg.body == start:
                        remove_from_list(blacklisted_users, msg.author.name)
                        msg.reply(started)
                   elif msg.body == stop:
                        msg.reply(already_stopped)
               else:
                   if msg.body == start:
                        msg.reply(started)
                   elif msg.body == stop:
                        add_to_list(blacklisted_users, msg.author.name)
                        msg.reply(stopped)

def delete_if_downvoted():
     """
     auto delete the comment and image if downvoted
     """
     for comment in reddit.redditor(bot_username).comments.controversial('all', limit=None):
          if comment.score <= delete_threshold:
               with open(comment_file) as comments:
                    dicc = yaml.load(comments)
               delete_image(dicc[comment.parent().id])
               comment.delete()

if __name__ == '__main__':
     beginning = time.time()
     now = beginning
     
     for i in range(0, 100): # while True:
          try:
               main()
          except Exception as e:
               if e == praw.exceptions.APIException:
                    print('ups, exceeded the limit. 100 sec. sleep')
                    time.sleep(100)
               else:
                    print(str(e))
          time.sleep(2)
          if (time.time() - now) >= 3600:
               now = time.time()
               delete_if_downvoted()
     end = time.time()
     print('\n\n')
     print(end - beginning)
     print('\n')
     print(str(number_comments))
