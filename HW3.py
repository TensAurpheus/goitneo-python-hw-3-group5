from collections import UserDict
from datetime import datetime
import re

class NumberArgsError(Exception):
    pass


def phone_validation(phone):
    if len(phone) == 10 and phone.isdigit():
        return True
    else:
        return False


# def name_error_check(func):
#     def inner(*args):
#         try:
#             return func(*args)
#         except:
#             return "Not found record with the name {name}!"
#     return inner


def birthday_error_check(func):
    def inner(*args):
        if re.search(r'\b\d{2}\.\d{2}\.\d{4}', args[1]):
            try:
                bday = datetime.strptime(args[1], '%d.%m.%Y')
                return func(*args)
            except:
                return 'Enter a valid date!'
        else:
            return "Enter birthday as DD.MM.YYYY!"
    return inner


# def check_number_arguments(args, n):
#     if len(args) != n:
#         raise NumberArgsError


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
           

class Birthday:
    def __init__(self, birthday):
        self.value = datetime.strptime(birthday, '%d.%m.%Y')
            
    def __str__(self):
        return self.value.strftime('%d.%m.%Y')


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.birthday = birthday
        
    def __str__(self):
        return (
            f"Contact name: {self.name}; " 
            f"phones: {', '.join(str(p) for p in self.phones)}; "
            f'birthday: {self.birthday}'
                )
    
    def show_phones(self):
        return f"{', '.join(str(p) for p in self.phones)}"
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    # def remove_phone(self, phone):
    #     for p in self.phones:
    #         if p.value == phone:
    #             self.phones.remove(p)

    def edit_phone(self, phone_from, phone_to):
        for p in self.phones:
            if p.value == phone_from:
                p.value = phone_to
                return 'Phone changed!'
        return f'The record for {self.name} does not contain phone {phone_from}'
        
    # def find_phone(self, phone):
    #     for p in self.phones:
    #         if p.value == phone:
    #             return p.value
    #     return "Not found"
    
    @birthday_error_check
    def add_birthday(self, birthday):
        if not self.birthday:
            self.birthday = Birthday(birthday)
            return 'Birthday added!'
        else:
            return f'Cannot add! Birthday for {self.name} is already specified!'


class AddressBook(UserDict):
    
    def add_record(self, record: Record):
        if record.name.value in self.data:
            self.data[str(record.name)].add_phone(str(record.phones[0]))
            return f'Phone added to {record.name}!'
        else:
            self.data[str(record.name)] = record
            return 'Contact added!'

    # @name_error_check
    # def find(self, name):
    #     return self.data[name]
        
    # @name_error_check
    # def delete(self, name):
    #     self.data.pop(name)
    
    def __str__(self):
        book = ''
        for name, record in self.data.items():
            book += str(record) + "\n"
        return book

    def get_birthdays_per_week(self):
        today = datetime.today().date()
        greet_dict = {}
        for user in self.data.values():
            if not user.birthday: 
                continue
            name = str(user.name)
            birthday = user.birthday.value.date()
            birthday_this_year = birthday.replace(year=today.year)
            
            difference_days = birthday_this_year - today
            difference_days = difference_days.days
                        
            if (difference_days >= 1 and difference_days <= 7):
                birthday_weekday = birthday_this_year.strftime('%A')
                if birthday_weekday in ['Saturday', 'Sunday']:
                    birthday_weekday = 'Monday'
                try:
                    greet_dict[birthday_weekday].append(name)
                except:
                    greet_dict[birthday_weekday] = [name]
        
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                    'Friday', 'Saturday', 'Sunday']
        greet_list = ''
        for weekday in weekdays:
            try:
                birthday_names = ', '.join(greet_dict[weekday])
                greet_list += f'{weekday}: {birthday_names}\n'
            except:
                continue
        if not greet_list:
            greet_list = 'Noone to greet in the next week!' 
        return greet_list


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


HELP = (
    """Phones must be 10-digit numbers, and birthday is expected as DD.MM.YYYY
add [name] [phone] - add new contact or new phone to existing contact
change [name] [old_phone] [new_phone] - change phone for a contact
phone [name] - display all phones for a contact
all - display all contacts
add-birthday [name] [birthday] - add birthday to a contact
show-birthday [name] - show birthday for a contact
hello - get a greeting
close or exit - exit the program
""")


def main():
    book = AddressBook()
    print("Welcome! Enter 'help' to see the list of commands!")
    while True:
        try:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)
            if command in ["close", "exit"] and not args:
                print("Good bye!")
                break
            if command == 'help' and not args:
                print(HELP)
            elif command == "hello" and not args:
                print("Greetings, Seeker!")
            elif command == "add":
                name, phone = args
                if phone_validation(phone): 
                    print(book.add_record(Record(name, phone)))
                else: 
                    print('Phone must be 10 digits!')
            elif command == 'change':
                name, phone_from, phone_to = args
                if phone_validation(phone_from) and phone_validation(phone_to):
                    print(book[name].edit_phone(phone_from, phone_to))
                else: 
                    print('Phone must be 10 digits!')
            elif command == 'phone':
                name, = args
                print(book[name].show_phones())
            elif command == 'all' and not args:
                print(book)
            elif command == 'add-birthday':
                name, birthday = args
                print(book[name].add_birthday(birthday))
            elif command == 'show-birthday':
                name, = args
                print(book[name].birthday)
            elif command == 'birthdays' and not args:
                print(book.get_birthdays_per_week())
            else:
                print("Invalid command.")
        except KeyError:
            print('No such name in the book!')
        except ValueError:
            print('Wrong syntax!')


if __name__ == "__main__":
    main()
