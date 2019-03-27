from .core import os, ConfigParser

WELCOME_MSG = "Build a report to show off to your potential employers."
APIs = ["Reddit"] #"Github",
DATAPATH = r'{}\Howdigo'.format(os.environ['APPDATA'])

if not os.path.exists(DATAPATH):
    os.makedirs(DATAPATH)

# Read app.ini
parser = ConfigParser()

try:
    parser.read('.\\report\\api.ini')
    _ = parser.get('Reddit', 'ClientID')
except:
    parser.read('.\\report\\realjohnward\\api.ini')

# reddit settings
r = 'Reddit'
CLIENT_ID = parser.get(r, 'ClientID')
PASSWORD = parser.get(r,'Password')
CLIENT_SECRET = parser.get(r, 'ClientSecret')
USERNAME= parser.get(r,'Username')
USER_AGENT = parser.get(r, 'Useragent')

# CLIENT_ID = "QLRAtXHUzbV4Xw"
# PASSWORD = "Jw052796rt"
# CLIENT_SECRET = "HllAPy3SokVnWlMq0Re28t6mu34"
# USERNAME= "realjohnward"
# USER_AGENT = "praw"
REDDIT_HEADERS = {'submissions': ['author', 'clicked', 'comments', 'created_utc', 'distinguished', 'edited', 'id', 'is_self', 'link_flair_template_id',
                            'link_flair_text', 'locked', 'name', 'num_comments', 'over_18', 'permalink', 'score', 'selftext', 'spoiler', 'stickied', 'subreddit',
                            'title', 'upvote_ratio', 'url']}

GITHUB_HEADERS = {'repository': ['unique_views', 'total_views', 'unique_clones', 'total_clones', 'referrer', 'clone_timestamp']}


# HEADERS = {'reddit': REDDIT_HEADERS, 'github': GITHUB_HEADERS}


# github settings
gbcfg = parser['Github']
GB_USERNAME = gbcfg['Username']
GB_PASSWORD = gbcfg['Password']
