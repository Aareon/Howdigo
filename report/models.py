
if not __name__ == '__main__':
    from .core import plt, FigureCanvasTkAgg, NavigationToolbar2TkAgg, \
                    Figure, pd, np, write_csv_file, filedialog
else:
    import tkinter as tk
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
    from matplotlib.figure import Figure
    import pandas as pd
    import sys



class Canvas(FigureCanvasTkAgg):
    def __init__(self, figure, master, save_name=None):
        super().__init__(figure, master)
        self.draw()
        self._tkcanvas.pack()
        self.save_name = save_name

    def savefig(self, fname):
        plt.savefig(fname)


class Report:
    def __init__(self, master, models, data, size=(50,50), fontsize=20,name="plotgroup", title="Report"):
        plt_models = []
        for i, model in enumerate(models):
            m = model(data)
            plt_models.append(m)
        self.data = data
        self.project = name

    def file_save(self):
        f = filedialog.asksaveasfile(mode='w', title=f"{self.project}_report",defaultextension=".csv")
        if f is None:
            return
        write_csv_file(f, self.data)

    def show(self):
        plt.show()

class GHReport(Report):
    def __init__(self, master, models, data, name="github-report"):
        super().__init__(master, models, data, name=name)




class Pie(pd.DataFrame):
    def __init__(self, data, categories, title=None):
        super().__init__(data, index=categories)
        self.plot.pie()

        # fig.legend(self.chart[0], labels=['%s: %1.1f %%' % (l, s) for l, s in zip(labels, values)], loc="upper right")

        # Canvas.__init__(self, fig, master, save_name=save_name)


class StackedBars(pd.DataFrame):
    def __init__(self, data, xaxis_labels=None, title=None):
        super().__init__(data)
        self.plot.bar(stacked=True)


class Bars(pd.DataFrame):
    def __init__(self, data, xaxis_labels=None, title=None):
        super().__init__(data)
        self.plot.bar(legend=False)

class MultiColumnedBars(pd.DataFrame):
    def __init__(self, data, columns, xaxis_labels=None, title=None):
        super().__init__(data, columns=columns)
        self.plot.bar()



def test():
    root = tk.Tk()
    root.geometry("500x500")
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))

    # fig, axes = plt.subplots(nrows=2, ncols=2)
    # fig = plt.figure()
    items = {"tekken7": 500, "streetfighter5": 300, "dragonballfighterz": 200}
    # pie = PieCanvas(root, size=(50,50), labels_values=items)
    data = list(range(20))
    bars = Bars(data)

    # canvas = FigureCanvasTkAgg(fig, root)
    # canvas.draw()
    plt.show()

    root.mainloop()


if __name__ == '__main__':
    test()
