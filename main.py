from report import Howdigo, BackgroundWorker, freeze_support, sys

if __name__ == '__main__':
    freeze_support()

    root = Howdigo()

    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))

    root_worker_q = root.to_stream_q
    worker_root_q = root.from_stream_q

    worker = BackgroundWorker(root_worker_q, worker_root_q)
    worker.daemon = True
    worker.start()

    root.mainloop()
