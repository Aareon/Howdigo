from .core import tk, ttk, messagebox, Queue, WELCOME_MSG, APIs
from .core import RedditStreamer #GithubStreamer
from .core import REDDIT_MODELS, Report, sys #, GITHUB_MODELS

MODELS = {'reddit': REDDIT_MODELS} #, 'github': GITHUB_MODELS}

class Howdigo(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("500x300")

        self.wm_title("Howdigo Report Builder")
        self.mm = MainMenu(self)
        self.mm.pack(fill="both", expand=1)

        self.to_stream_q = Queue()
        self.from_stream_q = Queue()

class MainMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # welcomelab = tk.Label(self, text=WELCOME_MSG)
        # welcomelab.pack(side="top")
        self.step = -1
        self.choice_funcs = [self.choice_1, self.choice_2, self.choice_3]
        self.cfg = {'step1': {}, 'step2': {}, 'step3': {}}
        self.navbar()

    def restart(self):
        self.step = -1
        self.prevbtn.config(text="Back", command=self.prev_choice, width=10, state='disabled')
        self.nextbtn.config(text="Next", command=self.next_choice)
        self.next_choice(restart=True)

    def next_choice(self, event=None, restart=False):
        self.step += 1
        self.choice_funcs[self.step](restart=restart)
        self.prevbtn.config(state='normal')
    def prev_choice(self, event=None):
        self.step -= 1
        self.choice_funcs[self.step](back=True)
        self.nextbtn.config(state='normal', text='Next')
        if self.step == 0:
            self.prevbtn.config(state='disabled')

    def navbar(self):
        nbframe = tk.Frame(self)
        nbframe.pack(side="bottom", fill="x")

        self.nextbtn = ttk.Button(nbframe, text="Next", state='disabled', command=self.next_choice)
        self.nextbtn.pack(side="right", padx=5, pady=5)

        self.prevbtn = ttk.Button(nbframe, text="Back", state='disabled', command=self.prev_choice)
        self.prevbtn.pack(side="left", padx=5, pady=5)

        self.next_choice()

    def choice_1(self, back=False, restart=False):

        if back or restart:
            self.cframe.destroy()
            choice = self.cfg['step1']['choice']
        else:
            choice = None

        self.cframe = tk.Frame(self)
        self.cframe.pack(side="top", fill="x")
        choicelab = tk.Label(self.cframe, text="Choose what API to stream from.")
        choicelab.pack(side="top")
        answerframe = tk.Frame(self.cframe)
        answerframe.pack(side="bottom", fill="x")
        self.nextbtn.config(state='disabled')
        self.choice = tk.StringVar(value=choice)
        cbox = ttk.Combobox(answerframe, values=APIs, textvariable=self.choice)
        cbox.bind("<<ComboboxSelected>>", self.choice_1_selected)
        cbox.pack(padx=10, pady=10)

    def choice_1_selected(self, event):
        self.cfg['step1']['choice'] = self.choice.get()
        self.nextbtn.config(state='normal')

    def choice_2(self, back=False, restart=False):
        def options():
            cbox = ttk.Combobox(answerframe, values=list(MODELS[api]), textvariable=self.choice)
            cbox.bind("<<ComboboxSelected>>", self.choice_2_selected)
            cbox.pack(padx=10, pady=10)




        api = self.cfg['step1']['choice'].lower()

        self.cframe.destroy()

        if back:
            self.choice.set(self.cfg['step2']['choice'])
        else:
            self.choice.set(None)


        self.cframe = tk.Frame(self)
        self.cframe.pack(side="top", fill="x")
        choicelab = tk.Label(self.cframe, text=f"What are you streaming from {api}?")
        self.nextbtn.config(state='disabled')
        choicelab.pack(side="top")
        answerframe = tk.Frame(self.cframe)
        answerframe.pack(side="bottom", fill="x")
        options()



    def choice_2_selected(self, event):
        self.nextbtn.config(state='normal')


    def choice_3(self, back=False, restart=False):
        self.cframe.destroy()
        def options():
            models = MODELS[api][stream_mode]
            self.listbox = tk.Listbox(answerframe, selectmode=tk.MULTIPLE)
            for model in models:
                self.listbox.insert(0, str(model))

            self.listbox.pack(side="top", fill='both')

            keywordframe = tk.Frame(answerframe)
            keywordframe.pack(side="bottom", fill="both")
            self.entry = tk.Entry(keywordframe, width=20)
            self.entry.pack(side="right", padx=5, pady=5)
            nameofprojlab = tk.Label(keywordframe, text="Filter for Keyword (Name of Project): ")
            nameofprojlab.pack(side="left", padx=5, pady=5)

            if back:
                sel = self.cfg['step3']['models']
                lb_items = self.listbox.get(0)
                for i, item in enumerate(lb_items):
                    if item in sel:
                        self.listbox.select_set(i)
                        self.listbox.event_generate("<<ListboxSelect>>")
                pname = self.cfg['step3']['project']
                self.entry.insert("1.0", pname)


        api = self.cfg['step1']['choice'].lower()
        stream_mode = self.choice.get()

        self.cframe = tk.Frame(self)
        self.cframe.pack(side="top", fill="x")
        self.nextbtn.config(text="Stream", command=self.init_stream)
        self.nextbtn.config(state='normal')
        choicelab = tk.Label(self.cframe, text=f"Select the models you want in your report.")
        choicelab.pack(side="top")
        answerframe = tk.Frame(self.cframe)
        answerframe.pack(side="bottom", fill="x")
        options()





    def init_stream(self):
        self.nextbtn.config(text="End Early", command=None)
        self.nextbtn.bind("<Button 1>", lambda e: self.master.from_stream_q.put({'done': True}))

        self.cfg['step2']['choice'] = self.choice.get()
        self.cfg['step3']['project'] = self.entry.get()

        api = self.cfg['step1']['choice'].lower()
        stream_mode = self.cfg['step2']['choice'].lower()
        project_name = self.cfg['step3']['project']
        print("api: ", api, " ; stream_mode: ", stream_mode)


        # selected_models = [MODELS[api][stream_mode][[int(i)]] for i in ]
        selected_models = []
        lb_items = self.listbox.get(0, tk.END)
        for sel in self.listbox.curselection():
            name = lb_items[sel]
            print("name: ", name)
            model = MODELS[api][stream_mode][name]
            selected_models.append(model)

        self.cfg['step3']['models'] = selected_models

        print(f"selected models: {selected_models}; projname: {self.cfg['step3']['project']}")
        required_data = []
        for dic in selected_models:
            # if api == 'reddit':
            #     data = dic['required_data']
            # else:
            #     data = dic['objects']
            data = dic['required_data']

            required_data.extend(data)

        choices = {'api': api, 'mode': stream_mode, 'data': required_data, 'project': project_name}

        self.master.models = [selected_models[i]['object'] for i in range(len(selected_models))]

        self.cframe.destroy()
        self.cframe = StreamFrame(self, self.master, choices)
        self.cframe.pack(fill='both', expand=1)

    def init_done_frame(self, **kwargs):
        print("init_done_frame")
        try:
            self.nextbtn.unbind("<Button 1>")
            self.cframe.destroy()
            self.cframe = DoneFrame(self, self.master, **kwargs)
            self.cframe.pack(fill='both', expand=1)
            self.cframe.report.show()

        except Exception as e:
            print("error during init_done_frame: ", e)




class StreamFrame(tk.Frame):
    def __init__(self, master, app, choices):
        tk.Frame.__init__(self, master)
        self.app = app
        self.wheel = ["|","/","-","\\"]
        self.w_index = 0
        self.var = tk.StringVar(value=self.wheel[self.w_index])
        loading_wheel = tk.Label(self, textvariable=self.var)
        loading_wheel.pack(side="top")

        self.data = []

        self.streamlab = tk.Label(self, text="streaming...")
        self.streamlab.pack(side="bottom", fill='x')

        self.app.to_stream_q.put(choices)
        self.streaming = True

        self.app.after(200, self.check_if_streaming)

    def update_wheel(self):
        if self.w_index < len(self.wheel):
            self.w_index += 1
        else:
            self.w_index = 0
        self.var.set(self.wheel[self.w_index])


    def check_if_streaming(self):
        while self.app.from_stream_q.qsize():
            try:
                info = self.app.from_stream_q.get(0)
                if info:
                    print("info: ", info)
                    try:
                        if info['done']:
                            self.app.to_stream_q.put({'stop': True})
                            self.streaming = False
                            print("call init_done_frame")
                            self.master.init_done_frame(data=self.data)
                            return
                    except KeyError:
                        pass
                    # try:
                    #     data = info['github-data']
                    #     self.streaming = False
                    #     print("call init_done_frame")
                    #     self.master.init_done_frame(data=data, gh=True)
                    #     return
                    # except KeyError:
                    #     pass
                    try:
                        if info['update_wheel']:
                            self.update_wheel()
                    except KeyError:
                        pass
                    try:
                        e = info['error']
                        messagebox.showerror(title='Error', message=e)
                    except KeyError:
                        pass
                    try:
                        item = info['item']
                        self.data.append(item)
                        self.streamlab.config(text=item['title'])
                    except KeyError:
                        pass
            except:
                pass

        if self.streaming:
            self.app.after(200, self.check_if_streaming)


class DoneFrame(tk.Frame):
    def __init__(self, master, app, data=None, gh=False):
        tk.Frame.__init__(self, master)
        print("doneframe data: ", data)
        print("doneframe gh: ", gh)
        tk.Label(self, text="Finished!").pack()
        self.app = app
        self.master.prevbtn.config(text="Build new report", command=self.master.restart, width=20)
        self.master.nextbtn.config(text="Exit", command= lambda: sys.exit(0))
        # popup = tk.Toplevel(self.app, width=500, height=500)
        # popup.title("Table")
        frame = tk.Frame(self)
        frame.pack(fill='both', expand=1)


        if not gh:
            self.report = Report(self, self.app.models, data, name=self.master.cfg['step3']['project'])

            datatable = FrameDataTable(frame, data)
            datatable.pack(side='bottom', fill='both', expand=1)

            topribbon = tk.Frame(frame)
            topribbon.pack(side="bottom", fill='x')

            savebtn = ttk.Button(topribbon, text="Save", command=self.report.file_save)
            # cancelbtn = ttk.Button(btmribbon, text="Cancel", command=popup.destroy)
            savebtn.pack(side="right", padx=5, pady=5)
        # else:
        #     report = GHReport(self, self.app.models, data, name=self.master.cfg['step3']['project'])


class FrameDataTable(ttk.Treeview):
    def __init__(self, master, data, *args, **kwargs):

        headers = []

        for header,value in data[0].items():
            headers.append(header)

        headers = ['id'] + headers

        super().__init__(master, *args, columns=headers, height=10, **kwargs)
        self['show'] = 'headings'

        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.yview)
        self.vsb.pack(side='right', fill='y')
        self.hsb = ttk.Scrollbar(self, orient="horizontal", command=self.xview)
        self.hsb.pack(side='bottom', fill='x')

        self.config(yscrollcommand=self.vsb.set)
        self.config(xscrollcommand=self.hsb.set)


        for col in headers:
            self.heading(col, text=col.title(), command=lambda c=col: self.sortby(c, 0))
            self.column(col, width=50)

        for id, row in enumerate(data):
            print("row: ", row)

            self.insert("", tk.END, values=[id] + list(row.values()), iid=id)


    def sortby(self, col, descending):
        """sort tree contents when a column header is clicked on"""

        data = [(self.set(child, col), child) for child in self.get_children('')]

        if col == '#':
            data.sort(key=lambda t: int(t[0]), reverse=descending)
        else:
            data.sort(reverse=descending)

        for i, item in enumerate(data):
            self.move(item[1], '', i)
        # switch the heading so it will sort in the opposite direction
        self.heading(col, command=lambda col=col: self.sortby(col, int(not descending)))






if __name__ == '__main__':
    root = Howdigo()
    root.mainloop()
