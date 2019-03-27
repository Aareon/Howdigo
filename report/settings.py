from .core import os, ConfigParser

WELCOME_MSG = "Build a report to show off to your potential employers."
APIs = ["Reddit"] #"Github",
DATAPATH = r'{}\Howdigo'.format(os.environ['APPDATA'])

if not os.path.exists(DATAPATH):
    os.makedirs(DATAPATH)

# Read app.ini
parser = ConfigParser()

parser.read('.\\report\\api.ini')
# parser.read('.\\report\\realjohnward\\api.ini')

# reddit settings
r = 'Reddit'
CLIENT_ID = parser.get(r, 'ClientID')
PASSWORD = parser.get(r,'Password')
CLIENT_SECRET = parser.get(r, 'ClientSecret')
USERNAME= parser.get(r,'Username')
USER_AGENT = parser.get(r, 'Useragent')


REDDIT_HEADERS = {'submissions': ['author', 'clicked', 'comments', 'created_utc', 'distinguished', 'edited', 'id', 'is_self', 'link_flair_template_id',
                            'link_flair_text', 'locked', 'name', 'num_comments', 'over_18', 'permalink', 'score', 'selftext', 'spoiler', 'stickied', 'subreddit',
                            'title', 'upvote_ratio', 'url']}

GITHUB_HEADERS = {'repository': ['unique_views', 'total_views', 'unique_clones', 'total_clones', 'referrer', 'clone_timestamp']}


# HEADERS = {'reddit': REDDIT_HEADERS, 'github': GITHUB_HEADERS}


# github settings
gh = 'Github'
GB_USERNAME = parser.get(gh, 'Username')
GB_PASSWORD = parser.get(gh, 'Password')
