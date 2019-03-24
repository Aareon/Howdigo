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


class Report:
    def __init__(self):
        self.total_submissions = 0
        self.total_comments = 0
        self.total_score = 0
        self.total_upvote_ratio = 0
        self.avg_upvote_ratio = 0
        self.total_viewers = 0
        self.subreddit_viewers = {}


    def compile_report(self):
        self.avg_upvote_ratio = self.total_upvote_ratio / self.total_submissions
        for subreddit, viewers in self.subreddit_viewers.items():
            self.total_viewers += viewers

    def print_report(self):
        print(f"Total Comments: {self.total_comments}")
        print(f"Total Score: {self.total_score}")
        print(f"Total Submissions: {self.total_submissions}")
        print(f"Total Viewer counts in Subreddits : {self.subreddit_viewers}")
        print(f"Total Viewers: {self.total_viewers}")
        print(f"Avg Upvote Ratio: {self.avg_upvote_ratio}")


def set_total_score(user, report):
    total_score = 0
    for submission in reddit.redditor(user).stream.submissions():
        report.total_score += submission.score


def stream_submissions(user, report):
    total_approval = 0
    for streamed, submission in enumerate(reddit.redditor(user).stream.submissions()):
        report.total_upvote_ratio += submission.upvote_ratio
        report.total_score += submission.score
        report.total_comments += submission.num_comments
        report.total_submissions += 1

        sr_name = submission.subreddit.name
        sr_subs = submission.subreddit.subscribers
        if sr_name not in list(report.subreddit_viewers):
            report.subreddit_viewers[sr_name] = sr_subs
        else:
            report.subreddit_viewers[sr_name] += sr_subs

        print("streamed: ", submission.permalink)


if __name__ == '__main__':
    book = Report()
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
