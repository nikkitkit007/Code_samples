import os
import csv


class TextFile(object):
    def __init__(self, file_name):
        self.file_name = file_name
        try:
            file = open(file_name, "r")
            file.close()
            print("File \"%s\" was opened"%(file_name))
        except:
            file = open(file_name, "w")
            file.close()
            print("File \"%s\" was created"%(file_name))
        pass

    def delete_file(self):                          # delete created file
        try:
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), self.file_name)
            os.remove(path) 
        except:
            print("File %s not found"%(self.file_name))         

    def delete_data_in_file(self):                  # clear file
        file = open(self.file_name, "w")
        file.close()

    def add_to_file(self, text):                    # adding text to file
        file = open(self.file_name, "a")
        
        if type(text) == str:
            file.write(text)
        elif type(text) == list:
            for line in text:
                file.write(str(line))

        file.close()
    
    def set_new_data_in_file(self, data):           # clear data in file and write new data
        file = open(self.file_name, "w")

        if type(data) == str:
            file.write(data)
        elif type(data) == list:
            for line in data:
                file.write(str(line))

        file.close()
    
    def read_file_by_lines(self):                   # read all data from file by lines
        file = open(self.file_name, "r")
        lines = file.readlines()
        file.close()
        return lines
    
    def real_all_file(self):                        # read all data from file as text
        file = open(self.file_name, "r")
        data = file.read()
        file.close()
        return data

class CsvFile(TextFile):
    def csv_get_atts(self):                                 # return table atts 
        with open(self.file_name, "r") as f_obj:
            reader = csv.reader(f_obj)
            mass_atts = []

            for row in reader:
                mass_atts = row
                break
        return mass_atts

    def read_csv_to_dict(self, mass_atts):                  # return return dictionary 
        with open(self.file_name, "r") as f_obj:
            f_obj.seek(0)                                   # it's need to correct DictReader

            dict_data = {}
            reader = csv.DictReader(f_obj, delimiter=',')
            
            for att in mass_atts:
                dict_data[att] = []

            for line in reader:                             # fill dict                    
                for att in mass_atts:
                    dict_data[att].append(line[att])
        
        return(dict_data)
    

text_to_test = "First line!\nSecond line?\nNice\n"
text_file_name = "test_file.txt"
csv_name = "mycsv.csv"

mass =  [1,2,4,5]

instuct_for_text_file_test = "Write: \n0 to see instruction;\n1 to add; \n2 to rewrite file;\n3 to read by lines;\n4 to read all data in file\n5 to print data from file;\n6 to delete all data in file;\n7 to delete file.\n"
instuct_for_csv_file_test = "Write: \n0 to see instruction;\n1 to get mass with atts;\n2 to get dictionary from csv\n"

if __name__ == "__main__":

    what_do = int(input("1 to Test text file;\n2 to Test table\n"))

    if what_do == 1:                                    # Test text file
        f1 = TextFile(text_file_name)
        print(instuct_for_text_file_test)
        while 1:                                        # program work parth
            order = int(input("- Input order: "))
            if order == 0:
                print(instuct_for_text_file_test)

            elif order == 1:
                f1.add_to_file(text_to_test)

            elif order == 2:
                data = f1.set_new_data_in_file(text_to_test)

            elif order == 3:
                data = f1.read_file_by_lines()

            elif order == 4:
                data = f1.real_all_file()

            elif order == 5:
                print(data)
            
            elif order == 6:
                f1.delete_data_in_file()
            
            elif order == 7:
                f1.delete_file()

    elif what_do == 2:                                  # Test csv file
        t1 = CsvFile(csv_name)
        print(instuct_for_csv_file_test)
        while 1:                                        # program work parth
            order = int(input("- Input order: "))
            
            if order == 0:
                print(instuct_for_csv_file_test)
            
            elif order == 1:
                atts = t1.csv_get_atts()
                print(atts)
            
            elif order == 2:
                atts = t1.csv_get_atts()
                dict_csv = t1.read_csv_to_dict(atts)
                print(dict_csv)

