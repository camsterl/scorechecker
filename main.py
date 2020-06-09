import tkinter as tk
from tkinter import ttk
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import csv



score = []
time = []
home = []
away = []

scores = tk.Tk()
tree = ttk.Treeview(scores, height =  45)

def updates():

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome('C:\\Users\\Cameron Kerr\\PycharmProjects\\scorechecker\\chromedriver.exe', options=options)
    url = "https://www.flashscore.com.au/football/"


    driver.get(url)
    c = driver.page_source
    soup = BeautifulSoup(c, "html.parser")

    for g in soup.find_all('div', {'class': ['event__scores fontBold', 'event__scores']}):
        score.append(g.text)
        #print(score)


    for g in soup.find_all('div', {'class': ['event__stage--block', 'event__time']}):
        #if g.text == 'Finished':
            #continue
        #else:
        fixed_time = g.text
        fixed_time = fixed_time.replace(" \xa0", "")
        time.append(fixed_time)
            #print(time)

    for g in soup.find_all('div', {'class': ['event__participant event__participant--home','event__participant event__participant--home fontBold']}):
        home.append(g.text)
        #print(home)

    for g in soup.find_all('div', {'class': ['event__participant event__participant--away', 'event__participant event__participant--away fontBold']}):
        away.append(g.text)
        #print(away)

    df = pd.DataFrame.from_dict({'Home': home, 'Away': away, 'Scores': score, 'Time': time}, orient='index')
    df.transpose()
    df.to_csv('games.csv', index=False, header=True, encoding='utf-8')
    print("Finished sorting results")
    driver.close()
    driver.quit()





   

    f = open('games.csv')
    csv_f = csv.reader(f)
    next(f)


    scores.title("Live Soccer Scores")




    tree.grid(columnspan=4)
    tree["columns"]= ["Time", "Home", "Scores", "Away"]
    tree["show"] = "headings"
    tree.heading("Home", text="Home")
    tree.heading("Away", text="Away")
    tree.heading("Scores", text="Score")
    tree.heading("Time", text="Time")
    tree.column("Time", anchor=tk.CENTER, stretch=True)
    tree.column("Home", anchor=tk.CENTER, stretch=True)
    tree.column("Scores", anchor=tk.CENTER, stretch=True)
    tree.column("Away", anchor=tk.CENTER, stretch=True)
    tree.pack(fill='both')

    for row in tree.get_children():
        tree.delete(row)
        print(row)

    for row in csv_f:

        print(row)
        merged_list = [(time[i], home[i], score[i], away[i]) for i in range(0, len(home))]
        print(merged_list)

    index = 0
    for col in merged_list:
        tree.insert("", index, values=col)
        index = index + 1

    #scores.mainloop()
    columns = ['Time', 'Home', 'Score', 'Away']

    i = 0
    while i < 10:
        print(i)
        i = i + 1



    tree.after(30000, updates)

updates()
tree.mainloop()
