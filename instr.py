import tkinter as tk
from tkinter import messagebox
from collections import defaultdict


class AutoServiceApp(tk.Tk):
    def __init__(self, auto_service):
        super().__init__()
        self.auto_service = auto_service
        self.title("Управление автосервисом")
        self.geometry("600x400")
        self.configure(bg='#f0f0f0')

        self.current_frame = None
        self.show_login()

    def show_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill='both', expand=True)

    def show_login(self):
        self.show_frame(LoginFrame)

    def show_register(self):
        self.show_frame(RegisterFrame)

    def show_main_menu(self):
        self.show_frame(MainMenuFrame)

    def show_services(self):
        self.show_frame(ServicesFrame)

    def show_make_appointment(self):
        self.show_frame(MakeAppointmentFrame)

    def show_appointments(self):
        self.show_frame(AppointmentsFrame)

    def show_update_appointment(self):
        self.show_frame(UpdateAppointmentFrame)

    def show_delete_appointment(self):
        self.show_frame(DeleteAppointmentFrame)


class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        tk.Label(self, text="Вход", font=('Arial', 24)).pack(pady=20)

        tk.Label(self, text="Имя пользователя").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Пароль").pack()
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack()

        tk.Button(self, text="Войти", command=self.login).pack(pady=10)
        tk.Button(self, text="Регистрация", command=self.master.show_register).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.master.auto_service.login(username, password)
        if self.master.auto_service.current_user:
            self.master.show_main_menu()
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")


class RegisterFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        tk.Label(self, text="Регистрация", font=('Arial', 24)).pack(pady=20)

        tk.Label(self, text="Имя пользователя").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Пароль").pack()
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack()

        tk.Button(self, text="Зарегистрироваться", command=self.register).pack(pady=10)
        tk.Button(self, text="Назад", command=self.master.show_login).pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.master.auto_service.register(username, password)
        messagebox.showinfo("Успех", "Регистрация прошла успешно")
        self.master.show_login()


class MainMenuFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        tk.Label(self, text="Главное меню", font=('Arial', 24)).pack(pady=20)

        tk.Button(self, text="Посмотреть услуги", command=self.master.show_services).pack(fill='x', pady=5)
        tk.Button(self, text="Записаться на прием", command=self.master.show_make_appointment).pack(fill='x', pady=5)
        tk.Button(self, text="Посмотреть записи", command=self.master.show_appointments).pack(fill='x', pady=5)
        tk.Button(self, text="Обновить запись", command=self.master.show_update_appointment).pack(fill='x', pady=5)
        tk.Button(self, text="Удалить запись", command=self.master.show_delete_appointment).pack(fill='x', pady=5)
        tk.Button(self, text="Выйти", command=self.logout).pack(fill='x', pady=5)

    def logout(self):
        self.master.auto_service.logout()
        self.master.show_login()


class ServicesFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        tk.Label(self, text="Услуги", font=('Arial', 24)).pack(pady=20)

        for key, value in self.master.auto_service.services.items():
            tk.Label(self, text=f"{key}. {value}").pack()

        tk.Button(self, text="Назад", command=self.master.show_main_menu).pack(pady=20)


class MakeAppointmentFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        tk.Label(self, text="Запись на прием", font=('Arial', 24)).pack(pady=20)

        tk.Label(self, text="Имя").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        tk.Label(self, text="Телефон").pack()
        self.phone_entry = tk.Entry(self)
        self.phone_entry.pack()

        tk.Label(self, text="Автомобиль").pack()
        self.car_entry = tk.Entry(self)
        self.car_entry.pack()

        tk.Label(self, text="Услуги (через запятую)").pack()
        self.services_entry = tk.Entry(self)
        self.services_entry.pack()

        tk.Button(self, text="Записаться", command=self.make_appointment).pack(pady=10)
        tk.Button(self, text="Назад", command=self.master.show_main_menu).pack()

    def make_appointment(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        car = self.car_entry.get()
        services = self.services_entry.get().split(',')
        services = [int(service.strip()) for service in services if service.strip().isdigit()]

        self.master.auto_service.make_appointment(name, phone, car, services)
        messagebox.showinfo("Успех", "Вы успешно записались на прием")
        self.master.show_main_menu()


class AppointmentsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        tk.Label(self, text="Записи", font=('Arial', 24)).pack(pady=20)

        tk.Label(self, text="Фильтр по телефону (опционально)").pack()
        self.phone_filter_entry = tk.Entry(self)
        self.phone_filter_entry.pack()

        self.appointments_text = tk.Text(self)
        self.appointments_text.pack()

        self.display_appointments()

        tk.Button(self, text="Фильтровать", command=self.display_appointments).pack(pady=5)
        tk.Button(self, text="Назад", command=self.master.show_main_menu).pack(pady=20)

    def display_appointments(self):
        self.appointments_text.delete(1.0, tk.END)
        phone_filter = self.phone_filter_entry.get()
        appointments = self.master.auto_service.appointments
        if not appointments:
            self.appointments_text.insert(tk.END, "Нет записей\n")
        else:
            for service, appointments_list in appointments.items():
                for appointment in appointments_list:
                    if appointment['user'] == self.master.auto_service.current_user:
                        if phone_filter and phone_filter != appointment['phone']:
                            continue
                        self.appointments_text.insert(tk.END, f"Услуга: {self.master.auto_service.services[service]}\n")
                        self.appointments_text.insert(tk.END, f"Имя: {appointment['name']}\n")
                        self.appointments_text.insert(tk.END, f"Телефон: {appointment['phone']}\n")
                        self.appointments_text.insert(tk.END, f"Автомобиль: {appointment['car']}\n")
                        self.appointments_text.insert(tk.END, "------------\n")


class UpdateAppointmentFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        tk.Label(self, text="Обновление записи", font=('Arial', 24)).pack(pady=20)

        tk.Label(self, text="Телефон").pack()
        self.phone_entry = tk.Entry(self)
        self.phone_entry.pack()

        tk.Label(self, text="Услуга").pack()
        self.service_entry = tk.Entry(self)
        self.service_entry.pack()

        tk.Label(self, text="Новое имя (опционально)").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        tk.Label(self, text="Новый телефон (опционально)").pack()
        self.new_phone_entry = tk.Entry(self)
        self.new_phone_entry.pack()

        tk.Label(self, text="Новый автомобиль (опционально)").pack()
        self.car_entry = tk.Entry(self)
        self.car_entry.pack()

        tk.Button(self, text="Обновить", command=self.update_appointment).pack(pady=10)
        tk.Button(self, text="Назад", command=self.master.show_main_menu).pack()

    def update_appointment(self):
        phone = self.phone_entry.get()
        service = int(self.service_entry.get().strip())
        name = self.name_entry.get()
        new_phone = self.new_phone_entry.get()
        car = self.car_entry.get()

        if not self.master.auto_service.update_appointment(phone, service, name, new_phone, car):
            messagebox.showerror("Ошибка", "Запись не найдена или принадлежит другому пользователю.")
        else:
            messagebox.showinfo("Успех", "Запись успешно обновлена")
            self.master.show_main_menu()


class DeleteAppointmentFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        tk.Label(self, text="Удаление записи", font=('Arial', 24)).pack(pady=20)

        tk.Label(self, text="Телефон").pack()
        self.phone_entry = tk.Entry(self)
        self.phone_entry.pack()

        tk.Label(self, text="Услуги (через запятую)").pack()
        self.services_entry = tk.Entry(self)
        self.services_entry.pack()

        tk.Button(self, text="Удалить", command=self.delete_appointment).pack(pady=10)
        tk.Button(self, text="Назад", command=self.master.show_main_menu).pack()

    def delete_appointment(self):
        phone = self.phone_entry.get()
        services = self.services_entry.get().split(',')
        services = [int(service.strip()) for service in services if service.strip().isdigit()]

        self.master.auto_service.delete_appointment(phone, services)
        messagebox.showinfo("Успех", "Запись успешно удалена")
        self.master.show_main_menu()


class AutoService:
    def __init__(self):
        self.services = {
            1: "Замена масла",
            2: "Замена тормозных колодок",
            3: "Ремонт двигателя",
            4: "Шиномонтаж",
            5: "Обслуживание двигателя",
            6: "Обслуживание ходовой",
            7: "Кузовные работы",
            8: "Замена других жидкостей"
        }
        self.appointments = defaultdict(list)
        self.users = {}
        self.current_user = None

    def register(self, username, password):
        if username in self.users:
            print("Пользователь с таким именем уже существует.")
        else:
            self.users[username] = password
            print("Регистрация прошла успешно.")

    def login(self, username, password):
        if username in self.users and self.users[username] == password:
            self.current_user = username
            print("Вы успешно вошли в систему.")
        else:
            print("Неверное имя пользователя или пароль.")

    def logout(self):
        self.current_user = None
        print("Вы вышли из системы.")

    def make_appointment(self, name, phone, car, services):
        for appointments in self.appointments.values():
            for appointment in appointments:
                if appointment['phone'] == phone:
                    print(f"Запись с номером телефона {phone} уже существует.")
                    return

        for service in services:
            if service in self.services:
                self.appointments[service].append({
                    'name': name,
                    'phone': phone,
                    'car': car,
                    'user': self.current_user
                })
                print(f"Вы успешно записаны на прием по услуге: {self.services[service]}")
            else:
                print(f"Услуги с номером {service} не существует.")

    def update_appointment(self, phone, service, name=None, new_phone=None, car=None):
        found = False
        if service in self.appointments:
            for appointment in self.appointments[service]:
                if appointment['phone'] == phone and appointment['user'] == self.current_user:
                    found = True
                    if name:
                        appointment['name'] = name
                    if new_phone:
                        appointment['phone'] = new_phone
                    if car:
                        appointment['car'] = car
                    print(f"Информация по записи с номером телефона {phone} успешно обновлена.")
                    break

        if not found:
            print(f"Запись с номером телефона {phone} не найдена.")
            return False
        return True

    def delete_appointment(self, phone, services=None):
        if not self.appointments:
            print("\nНет записей для удаления.")
            return
        found = False
        for service in services:
            if service in self.appointments:
                for appointment in list(self.appointments[service]):
                    if appointment['phone'] == phone and appointment['user'] == self.current_user:
                        self.appointments[service].remove(appointment)
                        found = True
                if not self.appointments[service]:
                    del self.appointments[service]
        if not found:
            print(f"Запись с номером телефона {phone} не найдена.")
        else:
            print(f"Записи с номером телефона {phone} по выбранным услугам успешно удалены.")


if __name__ == "__main__":
    auto_service = AutoService()
    app = AutoServiceApp(auto_service)
    app.mainloop()
