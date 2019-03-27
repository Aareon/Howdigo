from .core import Process, RedditStreamer, time   #,GithubStreamer

class BackgroundWorker(Process):
    def __init__(self, from_main_q, to_main_q):
        Process.__init__(self, target=self.mainloop)

        self.from_main_q = from_main_q
        self.to_main_q = to_main_q


    def mainloop(self):
        while True:
            self.update()
            time.sleep(0.01)

    def update(self):
        while self.from_main_q.qsize():
            try:
                info = self.from_main_q.get(0)
                if info['api'] == 'reddit':
                    self.streamer = RedditStreamer(self.from_main_q, self.to_main_q, mode=info['mode'], data=info['data'], project=info['project'])
                    self.streamer.stream_data()
                # elif info['api'] == 'github':
                    # self.streamer = GithubStreamer(self.from_main_q, self.to_main_q, mode=info['mode'], data=info['data'], project=info['project'])
                    # self.streamer.stream_data()
                else:
                    self.to_main_q.put({'error': 'No streamer object exists for the api "{}"'.format(info['api'])})

            except Exception as e:
                self.to_main_q.put({'error': e})
