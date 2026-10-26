import requests
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

currencies = {
    "USD": "Доллар США",
    "EUR": "Евро",
    "CNY": "Юань",
    "RUB": "Российский рубль",
}

def update_currency_label(event):
    code = target_combobox.get()
    name = currencies.get(code, code)
    currency_label.config(text=name)

def exchange():
    target_code = target_combobox.get()
    base1_code = base1_combobox.get()
    base2_code = base2_combobox.get()

    if not target_code:
        mb.showerror('Ошибка', 'Выберите целевую валюту')
        return

    results = []

    for base_code, base_name in [(base1_code, "Первая базовая"), (base2_code, "Вторая базовая")]:
        if not base_code:
            continue

        try:
            response = requests.get(f"https://open.er-api.com/v6/latest/{base_code}")
            response.raise_for_status()
            data = response.json()

            if target_code in data.get('rates', {}):
                rate = data['rates'][target_code]
                base_full_name = currencies.get(base_code, base_code)
                target_full_name = currencies.get(target_code, target_code)
                results.append(f"{base_name}: {rate:.4f} {target_full_name} за 1 {base_full_name}")
            else:
                results.append(f"{base_name}: валюта {target_code} не найдена в данных для {base_code}")
        except Exception as e:
            results.append(f"{base_name}: ошибка при запросе — {e}")

    if results:
        message = "\n".join(results)
        mb.showinfo('Курсы обмена', message)
    else:
        mb.showerror('Ошибка', 'Не удалось получить ни одного курса')

root = Tk()
root.title("Курс валют (два базовых)")
root.geometry("350x280")

Label(text='Первая базовая валюта').pack(pady=5, padx=10)
base1_combobox = ttk.Combobox(values=list(currencies.keys()), state="readonly")
base1_combobox.pack()

Label(text='Вторая базовая валюта').pack(pady=5, padx=10)
base2_combobox = ttk.Combobox(values=list(currencies.keys()), state="readonly")
base2_combobox.pack()

Label(text='Целевая валюта').pack(pady=5, padx=10)
target_combobox = ttk.Combobox(values=list(currencies.keys()), state="readonly")
target_combobox.pack()
target_combobox.bind("<<ComboboxSelected>>", update_currency_label)

currency_label = ttk.Label()
currency_label.pack(pady=10, padx=10)

button = Button(text='Получить курсы', command=exchange)
button.pack()

root.mainloop()