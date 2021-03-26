from infoget import getComments
from tkinter import *
import logging
fields = 'subreddit', 'limit'
sort_types = "top", "hot", "new"

def getVal(entries):
    inp = {}
    for entry in entries:
        inp[entry[0]] = entry[1].get()
    print(inp)
    getComments(inp)
def makeform(root, fields):
    entries = []
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=15, text=field, anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append((field, ent))
    return entries

if __name__ == "__main__":
    logging.basicConfig(filename='logs/runlog.log', encoding='utf-8', level=logging.DEBUG)
    logging.info("Program Started.")
    root = Tk()
    root.title("Redapi Scraper")
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: getVal(e)))
    b1 = Button(root, text='Show',
                  command=(lambda e=ents: getVal(e)))
    b1.pack(side=LEFT, padx=5, pady=5)
    b2 = Button(root, text='Quit', command=root.quit)
    b2.pack(side=LEFT, padx=5, pady=5)
    root.mainloop()

    #getComments(None)
