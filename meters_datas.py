import csv
import datetime
import smtplib
import json


def main():
    filename = "meters_datas"
    datas = read_cvs(filename)
    print(datas)
    print(date_today())
    #print(meters_data_for_print(filename))
    choice = menu()
    if choice == '1':
        index, line = update_meter_data(filename)
        write_line_csv(index, line, filename)

        choice == menu()
    elif choice == '2':
        text = meters_data_for_print(filename)
        send_notification(text)
    elif choice == '3':
        print('Func to add new meter')
    else:
            while choice not in '123':
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

def read_list(list, index):
    '''Func get list and return index element string'''
    return list[index]

def menu():
    print("МЕНЮ\n\n1 - ОБНОВИТЬ показания\n2 - ОТПРАВИТЬ показания по email\n3 - ДОБАВИТЬ НОВЫЙ счетчик")
    return input()

def update_meter_data(filename):
    print('Будем обновлять показания счетчика')
    meter_number = input('Введите последние цифры номера счетчика: ')
    index, line = check_number_meter(meter_number, filename)
    #data = read_cvs(filename)
    #data[index] = line
    print('Нужно обновить строку')
    print(line)
    meter_data = input('Введите показания счетчика с запятой: ')
    #Обновляем данные счетчика
    line[2], line[3] = meter_data, str(date_today())
    print(line)
    return index, line

def check_number_meter(number, filename):
    main_list = read_cvs(filename)
    for number_line in range(len(main_list)):
        #print(number_line)
        list = read_list(main_list[number_line], 0)
        print(list.split(' '))
        print(list.split(' ')[1])
        if list.split(' ')[1].endswith(number):
            print('Такой счетчик есть'), print(number_line)
            return number_line, list.split(' ')
        else:
            print('Такого счетчика нет')
            continue

def date_today():
    '''Func that returned today date'''
    today = datetime.date.today()
    print('Сегодня ' + str(today))
    return today

def write_line_csv(index, line, filename):
    '''Func that write csv file with meters datas'''
    data = read_cvs(filename)
    data[index] = [(' ').join(line)]
    print(data)
    today_date = str(date_today())
    filename = today_date + ' meters_datas' + '.csv'
    #meters_datas_list = data.split('\n')
    with open(file=filename, mode="w", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=' ')
        for list in data:
            line = list[0].split()
            writer.writerow(line)

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