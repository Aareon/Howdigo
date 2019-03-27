
if not __name__ == '__main__':
    from .core import pd, np, write_csv_file, filedialog, plt 
else:
    import tkinter as tk
    import pandas as pd
    import sys



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
    pass


if __name__ == '__main__':
    test()
