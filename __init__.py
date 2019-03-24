import praw
from praw.models.user import User
import sys
import os

CLIENT_ID = "QLRAtXHUzbV4Xw"
PASSWORD = "Jw052796rt"
CLIENT_SECRET = "HllAPy3SokVnWlMq0Re28t6mu34"
USERNAME= "realjohnward"
USER_AGENT = "praw"
ABOUT_URL = "https://realjohnward.com"
REDIRECT_URL = "https://realjohnward.com"


reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                     password=PASSWORD, user_agent=USER_AGENT,
                     username=USERNAME)


class StatBook:
    def __init__(self):
        self.total_submissions = 0
        self.total_comments = 0
        self.total_score = 0
        self.total_upvote_ratio = 0
        self.avg_upvote_ratio = 0
        self.community_data = {}

    def compile_report(self):
        self.avg_upvote_ratio = self.total_upvote_ratio / self.total_submissions


    def print_report(self):
        print(f"Total Comments: {self.total_comments}")
        print(f"Total Score: {self.total_score}")
        print(f"Total Upvote Ratio: {self.total_upvote_ratio}")
        print(f"Total Submissions: {self.total_submissions}")
        print(f"Avg Upvote Ratio: {self.avg_upvote_ratio}")


def set_total_score(user, statbook):
    total_score = 0
    for submission in reddit.redditor(user).stream.submissions():
        statbook.total_score += submission.score


def stream_submissions(user, statbook):
    total_approval = 0
    for streamed, submission in enumerate(reddit.redditor(user).stream.submissions()):
        statbook.total_upvote_ratio += submission.upvote_ratio
        statbook.total_score += submission.score
        statbook.total_comments += submission.num_comments
        statbook.total_submissions += 1
        print("streamed: ", submission.permalink)


if __name__ == '__main__':
    book = StatBook()
    try:
        stream_submissions(USERNAME, book)
    except KeyboardInterrupt:
        print('Interrupted')
        book.compile_report()
        book.print_report()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
