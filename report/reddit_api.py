from .core import CLIENT_ID, CLIENT_SECRET, PASSWORD, USER_AGENT, USERNAME, REDDIT_HEADERS
from .core import csv, Queue, string, random, time_tracker, Thread
from .core import Reddit, DATAPATH, os, sys
from .core import Pie, StackedBars, Bars, MultiColumnedBars


class RedditStreamer:

    def __init__(self, from_main_q, to_main_q, max_wait=5, mode='submissions', data=None, project=""):

        self.api = Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                             password=PASSWORD, user_agent=USER_AGENT,
                             username=USERNAME)

        self.from_main_q = from_main_q
        self.to_main_q = to_main_q
        self.user = USERNAME
        self.max_wait = max_wait
        self.project = project
        letters = string.ascii_lowercase
        self.filename = ''.join(random.choice(letters) for i in range(5))
        self.headers = []

        if data is not None:
            for header in data:
                if header in REDDIT_HEADERS[mode] and header not in self.headers:
                    self.headers.append(header)


    def stream_data(self):
        def check_if_streaming():
            while self.from_main_q.qsize():
                try:
                    info = self.from_main_q.get(0)
                    try:
                        if info['stop']:
                            f.close()
                            sys.exit(0)
                    except KeyError:
                        pass
                except:
                    pass

        def process_submission(submission):
            info = {}
            for header in self.headers:
                if hasattr(submission, header):
                    info[header] = getattr(submission, header)
                else:
                    info[header] = 'n/a'
            return {'item': info}

        # since generator has counter delays, we need timer to keep constant "ticks" & updates to main process
        to_thread_q = Queue()
        timer = Thread(target=time_tracker, args=(self.max_wait, to_thread_q, self.to_main_q))
        timer.daemon = True
        timer.start()

        for streamed, submission in enumerate(self.api.redditor(self.user).stream.submissions()):
            try:
                check_if_streaming()
            except:
                pass
            to_thread_q.put({'new_stream': True})
            if self.project in submission.title:
                info = process_submission(submission)
                self.to_main_q.put(info)


class CommunityFocus(Pie):
    """
    Pie chart divided by submissions per community (%)
    """
    def __init__(self, data, name="Community Focus (All Submissions)"):
        # get relevant data for model
        subreddits = {}
        total = 0
        for item in data:
            srname = item['subreddit'].display_name
            if srname not in list(subreddits):
                subreddits[srname] = 1
            else:
                subreddits[srname] += 1
            total += 1

        info = {}
        for subreddit, submits in subreddits.items():
            info[subreddit] = submits / total


        Pie.__init__(self, info, title=name)


class UpvotesPerLink(StackedBars):
    def __init__(self, data, name="Upvotes per submission"):
        # get relevant data for model
        links = []
        subreddits = {}

        yt_indicator = 'yout'
        #tekk: [0,1,50...],

        for item in data:
            link = item['url']
            if link not in links and yt_indicator in link:
                links.append(link)

        for item in data:

            srname = item['subreddit'].display_name
            link = item['url']

            if srname not in list(subreddits):
                subreddits[srname] = [0 * i for i in range(len(list(links)))]

            try:
                ind = links.index(link)
                subreddits[srname][ind] += item['score']
            except:
                pass

        StackedBars.__init__(self, subreddits, xaxis_labels=links, title=name)


class ScoreCommentsPerSubmit(MultiColumnedBars):
    def __init__(self, data, name="Score+Comments per submission"):
        # get relevant data for model
        info = []
        for item in data:
            info.append([item['score'], item['num_comments']])

        MultiColumnedBars.__init__(self, info, ['score', 'num_comments'], title=name)



class CommentsPerSubmit(Bars):
    def __init__(self, data, name="Comments per submission"):
        # get relevant data for model
        comments = []
        for item in data:
            comments.append(item['num_comments'])

        Bars.__init__(self, comments, title=name)


class ScorePerSubmit(Bars):
    def __init__(self, data, name="Score per submission"):
        # get relevant data for model
        scores = []
        for item in data:
            scores.append(item['score'])

        Bars.__init__(self, scores, title=name)

class UpvoteRatioPerSubmit(Bars):
    def __init__(self, data, name="Upvote % per submission"):
        # get relevant data for model
        ratios = []
        for item in data:
            ratios.append(item['upvote_ratio'])

        Bars.__init__(self, ratios, title=name)






#  {"Community Focus (All Submissions)": {'object': CommunityFocus, 'required_data': ['subreddit', 'upvote_ratio', 'score', 'url']},
                            # 'Upvotes Per Link': {'object': UpvotesPerLink, 'required_data': ['subreddit', 'url', 'score']},
REDDIT_MODELS = {'submissions': {'Comments Per Submission': {'object': CommentsPerSubmit, 'required_data': ['num_comments', 'url']},
                        'Score Per Submission': {'object': ScorePerSubmit, 'required_data': ['score', 'url']},
                        'Upvote % per submission': {'object': UpvoteRatioPerSubmit, 'required_data': ['upvote_ratio', 'url']},
                        'Score+Comments per submission': {'object': ScoreCommentsPerSubmit, 'required_data': ['score', 'num_comments', 'url']}}}
