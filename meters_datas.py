import csv
import datetime
import smtplib
import json
import sys
import argparse

"""
meters_datas.csv structure (from left to right):
personal account number
meter number
meter data (sep. is - ',')
date of update data
date of send's data)
"""

def main():
    filename = "meters_datas"
    dict_params = get_params()
    if len(dict_params) != 0:
        if len(dict_params['change']) != 0:
            list_changes = dict_params['change']
            for i in range(len(list_changes) // 2):
                meter_number = list_changes[i*len(list_changes) // 2]
                meter_data = list_changes[i*len(list_changes) // 2 + 1]
                index, line = check_number_meter(meter_number, filename)
                line[2], line[3] = meter_data, str(date_today())
                data, filename_with_date = write_line_csv(index, line, filename)
                write_csv(filename, data)
                write_csv(filename_with_date, data)
                print('показания обновлены из аргументов')

    datas = read_cvs(filename)
    #print(datas)
    print("Сегодня " + str(date_today()) + "\n")
    #print(meters_data_for_print(filename))
    while True:
        choice = menu()
        if choice == '1':
            index, line = update_meter_data(filename)
            data, filename_with_date = write_line_csv(index, line, filename)
            write_csv(filename, data)
            write_csv(filename_with_date, data)
            continue
        elif choice == '2':
            #print('Func that send email')
            text = meters_data_for_print(filename)
            #print(text)
            send_notification(text)
            continue
        elif choice == '3':
            print('Func to add new meter')
        elif choice == '0':
            print("THE END")
            break
        else:
            continue   

def get_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--change', nargs='*', help='change meter data')
    args = parser.parse_args()
    #print(len(args.change))
    #print('***', args.change)
    if len(args.change) % 2 == 0:
        change_dict = {}
        change_dict['change'] = args.change
        #print('*', change_dict)
        return change_dict
 
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
    print("МЕНЮ\n\n")
    print("1 - ОБНОВИТЬ показания")
    print("2 - ОТПРАВИТЬ показания по email")
    print("3 - ДОБАВИТЬ НОВЫЙ счетчик")
    print("0 - ВЫХОД")
    return input()

def update_meter_data(filename):
    print('Будем обновлять показания счетчика')
    meter_number = input('Введите последние цифры номера счетчика или NO для выхода: ')
    if meter_number == 'NO':
        print('Выход из программы')
        quit()
    else:
        index, line = check_number_meter(meter_number, filename)
        #data = read_cvs(filename)
        #data[index] = line
        print(f'Обновляем данные счетчика {line[1]} \nПоследние показания {line[2]}')
        #print(line)
        meter_data = input('Введите показания счетчика с запятой: ')
        #Обновляем данные счетчика
        line[2], line[3] = meter_data, str(date_today())
        #print(line)
        return index, line

def check_number_meter(number, filename):
    main_list = read_cvs(filename)
    for number_line in range(len(main_list)):
        #print(number_line)
        list = read_list(main_list[number_line], 0)
        #print(list.split(' '))
        #print(list.split(' ')[1])
        if list.split(' ')[1].endswith(number):
            #print('Такой счетчик есть'), print(number_line)
            return number_line, list.split(' ')
        else:
            print('Такого счетчика нет')
            continue

def date_today():
    '''Func that returned today date'''
    today = datetime.date.today()
    return today

def write_line_csv(index, line, filename):
    '''Func that write csv file with meters datas'''
    data = read_cvs(filename)
    data[index] = [(' ').join(line)]
    #print(data)
    today_date = str(date_today())
    filename_with_date = today_date + ' meters_datas'
    #meters_datas_list = data.split('\n')
    return data, filename_with_date
    
def write_csv(filename, data):
    filename += '.csv'
    with open(file=filename, mode="w", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerows(data)

def meters_data_for_print(filename):
    '''Function that returns a text with datas for print or email'''
    meters_data_for_print = ""
    for list in read_cvs(filename):
        meters_data_for_print += (' ').join(list[0].split()[:3]) + '\n'
    print('Данные подготовлены для записи/отправки')
    return meters_data_for_print

def send_notification(text):
    #email = ['ryabovd@outlook.com']
    email = ['pokazvodokanal@mail.ru']
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
    print('Данные отправлены на ' + email[0].upper())
    # Дописать функцию изменения строки с датой отправки
    mail_lib.quit()

if __name__ == "__main__":
    main()

# Наладить работу без параметров
# Удалить отладку из функции поиска счетчика
# Написать функцию записи даты передачи показаний
# Определить как работать: немедленная запись каждого измения в файл или работать в оперативной памяти или запись во временный файл изменений
# Дополнить меню пунктом просмотра показаний с датами передачи
# Улучшить возможность чтения из командной строки. Для ввода нескольких счетчиков с показаниями
# Написать исключение для отслеживания ошибки неправильного номера счетчика
# Написать функцию проверки показиний, чтобы не записывать показания меньше текущих
