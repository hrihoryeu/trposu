from tkinter import Tk, Label, Menu, Menubutton, Checkbutton, Frame, LEFT, LabelFrame, Button, DISABLED, IntVar, RAISED, messagebox, ttk
import json
import pymongo
from pymongo import MongoClient 
from data import list_of_names


class Subscription():
    def __init__(self):
        self.cluster = MongoClient('mongodb+srv://Yegor:1234@cluster0.z0dtg.mongodb.net/<dbname>?retryWrites=true&w=majority')

        self.db = self.cluster['FitnessCenter']
        self.collection = self.db['visitors']

        self.list_of_names = list_of_names

        self.main = Tk()

        self.main.title('Fitness center')
        self.main.geometry('420x250')

        self.full_frame = LabelFrame(self.main)
        self.left_frame = LabelFrame(self.full_frame, text='Информация')
        self.right_frame = LabelFrame(self.full_frame)

        self.full_frame.pack(pady=20)
        self.left_frame.pack(side=LEFT)
        self.right_frame.pack(side=LEFT)

        self.info_label = Label(self.left_frame, height=4)
        self.info_label.pack(padx=5, pady=5)

        self.all_in_var = IntVar()
        self.all_in_check = Checkbutton(self.left_frame, text='Все пришли', variable=self.all_in_var, onvalue=True, offvalue=False, indicatoron=1)
        self.all_in_check.pack(padx=5, pady=5)

        self.not_all_in = ttk.Combobox(self.left_frame, text='Список посетителей', width=25, values = self.list_of_names)
        self.not_all_in.pack(padx=5, pady=5)

        self.start_button = Button(self.right_frame, text='Провести занятие', width=25, command=self.start)
        self.absent_button = Button(self.right_frame, text='Отсутствует', width=25, command=self.absent)
        self.top_up_button = Button(self.right_frame, text='Пополнить абонемент', width=25, command=self.top_up)
        self.show_data_button = Button(self.right_frame, text='Отобразить данные', width=25, command=self.show_data)

        self.start_button.pack(padx=5, pady=5)
        self.absent_button.pack(padx=5, pady=5)
        self.top_up_button.pack(padx=5, pady=5)
        self.show_data_button.pack(padx=5, pady=5)

        self.main.mainloop()

    def absent(self):
        self.collection.update_one({'name': self.not_all_in.get()}, {'$set':{'indicator':False}})
        self.info_label['text'] = 'Отсутствие {} не повлияет\nна количество занятий'.format(self.not_all_in.get())  

    def start(self):
        if self.all_in_var.get():
            self.all_to_true_false(True)
        
        if self.all_false():
            self.info_label['text'] = 'На занятие никто\nне пришел'
            self.all_to_true_false(True)
        else:
            check = self.with_zero()
            if check == True:
                for name in self.list_of_names:
                    for parametr in self.collection.find({'name': name}):
                        if parametr['indicator'] == True:
                            self.collection.update_one({'name':name}, {'$set':{'subscription':parametr['subscription'] - 1}})
                            self.info_label['text'] = 'Занятие успешно\nпроведено'
                self.all_to_true_false(True)
            else:
                self.info_label['text'] = '{} нужно пополнить\nабонемент'.format(check[1])
                
    def show_data(self):
        for parametr in self.collection.find({'name':self.not_all_in.get()}):
            self.info_label['text'] = '{}:\nосталось {} занятий(е/я)'.format(self.not_all_in.get(), parametr['subscription'])
   
    def top_up(self):
        for parametr in self.collection.find({'name':self.not_all_in.get()}):
            if parametr['subscription'] < 3:
                self.collection.update_one({'name': self.not_all_in.get()}, {'$set':{'subscription':8}})
                self.info_label['text'] = 'Абонемент для {}\n успешно пополнен'.format(self.not_all_in.get())
            else:
                self.info_label['text'] = 'ERROR!\nУ {} осталось\nбольше 2х занятий'.format(self.not_all_in.get())
    
    def all_to_true_false(self, bool_var = bool):
        if bool_var == False:
            for i in self.list_of_names:
                self.collection.update_one({'name': i}, {'$set':{'indicator':False}})
        else:
            for i in self.list_of_names:
                self.collection.update_one({'name': i}, {'$set':{'indicator':True}})
    
    def all_false(self):
        count = 0
        for name in self.list_of_names:
            for parameter in self.collection.find({'name':name}):
                if parameter['indicator'] == True:
                    count += 1 
        if count == 0:
            return True
        else:
            return False

    def with_zero(self):
        count = 0
        who = ''
        for name in self.list_of_names:
            for parameter in self.collection.find({'name':name}):
                if parameter['subscription'] < 1 and parameter['indicator'] == True:
                    count += 1
                    who = name
        if count == 0:
            return True
        else:
            return [False, who]

prog = Subscription()