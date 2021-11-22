import csv
import datetime
import smtplib
import json


def main():
    filename = "meters_datas"
    datas = read_cvs(filename)
    print(datas)
    print(date_today())
    print(meters_data_for_print(filename))
    choice = menu()
    if choice == '1':
        update_meter_data(filename)
    elif choice == '2':
        text = meters_data_for_print(filename)
        send_notification(text)
    elif choice == '3':
        pass
    else:
            while choice != '1':
                choice = menu()   

def read_cvs(filename):
    '''Func that reads csv file (delimiter is '\n') and returns a list of data'''
    data_list = []
    filename = filename + '.csv'
    with open(filename, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter = '\n')
        for row_list in reader:
            data_list.append(row_list)
    print('Данные прочитаны из файла')
    return data_list

def read_list(list, element):
    '''Func get list and return n-element string'''
    return list[element]

def menu():
    print("МЕНЮ\n\n1 - ОБНОВИТЬ показания\n2 - ОТПРАВИТЬ показания по email\n3 - ДОБАВИТЬ НОВЫЙ счетчик")
    return input()

def update_meter_data(filename):
    print('Будем обновлять показания счетчика')
    meter_number = input('Введите последние цифры номера счетчика ')
    check_number = check_number_meter(meter_number, filename)

def check_number_meter(number, filename):
    main_list = read_cvs(filename)
    for number_line in range(len(main_list)):
        print(number_line)
        list = read_list(main_list[number_line], 0)
        print(list.split(' '))
        print(list.split(' ')[1])
        if list.split(' ')[1].endswith(number):
            return print('Такой счетчик есть'), print(number_line)
        else:
            print('Такого счетчика нет')
            continue

def date_today():
    '''Func that returned today date'''
    today = datetime.date.today()
    print('Сегодня ' + str(today))
    return today

def meters_data_for_print(filename):
    '''Function that returns a text with datas for print or email'''
    meters_data_for_print = ""
    for list in read_cvs(filename):
        meters_data_for_print += list[0] + '\n'
    print('Данные подготовлены для записи/отправки')
    return meters_data_for_print

def send_notification(text):
    email = ['ryabovd@outlook.com']
    with open('settings.json', 'r', encoding='utf-8') as file:
        settings = json.load(file)
        sender = settings["sender"]
        sender_password = settings["sender_password"]
    mail_lib = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    mail_lib.login(sender, sender_password)
    for to_item in email:
        msg = 'From: %s\r\nTo: %s\r\nContent-Type: text/plain; charset="utf-8"\r\nSubject: %s\r\n\r\n' % (
            sender, to_item, 'Показания приборов учета на {}'.format(date_today()))
        msg += text
        mail_lib.sendmail(sender, to_item, msg.encode('utf8'))
    print('Данные отправлены')
    mail_lib.quit()

if __name__ == "__main__":
    main()

"""
meters_datas.csv structure (from left to right):
personal account number
meter number
meter data (sep. is - ',')
date of update data
date of send's data)
"""

# Write func for check number meter