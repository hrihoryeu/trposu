from tkinter import Tk, Label, Menu, Menubutton, Checkbutton, Frame, LEFT, LabelFrame, Button, DISABLED, IntVar, RAISED, messagebox, ttk
import json

class Subscription():
    def __init__(self):
        self.data_file = open('visitors_data.txt', 'r', encoding='utf-8')

        self.main = Tk()

        self.main.title('Fitness center')
        self.main.geometry('420x250')

        self.full_frame = LabelFrame(self.main)
        self.left_frame = LabelFrame(self.full_frame, text='Информация')
        self.right_frame = LabelFrame(self.full_frame)

        self.full_frame.pack(pady=20)
        self.left_frame.pack(side=LEFT)
        self.right_frame.pack(side=LEFT)

        self.info_label = Label(self.left_frame, height=5)
        self.info_label.pack(padx=5, pady=5)

        self.all_in_var = IntVar()
        self.all_in_check = Checkbutton(self.left_frame, text='Все пришли', variable=self.all_in_var, onvalue=True, offvalue=False, indicatoron=1)
        self.all_in_check.pack(padx=5, pady=5)
        
        self.list_of_visitors = json.load(self.data_file)

        self.not_all_in = ttk.Combobox(self.left_frame, text='Список посетителей', width=25, values = list(self.list_of_visitors))
        self.not_all_in.pack(padx=5, pady=5)

        for i in enumerate(self.list_of_visitors):
            self.list_of_visitors[i[1]].append(True)
        print(self.list_of_visitors)

        self.start_button = Button(self.right_frame, text='Провести занятие', width=25, command=self.start)
        self.absent_button = Button(self.right_frame, text='Отсутствует', width=25, command=self.absent)
        self.top_up_button = Button(self.right_frame, text='Пополнить абонемент', width=25, command=self.top_up)
        self.show_data_button = Button(self.right_frame, text='Отобразить данные', width=25, command=self.show_data)
        self.save_button = Button(self.right_frame, text='Сохранить данные', width=25, command=self.save_file)

        self.start_button.pack(padx=5, pady=5)
        self.absent_button.pack(padx=5, pady=5)
        self.top_up_button.pack(padx=5, pady=5)
        self.show_data_button.pack(padx=5, pady=5)
        self.save_button.pack(padx=5, pady=5)

        self.main.mainloop()

    def absent(self):
        self.list_of_visitors[self.not_all_in.get()][1] = False
        self.info_label['text'] = 'Отсутствие {} не повлияет\nна количество занятий'.format(self.not_all_in.get())
        print(self.list_of_visitors)       

    def start_1(self):
        count = 0
        if self.all_in_var.get():
            for i in self.list_of_visitors:
                self.all_in_check.deselect()
                if self.list_of_visitors[i][0] < 1:
                    break
                self.list_of_visitors[i][0] -= 1
                count += 1
            if count < len(self.list_of_visitors):
                self.info_label['text'] = 'Нужно пополнить абонемент\nдля {}'.format(i)
                for i in enumerate(self.list_of_visitors):
                    if i[0] < count:
                        self.list_of_visitors[i[1]][0] += 1
            else:
                self.info_label['text'] = 'Занятие успешно\nпроведено'
        elif len(self.new_list) > 0:
            for i in self.new_list:
                if self.list_of_visitors[i][0] < 1:
                    break
                self.list_of_visitors[i][0] -= 1
                count += 1
            if count < len(self.list_of_visitors):
                self.info_label['text'] = 'Нужно пополнить абонемент\nдля {}'.format(i)
                for i in enumerate(self.list_of_visitors):
                    if i[0] < count:
                        self.list_of_visitors[i[1]][0] += 1
            else:
                self.new_list = list()
                self.info_label['text'] = 'Занятие успешно\nпроведено'
        else:
            self.info_label['text'] = 'Нужно хоть\nчто-то нажать'

    def start(self):
        if self.all_in_var.get():
            self.all_to_true_false(True)
        
        if self.all_false():
            print(self.all_false())
            self.info_label['text'] = 'Нужно хоть\nчто-то нажать'
        else:
            for i in self.list_of_visitors:
                if self.list_of_visitors[i][1]:
                    self.list_of_visitors[i][0] -= 1
            self.info_label['text'] = 'Занятие успешно\nпроведено'
            self.all_to_true_false(True)
        
    def show_data(self):
        self.info_label['text'] = '{}:\nосталось {} занятий(е/я)'.format(self.not_all_in.get(), self.list_of_visitors[self.not_all_in.get()][0])

    def top_up(self):
        for i in self.counter_func():
            if self.list_of_visitors[self.counter_func()[i]][0] < 3:
                self.list_of_visitors[self.counter_func()[i]][0] = 8
                self.info_label['text'] = 'Абонемент для {}\n успешно пополнен'.format(self.counter_func()[i])
            else:
                self.info_label['text'] = 'ERROR!\nУ {} осталось\nбольше 2х занятий'.format(self.counter_func()[i])
    
    def counter_func(self):
        a = 0
        counter = dict()
        for i in self.list_of_visitors:
            a += 1
            if self.list_of_visitors[i][1].get() == True:
                counter.update({a: i})
        return counter
    
    def save_file(self):
        self.info_label['text'] = 'Успешное сохранение'

    def all_to_true_false(self, bool_var = bool):
        if bool_var == False:
            for i in self.list_of_visitors:
                self.list_of_visitors[i][1] = False
        else:
            for i in self.list_of_visitors:
                self.list_of_visitors[i][1] = True
    
    def all_false(self):
        count = 0
        for i in self.list_of_visitors:
            if self.list_of_visitors[i][1] == True:
                count += 1
        if count == 0:
            return True
        else:
            return False

    def with_zero(self):
        for i in self.list_of_visitors:
            if self.list_of_visitors[i][0] == 0:
                return False
            else:
                return True


'''    def no_access(some_list = dict):
        for i in some_list:
            if '''
prog = Subscription()