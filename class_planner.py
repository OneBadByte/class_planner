#!/usr/bin/python3

import os
import json
from pathlib import Path
from datetime import date
from datetime import timedelta

class SystemData:
    system_data = {
            #users last used file
            "lastSaveFile": "",
            }
    #File the system will be using
    SYSTEM_FILE = "system.json"
    
    def load_system_file(self):
        """loads the system file"""
        system_file = open(self.SYSTEM_FILE, 'r')
        file_data = str(system_file.read())
        self.system_data = json.loads(file_data)
    
    def write_system_file(self, file_name):
        """writes the system file to current location"""
        system_file = open(file_name, 'w')
        json_data = json.dumps(self.system_data)
        system_file.write(json_data)

    def check_for_system_file(self):
        """looks for system file or it will create one"""
        if not Path(self.SYSTEM_FILE).exists():
            self.write_system_file(self.SYSTEM_FILE)
        else:
            self.load_system_file()

    def change_last_save(self, file_name):
        """changes the default user save filee"""
        self.system_data["lastSaveFile"] = file_name
        self.write_system_file(self.SYSTEM_FILE)

#-------------------------------------------------------------------------------------------------------
class ClassPlanner:

    
    class_data = {
            "className": "",
            "daysLeft": 0,
            "chapterNumberList": [],
            "chapterLengthTotal": 0,
            "chaptersFinished": [],
            "chaptersLeft": 0,
            "saveFile": "",
            "endDate":{
                "year": 2019,
                "month": 1,
                "day": 26,
                }
            }

    def calculate_days_left(self):
        year = self.class_data["endDate"]["year"]
        month = self.class_data["endDate"]["month"]
        day = self.class_data["endDate"]["day"]
        end_date = date(year, month, day)
        today = date.today() + timedelta(days=1)
        days_left = str(end_date - today).split(" ")
        days_left[2] 
        return ' '.join(days_left[:2])


    def load_user_file(self, file_name):
        """loads the users save file"""
        user_file = open(file_name, 'r')
        file_data = str(user_file.read())
        self.class_data = json.loads(file_data)
    
    def write_user_file(self, file_name):
        """writes the users save file"""
        user_file = open(file_name, 'w')
        json_data = json.dumps(self.class_data)
        user_file.write(json_data)

#-------------Getters and setters of the ClassPlanner--------------------------------------------------
    def get_save_file(self):
        """gets the name of users save file"""
        return self.class_data["saveFile"]
    
    def set_save_file(self, file_name):
        """sets the name of users save file"""
        self.class_data["saveFile"] = file_name
    
    def get_chapter_number_list(self):
        return self.class_data["chapterNumberList"]
    
    def set_chapter_number_list(self, chapter_number_list):
        self.class_data["chapterNumberList"] = chapter_number_list
    
    def get_class_name(self):
        return self.class_data["className"]

    def get_chapter_length_list(self):
        return self.class_data["chapterLengthList"]

    def get_chapters_left(self):
        return self.class_data["chaptersLeft"]

    def get_days_left(self):
        return self.class_data["daysLeft"]
    
    def get_chapter_length_total(self):
        total = 0
        for x in self.get_chapter_length_list():
            total = total + x
        return total
    
    def set_class_name(self, name):
        self.class_data["className"] = name

    def set_days_left(self, days):
        self.class_data["daysLeft"] = days

    def set_chapters_left(self, chapters):
        self.class_data["chaptersLeft"] = chapters

    def set_chapter_length_list(self, length_list):
        self.class_data["chapterLengthList"] = length_list

    def set_chapter_length_total(self, total):
        self.class_data["chapterLengthTotal"] = total

    def set_end_date(self, day, month, year):
        """sets the classPlanners end date"""
        self.class_data["endDate"]["year"] = year
        self.class_data["endDate"]["month"] = month
        self.class_data["endDate"]["day"] = day
#-------------------------------------------------------------------------------------------------------

#-----------------------------main functions of the ClassPlanner----------------------------------------
    def create_class_plan(self):
        """creates a plan file with user data"""
        self.set_class_name(input("what is the class name?: "))

        year = (int(input("whats the end dates year?: ")))
        month = (int(input("whats the end dates month?: ")))
        day = (int(input("whats the end dates day?: ")))
        self.set_end_date(day, month, year)

        self.set_chapters_left(int(input("how many chapters are there?: ")))

        # adds chapter numbers to the chapter_number_list
        chapter_number_list = []
        for x in range(self.get_chapters_left()):
            chapter_number_list.append(x+1)
        self.set_chapter_number_list(chapter_number_list)

        # adds chapter lengths to a list. the user provides the data
        chapter_length_list = []
        counter = 1
        for x in range(self.get_chapters_left()):
            progress_string = "chapter length is?({}/{}): ".format(x+1, self.get_chapters_left())
            chapter_length_list.append(int(input(progress_string)))
        self.set_chapter_length_list(chapter_length_list)

        # calculates the chapter_length_list into a total
        self.set_chapter_length_total(self.get_chapter_length_total())

        # creates a save file for the user and adds file_name to class_data
        file_name = input("name of new file?: ")
        self.set_save_file(file_name)
        self.write_user_file(file_name)
        print("done")

    #TODO is this needed?
    def chapter_length_list_total(self):
        total = 0
        for x in self.get_chapter_length_list():
            total = total + x
        self.set_chapter_length_total(total)

    def get_chapter_day_avg(self):
        """caculates how much work needs done each day"""
        return int((self.get_chapter_length_total()/self.get_days_left())) + 1

    def average_calculator(self):
        """prints out how much work needs to be done"""
        total_to_be_minused = 0
        counter = 0
        for x in self.get_chapter_length_list():
            math = int((self.get_chapter_length_total() - total_to_be_minused) / self.get_days_left()) + 1
            print("chapter: {} read will average to: {}".format(self.get_chapter_number_list()[counter], math))
            total_to_be_minused = total_to_be_minused + x
            counter = counter + 1

    def day_planner(self):
        """creates a day plan using data from class_data"""
        day = 1
        # gets the average work needed each day
        avg_work_needed = self.get_chapter_day_avg()
        total_chapters = self.get_chapters_left()

        # gets the chapter length list and number list
        chapter_length_list = self.get_chapter_length_list()
        chapter_number_list = self.get_chapter_number_list()

        #these are used as placeholders for when length is bellow avg
        chapter_number_holder = []
        chapter_length_holder = []

        for chapter_iterator in range(len(chapter_length_list)):
            #used to calculate the total chapter length
            collective_chapter_length = chapter_length_list[chapter_iterator]
            #print string that prints the collected chapter numbers
            chapter_number_print_string = ""

            if chapter_number_holder != []:
                for iterator in range(len(chapter_number_holder)):
                    # adds a stored chapter length to the total chapter length
                    collective_chapter_length = collective_chapter_length + chapter_length_holder[iterator]
                    # adds a stored chapter number to the print string
                    chapter_number_print_string = chapter_number_print_string + " " + str(chapter_number_holder[iterator])

            # checks if chapter length is greater than or that chapter_iterator is at the end
            if collective_chapter_length >= avg_work_needed or chapter_iterator == total_chapters-1:
                chapter_number_print_string = chapter_number_print_string + " " + str(chapter_number_list[chapter_iterator])
                print("day {} read chapters {}".format(day, chapter_number_print_string))
                # only changes the day when a day is printed out
                day = day + 1
                #resets the chapter holders
                chapter_length_holder = []
                chapter_number_holder = []
            else:
                # adds to the chapter holders
                chapter_length_holder.append(chapter_length_list[chapter_iterator])
                chapter_number_holder.append(chapter_number_list[chapter_iterator])
        add_spaces(2) 
                
        

#-------------------------------------------------------------------------------------------------------

def add_spaces(number):
    """adds spaces to the terminal"""
    for x in range(number):
        print("")



#-------------------------------------------------------------------------------------------------------

# Objects ahoy!
classPlanner = ClassPlanner()
system = SystemData()

# checks for a system file
system.check_for_system_file()

# prints logo and welcome message
os.system("cat class_planner_logo.txt")
print("welcome to the class planner!")

# gets the default user save file
last_user_file = system.system_data["lastSaveFile"]
if last_user_file != "":
    # loads the user file into the classPlanners class_data
    classPlanner.load_user_file(last_user_file)
    #prints data from the save file
    print("class: {}\ndays left: {}\nchapters left: {}".format(
        classPlanner.get_class_name(),
        classPlanner.calculate_days_left(),
        classPlanner.get_chapters_left()
        ))
    add_spaces(10)

# infinite loop of destruction!!!
while True:
    # print messages for all of the user options and the code that prints it
    user_commands = [
            "see day plan 1",
            "see average calculator 2",
            "create class plan 3",
            "save plan file? 4",
            "load plan file? 5",
            "press anything else to quit"
            ]
    for x in user_commands:
        print(x)

    # lets the user press any key without exploding    
    try:
        user_input = int(input("what do you want to do?: "))
        add_spaces(2)

        # Actions that will happen from the users input

        #loads user file
        if user_input == 3:
            file_name = input("what is the file name? ")
            classPlanner.load_user_file(file_name)
            system.change_last_save(file_name)
        #saves user file
        elif user_input == 2:
            if classPlanner.class_data["saveFile"] == "":
                file_name = input("what is the file name? ")
                classPlanner.write_user_file(file_name)
                classPlanner.class_data["saveFile"] = file_name
                system.change_last_save(file_name)
            else:
                classPlanner.write_user_file(classPlanner.class_data["saveFile"])
        #calculates day planner for the user
        elif user_input == 1:
            classPlanner.day_planner()
        #calculates avg work for the user
        elif user_input == 2:
            print("total chapter length is: {}".format(classPlanner.chapter_length_list_total()))
            classPlanner.average_calculator()
        #creates a user file for the user
        elif user_input == 5:
            classPlanner.create_class_plan()
        # exits the program nicely
        else:
            system.change_last_save(classPlanner.get_save_file())
            break
    except Exception as e:
        # exits the program not nicely
        system.change_last_save(classPlanner.get_save_file())
        break


