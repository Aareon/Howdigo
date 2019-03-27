from .core import Github, GB_USERNAME, GB_PASSWORD, GITHUB_HEADERS
from .core import csv, Queue, string, random, time, MultiColumnedBars


class GithubStreamer:
    def __init__(self, from_main_q, to_main_q, max_wait=5, mode='repository', data=None, project=""):
        gb = Github(GB_USERNAME, GB_PASSWORD)
        self.api = gb.get_user()

        self.from_main_q = from_main_q
        self.to_main_q = to_main_q
        self.user = GB_USERNAME
        self.max_wait = max_wait
        self.project = project
        letters = string.ascii_lowercase
        self.filename = ''.join(random.choice(letters) for i in range(5))
        self.headers = []


    def stream_data(self):
        # on_models = []
        # for model in self.models:
        #     on_models.append(model(self.api, self.project))
        time.sleep(1)
        self.to_main_q.put({'github-data': {'user': self.api, 'repo': self.project}})



class ViewsPerDay(MultiColumnedBars):
    def __init__(self, data, name="Views per day"):
        user = data['user']
        repo = data['repo']

        r = user.get_repo(repo)
        self.data = r.get_views_traffic(per='day')
        print("data: ", self.data)
        # get relevant data for model
        info = []
        for item in self.data:
            info.append([item['count'], item['uniques']])

        MultiColumnedBars.__init__(self, info, ['total_views', 'unique_views'], title=name)


class ClonesPerDay(MultiColumnedBars):
    def __init__(self, data, name="Views per day"):
        user = data['user']
        repo = data['repo']

        r = user.get_repo(repo)
        self.data = r.get_clones_traffic(per='day')

        print("data: ", self.data)
        # get relevant data for model
        # info = []
        # for item in self.data:
            # info.append([item['count'], item['uniques']])

        # MultiColumnedBars.__init__(self, info, ['total_clones', 'unique_clones'], title=name)




GITHUB_MODELS = {'repository': {"Views per day": {'object': ViewsPerDay, 'required_data': ['total_views', 'unique_views', 'referrer']},
                            'Clones per day': {'object': ClonesPerDay, 'required_data': ['total_clones', 'unique_clones', 'clone_timestamp']}}}
