from tkinter import *
import requests
import re


class tkinter_App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, conf_cars, conf_customer, assign_car, add_cars,
                  edit_cars, delete_cars, add_customer, edit_customer):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="Main Menu", height=3, font=("", 22))
        label.pack()

        button3 = Button(self, text="Assign cars to customer",
                         command=lambda: controller.show_frame(assign_car), height=2)
        button3.pack(fill=X, side=BOTTOM)

        button2 = Button(self, text="Configure Customers",
                         command=lambda: controller.show_frame(conf_customer), height=2)
        button2.pack(fill=X, side=BOTTOM)

        button1 = Button(self, text="Configure Cars",
                         command=lambda: controller.show_frame(conf_cars), height=2)
        button1.pack(fill=X, side=BOTTOM)


class conf_cars(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Configure Cars", height=3, font=("", 22))
        label.pack(fill=X)

        button4 = Button(self, text="Back",
                         command=lambda: controller.show_frame(StartPage), height=2)
        button4.pack(fill=X, side=BOTTOM)
        button3 = Button(self, text="Remove",
                         command=lambda: (controller.show_frame(delete_cars), get_database_models()), height=2)
        button3.pack(fill=X, side=BOTTOM)
        button2 = Button(self, text="Edit",
                         command=lambda: (controller.show_frame(edit_cars), get_database_models()), height=2)
        button2.pack(fill=X, side=BOTTOM)
        button1 = Button(self, text="Add",
                         command=lambda: controller.show_frame(add_cars), height=2)
        button1.pack(fill=X, side=BOTTOM)


class add_cars(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Add Cars", height=5, font=("", 22))
        label.grid()

        Label(self, text="Manufacturer").grid(row=2, column=0)
        self.manufacturer = Entry(self)
        self.manufacturer.grid(row=2, column=1)
        Label(self, text="Year").grid(row=3, column=0)
        self.year = Entry(self)
        self.year.grid(row=3, column=1)
        Label(self, text="Customer").grid(row=4, column=0)
        self.customer = Entry(self)
        self.customer.grid(row=4, column=1)

        button4 = Button(self, text="Back",
                         command=lambda: self.controller.show_frame(conf_cars), height=2)
        button4.grid(row=5, column=0)
        button5 = Button(self, text="Submit",
                         command=lambda: self.add_car_func(), height=2)
        button5.grid(row=5, column=1)

    def add_car_func(self):
        manufacturer = self.manufacturer.get()
        year = int(self.year.get())
        customer_id = self.customer.get()
        output = {'manufacturer': f'{manufacturer}', 'year': f'{year}', 'customer_id': f'{customer_id}'}

        res = requests.post("http://127.0.0.1:5000/models/", json=output)
        self.controller.show_frame(conf_cars)


def get_database_models():
    response = requests.get('http://localhost:5000/models/')
    options_list = response.json()
    models = []
    for i in options_list:
        models.append(f'id {i["id"]}: {i["manufacturer"]}')
    return models


class edit_cars(Frame):
    def __init__(self, parent, controller):
        models = get_database_models()
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Edit Cars", height=5, font=("", 22))
        label.grid(sticky=E)
        self.value_inside = StringVar(self)
        self.value_inside.set("Select car ID")
        self.question_menu = OptionMenu(self, self.value_inside, *models)
        self.question_menu.grid(row=1, column=0)
        Label(self, text="Manufacturer").grid(row=2, column=0)
        self.manufacturer = Entry(self)
        self.manufacturer.grid(row=2, column=1)
        Label(self, text="Year").grid(row=3, column=0)
        self.year = Entry(self)
        self.year.grid(row=3, column=1)
        Label(self, text="Customer").grid(row=4, column=0)
        self.customer = Entry(self)
        self.customer.grid(row=4, column=1)
        button4 = Button(self, text="Back",
                         command=lambda: self.controller.show_frame(conf_cars), height=2)
        button4.grid(row=5, column=0, sticky=N + S + E + W)
        button5 = Button(self, text="Submit",
                         command=lambda: self.add_car_func(), height=2)
        button5.grid(row=5, column=1, sticky=N + S + E + W)

    def add_car_func(self):
        menu_choice = self.value_inside.get()
        temp = re.findall(r'\d+', menu_choice)
        id_model = int(temp[0])

        manufacturer = self.manufacturer.get()
        year = int(self.year.get())
        customer_id = self.customer.get()
        output = {'manufacturer': f'{manufacturer}', 'year': f'{year}', 'customer_id': f'{customer_id}'}

        res = requests.put(f"http://127.0.0.1:5000/models/{id_model}/", json=output)
        self.controller.show_frame(conf_cars)


class delete_cars(Frame):
    def __init__(self, parent, controller):
        models = get_database_models()
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Delete Cars", height=5, font=("", 22))
        label.grid()
        self.value_inside = StringVar(self)
        self.value_inside.set("Select car ID")
        self.question_menu = OptionMenu(self, self.value_inside, *models)
        self.question_menu.grid(row=1, column=0)
        button4 = Button(self, text="Back",
                         command=lambda: self.controller.show_frame(conf_cars), height=2)
        button4.grid(row=5, column=0, sticky=N + S + E + W)
        button5 = Button(self, text="Submit",
                         command=lambda: self.delete_car_func(), height=2)
        button5.grid(row=5, column=1, sticky=N + S + E + W)

    def delete_car_func(self):
        menu_choice = self.value_inside.get()
        temp = re.findall(r'\d+', menu_choice)
        id_model = int(temp[0])

        res = requests.delete(f"http://127.0.0.1:5000/models/{id_model}/")
        self.controller.show_frame(conf_cars)


class conf_customer(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Configure Customers", height=5, font=("", 22))
        label.pack(fill=X)

        button4 = Button(self, text="Back",
                         command=lambda: controller.show_frame(StartPage), height=2)
        button4.pack(fill=X, side=BOTTOM)

        button3 = Button(self, text="Remove",
                         command=lambda: controller.show_frame(StartPage), height=2)
        button3.pack(fill=X, side=BOTTOM)

        button2 = Button(self, text="Edit",
                         command=lambda: controller.show_frame(edit_customer), height=2)
        button2.pack(fill=X, side=BOTTOM)

        button1 = Button(self, text="Add",
                         command=lambda: controller.show_frame(add_customer), height=2)
        button1.pack(fill=X, side=BOTTOM)


class add_customer(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Add Customer", height=5, font=("", 22))
        label.grid()

        Label(self, text="First Name").grid(row=2, column=0)
        self.first_name = Entry(self)
        self.first_name.grid(row=2, column=1)
        Label(self, text="Family Name").grid(row=3, column=0)
        self.family_name = Entry(self)
        self.family_name.grid(row=3, column=1)
        Label(self, text="Age").grid(row=4, column=0)
        self.age = Entry(self)
        self.age.grid(row=4, column=1)

        button4 = Button(self, text="Back",
                         command=lambda: self.controller.show_frame(conf_cars), height=2)
        button4.grid(row=5, column=0)
        button5 = Button(self, text="Submit",
                         command=lambda: self.add_customer_func(), height=2)
        button5.grid(row=5, column=1)

    def add_customer_func(self):
        first_name = self.first_name.get()
        family_name = self.family_name.get()
        age = int(self.age.get())
        output = {'first_name': f'{first_name}', 'family_name': f'{family_name}', 'age': f'{age}'}

        res = requests.post("http://127.0.0.1:5000/customers/", json=output)
        self.controller.show_frame(conf_cars)


def get_database_customers():
    response = requests.get('http://localhost:5000/customers/')
    options_list = response.json()
    models = []
    for i in options_list:
        models.append(f'id {i["id"]}: {i["family_name"]}, {i["first_name"]}')
    return models


class edit_customer(Frame):
    def __init__(self, parent, controller):
        customers = get_database_customers()
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Edit Customer", height=5, font=("", 22))
        label.grid(sticky=E)
        self.value_inside = StringVar(self)
        self.value_inside.set("Select customer ID")
        self.question_menu = OptionMenu(self, self.value_inside, *customers)
        self.question_menu.grid(row=1, column=0)
        Label(self, text="First Name").grid(row=2, column=0)
        self.manufacturer = Entry(self)
        self.manufacturer.grid(row=2, column=1)
        Label(self, text="Family Name").grid(row=3, column=0)
        self.year = Entry(self)
        self.year.grid(row=3, column=1)
        Label(self, text="Age").grid(row=4, column=0)
        self.customer = Entry(self)
        self.customer.grid(row=4, column=1)
        button4 = Button(self, text="Back",
                         command=lambda: self.controller.show_frame(conf_cars), height=2)
        button4.grid(row=5, column=0, sticky=N + S + E + W)
        button5 = Button(self, text="Submit",
                         command=lambda: self.add_car_func(), height=2)
        button5.grid(row=5, column=1, sticky=N + S + E + W)

    def add_car_func(self):
        menu_choice = self.value_inside.get()
        temp = re.findall(r'\d+', menu_choice)
        id_model = int(temp[0])

        manufacturer = self.manufacturer.get()
        year = int(self.year.get())
        customer_id = self.customer.get()
        output = {'manufacturer': f'{manufacturer}', 'year': f'{year}', 'customer_id': f'{customer_id}'}

        res = requests.put(f"http://127.0.0.1:5000/models/{id_model}/", json=output)
        self.controller.show_frame(conf_cars)


class delete_customer(Frame):
    def __init__(self, parent, controller):
        customers = get_database_customers()
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Delete Customer", height=5, font=("", 22))
        label.grid()
        self.value_inside = StringVar(self)
        self.value_inside.set("Select Customer ID")
        self.question_menu = OptionMenu(self, self.value_inside, *customers)
        self.question_menu.grid(row=1, column=0)
        button4 = Button(self, text="Back",
                         command=lambda: self.controller.show_frame(conf_cars), height=2)
        button4.grid(row=5, column=0, sticky=N + S + E + W)
        button5 = Button(self, text="Submit",
                         command=lambda: self.delete_car_func(), height=2)
        button5.grid(row=5, column=1, sticky=N + S + E + W)

    def delete_car_func(self):
        menu_choice = self.value_inside.get()
        temp = re.findall(r'\d+', menu_choice)
        id_model = int(temp[0])

        res = requests.delete(f"http://127.0.0.1:5000/models/{id_model}/")
        self.controller.show_frame(conf_cars)


class assign_car(Frame):
    def __init__(self, parent, controller):
        customers = get_database_customers()
        models = get_database_models()
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Edit Customer", height=5, font=("", 22))
        label.grid()
        self.value_inside_model = StringVar(self)
        self.value_inside_model.set("Select Car ID")
        self.question_menu_model = OptionMenu(self, self.value_inside_model, *models)
        self.question_menu_model.grid(row=1, column=0)

        self.value_inside_customer = StringVar(self)
        self.value_inside_customer.set("Select customer ID")
        self.question_menu_customer = OptionMenu(self, self.value_inside_customer, *customers)
        self.question_menu_customer.grid(row=1, column=1)
        button4 = Button(self, text="Assign Customer to Car",
                         command=lambda: self.controller.show_frame(conf_cars), height=2)
        button4.grid(row=5, column=0)
        button5 = Button(self, text="Assign Car to Customer",
                         command=lambda: self.add_car_func(), height=2)
        button5.grid(row=5, column=1)

    def add_car_func(self):
        menu_choice = self.value_inside_model.get()
        temp = re.findall(r'\d+', menu_choice)
        id_model = int(temp[0])

        manufacturer = self.manufacturer.get()
        year = int(self.year.get())
        customer_id = self.customer.get()
        output = {'manufacturer': f'{manufacturer}', 'year': f'{year}', 'customer_id': f'{customer_id}'}

        res = requests.put(f"http://127.0.0.1:5000/models/{id_model}/", json=output)
        self.controller.show_frame(conf_cars)


def main():
    app = tkinter_App()
    app.mainloop()


if __name__ == '__main__':
    main()
