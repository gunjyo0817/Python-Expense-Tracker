# /usr/bin/env python3
# 111062116_許伊辰

import os,sys

class Record:
    """Represent a record."""
    def __init__(self, category , description , amount):
        """Initialize the Record with category, description, and amount"""
        self._category = category
        self._description = description
        self._amount = amount

    @property
    def category(self):
        return self._category
    @property
    def description(self):
        return self._description
    @property
    def amount(self):
        return self._amount

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        """We will read from 'records.txt' or prompt for initial amount of money."""
        records = []
        try:
            fh = open('records.txt','r')

            # Read initial_money and records
            initial_money = fh.readline()
            records = [i.rstrip('\n') for i in fh.readlines()]
            records = [tuple(i.split()) for i in records]
            fh.close()

            # Check if records.txt is empty
            if(initial_money == '' and len(records) == 0):
                sys.stderr.write('records.txt is empty.\n')
                initial_money = input('How much money do you have?  ')
                try:
                    initial_money = int(initial_money)
                except:
                    print('Invalid value for money. Set to 0 by default.')
                    initial_money = 0

            # Read initial_money and check if it's a number
            try:
                initial_money = int(initial_money)
            except:
                raise ValueError

            # Read previous records and check if they match the format  
            for items in records:
                if(len(items) != 3 or items[2].lstrip('-').isdigit() == False):# or is_category_valid(items[0],categories)==False):
                    raise ValueError

            print('Welcome back!')

        except ValueError:
            sys.stderr.write('Invalid format in records.txt. Deleting the contents.\n')
            records = []
            initial_money = input('How much money do you have?  ')
            try:
                initial_money = int(initial_money)
            except:
                print('Invalid value for money. Set to 0 by default.')
                initial_money = 0

        except FileNotFoundError:
            initial_money = input('How much money do you have?  ')
            try:
                initial_money = int(initial_money)
            except:
                print('Invalid value for money. Set to 0 by default.')
                initial_money = 0

        except PermissionError:
            sys.stderr.write('We have no permission to read records.txt, please change it to readable and run our program again.\n')
            os._exit(0)

        self._records = [Record(i[0],i[1],i[2])for i in records]
        self._money = initial_money

    def add(self, record , categories):
        """Add some expense or income records with categories,description and amount:
            cate1 desc1 amt1, cate2 desc2 amt2,  ..., caten descn amtn
            category description amoount separate by space
            each of record separate by comma
            be sure to input correct category and format"""
        record = record.split(',')
        items = [tuple(i.split()) for i in record]
        # Check if all records are valid
        errorMessage = ''
        for i in items:
            if(len(i) != 3):
                errorMessage = 'The format of records should be like this: breakfast -50, salary 3000, dinner -100'
            elif(i[2].lstrip('-').isdigit() == False):
                errorMessage = 'Invalid value for money.'
            elif(categories.is_category_valid(i[0],categories._categories)==False):
                errorMessage = 'The specified category is not in the category list.\nYou can check the category list by command "view categories".'
            if(errorMessage != ''):
                sys.stderr.write(f'    {errorMessage}\n    Fail to add the records. Please try again!\n')  
                return 

        # Update the records
        self._records += [Record(i[0],i[1],i[2]) for i in items]
        self._money += sum(int(i[2]) for i in items)
        print(f'Successfully added! Now you have {self._money} dollars')

    def view(self):
        """Print all the records and report the balance."""
        print('''
    Here's your expense and income records:
    Category        Description          Amount
    =============== ==================== ======
        ''')
        for items in self._records:
            print('    %-16s%-21s%s' % (items.category,items.description,items.amount))
        print(f'''
    ===========================================
    Now you have {self._money} dollars.
        ''')

    def delete(self, delete_record):
        """This function will allow you to delete some records.
            We will first ask you what description is going to be deleted.
            If there have mutiple records with the description.
            We will give you a list for choosing which one(or all) record(s) is going to be deleted."""
        # Check if there has anything to delete
        if(len(self._records) == 0):
            sys.stderr.write('There is nothing to delete.\n')
            return

        # delete_record should be a word
        if(len(delete_record) != 1):
            sys.stderr.write('Invalid format. Fail to delete a record\n.')
            return

        # Puts every record with description desc to deleteList
        deleteList = []
        for items in self._records:
            if(items.description == delete_record[0]):
                deleteList.append(items)

        # Check if there has no record with description desc
        if(len(deleteList) == 0):
            sys.stderr.write(f'There\'s no record with {delete_record[0]}. Fail to delete a record.\n')
            return

        # If there has only one record with description desc, then delete it directly
        elif(len(deleteList) == 1):
            self._records.remove(deleteList[0])
            self._money -= int(deleteList[0].amount)
            print(f'Successfully deleted! Now you have {self._money} dollars')
        
        # If there has more than one record with description desc, ask user which(or all) record(s) he/she whould like to delete
        else:
            print(f'''
    There are more than one {delete_record}:
    No.  Category        Description          Amount
    ===  =============== ==================== ======
            ''')
            count = 1
            for items in deleteList:
                print('    %d    %-16s%-21s%s' % (count,items.category,items.description,items.amount))
                count += 1
            print('    ===  ===========================================')

            delete_number = input(f'Which record do you want to delete?(1~{count-1}) Type all if you want to delete all records above.')

            # Delete all records with description desc
            if(delete_number == 'all'):
                for items in deleteList:
                    self._records.remove(items)
                    self._money -= int(items.amount)
                print(f'Successfully deleted! Now you have {self._money} dollars')
                return

            # Check delete_number is in correct format, and delete its corresponding record
            try:
                delete_number = int(delete_number)

                # If delete_number is not in range[1,count-1]
                if(delete_number < 1 or delete_number >= count):
                    sys.stderr.write(f'Index out of range. You should type number in [1,{count}]. Fail to delete a record.\n')
                    return 

                self._records.remove(deleteList[delete_number-1])
                self._money -= int(deleteList[delete_number-1].amount)
                print(f'Successfully deleted! Now you have {self._money} dollars')

            # If delete_number is not valid(a number or 'all')
            except:
                sys.stderr.write(f'Invalid format. You should type number in [1,{count}] or all. Fail to delete a record.\n')
        return 

    def find(self, finded_all_categories,find_category):
        """Print the records whose category is in the category or subcategories"""
        finded_all_categories = list(finded_all_categories)
        finded_list = []
        for i in finded_all_categories:
            finded_list += list(filter(lambda items : items.category==i ,self._records))
        if(len(finded_list) == 0):
            print(f'Here\'s no expense and income records under category "{find_category}"')
            return
        print(f'''
    Here's your expense and income records under category "{find_category}":
    Category        Description          Amount
    =============== ==================== ======
        ''')
        total_amount = 0
        for items in finded_list:
            print('    %-16s%-21s%s' % (items.category,items.description,items.amount))
            total_amount += int(items.amount)
        print(f'''
    ===========================================
    The total amount above is {total_amount} dollars.
        ''')  

    def save(self):
        """We will write the total money and all the records to 'records.txt'."""
        with open('records.txt','w') as fh:
            fh.write(f'{self._money}\n')
            write_records = []
            for i in range (len(self._records)):
                write_records.append(' '.join([self._records[i].category,self._records[i].description,self._records[i].amount]) + '\n')
            fh.writelines(write_records)
        print(f'Successfully saved! See you next time!')

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
 
    def view(self,categories=None,indentation=0):
        if(categories == None and indentation == 0):
            categories = self._categories
        for i in categories:
            if(type(i)==str):
                print(' '* indentation * 2 + '- ' + i) 
            else:
                self.view(i,indentation+1)
 
    def is_category_valid(self, category , categories=None):
        if(categories == None):
            categories = self._categories
        for i in categories:
            if(type(i)==type([])):
                if(self.is_category_valid(category,i)):
                    return True
            else:
                if(i==category):
                    return True
        return False
    
    def find_subcategories(self, category):
        def find_subcategories_gen(category, categories, found=False):
            """This is a generator that yields the target category and its subcategories"""
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(categories) \
                        and type(categories[index + 1]) == list:
                        for sub in categories[index + 1]:
                            yield from find_subcategories_gen(category, sub, True)
            else:
                if categories == category or found:
                    yield categories
        
        return find_subcategories_gen(category, self._categories)

# Program start!
records = Records()
categories = Categories()
while True:
    print('''
    +---+--- action menu ---+
    | 0 | add               |
    | 1 | view              |
    | 2 | delete            |
    | 3 | view categories   |
    | 4 | find (by category)|
    | 5 | exit              |
    +---+-------------------+
    ''')
    command = input('\nWhat do you want to do? (Type 0 ~ 5)  ')
    if command == '0':
        record = input('''
    Add some expense or income records with categories,description and amount:
    cate1 desc1 amt1, cate2 desc2 amt2,  ..., caten descn amtn
    category description amoount separate by space
    each of record separate by comma
    ''')
        records.add(record, categories)
    elif command == '1':
        records.view()
    elif command == '2':
        records.view()
        delete_record = input('\nWhich record do you want to delete? (Type the record\'s description Ex. salary) ').split()
        records.delete(delete_record)
    elif command == '3':
        print('Here are your categories')
        categories.view()
    elif command == '4':
        print('Here are your categories')
        categories.view()
        find_category = input('Which category do you want to find? ')
        finded_all_categories = categories.find_subcategories(find_category)
        records.find(finded_all_categories,find_category)
    elif command == '5':
        records.save()
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')