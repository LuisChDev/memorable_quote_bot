import praw
import re
import time
from random import random
from ImageScript import build_image, delete_image
from config import MEMORABLE_QUOTE_REGEX, source, start, stop
from config import bot_username, delete_threshold, already_stopped, stopped
from config import started, stopauto, startauto, PMme, numfigs
from database import Comment, Bannedsub, Banneduser, Message, Historicalfigure
from database import db
from pony.orm import db_session, select, delete

# connect to the database
db.bind(provider='sqlite', filename='database.db')
db.generate_mapping(create_tables=False)

# connect to the account
reddit = praw.Reddit('memorable_quote_bot')


# open a single database session
@db_session
def main():
    number_comments = 0
    # tm = time.time()
    check_inbox()
    # tm2 = time.time()
    # print(tm2 - tm)
    delete_if_downvoted()

    # tm3 = time.time()
    # print(tm3 - tm2)
    comments = reddit.subreddit('test').comments(limit=100)
    # tm4 = time.time()
    # print(tm4 - tm3)

    for comment in comments:
        regex = re.search(MEMORABLE_QUOTE_REGEX, comment.body)
        subname = comment.subreddit.display_name
        # with db_session:
        allowed = not select(
            b for b in Bannedsub if b.name == subname)[:]
        fresh = not select(
            c for c in Comment if c.id == comment.id)[:]

        if regex and allowed and fresh:
            # select a random person from db and create image
            person = select(x.name for x in Historicalfigure)[:][
                int(random()*numfigs)]
            number_comments = number_comments + 1
            image = build_image(regex.group(0), comment.id, person)
            # with db_session:
            Comment(id=comment.id, url=image)
            comment.reply(make_comment(image))

            print(
                regex.group(0) + '\n' + '-_-_-' +
                comment.subreddit.display_name + '\n' + comment.permalink +
                '\n')
    print('NEXT')


def make_comment(image_link):
    """
     writes a comment ready to be sent.
     """
    return ''.join([
        image_link, "\n\n _I am a bot._ ^bleep ^^bloop - [stop](", stopauto,
        ") | [start](", startauto, ") | [source](", source, ") | [PM me!](",
        PMme, ")"
    ])


# check inbox to block and unblock on demand.
# message 'stop' to not reply to your comment, 'start' to begin again.


def check_inbox():
    # with db_session:
    msg_list = select(m.id for m in Message)[:20]
    blacklist = select(b.name for b in Banneduser)[:20]
    msgs = reddit.inbox.messages(limit=100)
    for msg in msgs:
        # message_list = get_list(message_file)
        # blacklist = get_list(blacklisted_users)
        # if msg.id not in message_list:
        if msg.id not in msg_list:
            print(msg.body + ' not in list')
            # add_to_list(message_file, msg.id)
            # with db_session:
            Message(id=msg.id)
            # if msg.author.name in blacklist:
            if msg.author.name in blacklist:
                if msg.body == start:
                    # remove_from_list(blacklisted_users, msg.author.name)
                    # with db_session:
                    delete(m for m in Message if m.id == msg.id)
                    msg.reply(started)
                elif msg.body == stop:
                    msg.reply(already_stopped)
            else:
                if msg.body == start:
                    msg.reply(started)
                elif msg.body == stop:
                    # add_to_list(blacklisted_users, msg.author.name)
                    # with db_session:
                    Banneduser(name=msg.author.name)
                    msg.reply(stopped)


def delete_if_downvoted():
    """
     auto delete the comment and image if downvoted
     """
    for comment in reddit.redditor(bot_username).comments.controversial(
            'all', limit=None):
        if comment.score <= delete_threshold:
            # with open(comment_file) as comments:
            #     dicc = yaml.load(comments)
            # with db_session:
            link = (
                c.url for c in Comment if c.id == comment.parent().id)[0]
            # delete_image(dicc[comment.parent().id])
            delete_image(link)
            comment.delete()


def root():
    beginning = time.time()
    now = beginning

    for i in range(0, 10):  # while True:
        try:
            main()
        except Exception as e:
            if e == praw.exceptions.APIException:
                print('oops, exceeded the limit. 100 sec. sleep')
                time.sleep(100)
            else:
                print(str(e))
        time.sleep(2)
        if (time.time() - now) >= 3600:
            now = time.time()
            # delete_if_downvoted()
    end = time.time()
    print('\n\n')
    print(end - beginning)
    print('\n')


if __name__ == '__main__':
    root()
