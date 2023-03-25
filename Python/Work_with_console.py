# -*- coding: utf-8 -*-

from sys import platform
import os,stat
import subprocess

# little info:
# cwd == current work directory

def code_dir():                                                 # return directory with this script
    return os.path.dirname(os.path.realpath(__file__))                  

def CodeInfo (dir = os.path.dirname(os.path.realpath(__file__)) ):                              # info about files in code directory
    code_direcroty = os.path.dirname(os.path.realpath(__file__)) 
    cwd = os.path.abspath(os.curdir)
    files_in_dir = os.listdir(dir)
    
    print("- Code directory:", code_direcroty)
    print("- Current work directory:", cwd)
    print("- Files in", dir, ":", files_in_dir) 

def create_py_file_examle(pyfile_name = ".demo.py"):            # create py file for demonstrate how we call it
    pyfile = open(pyfile_name, "w")
    pyfile.write("print(\"You can run any files!\")")
    pyfile.close()

def create_scr_mac(script_file = ".script.sh", pyfile_name = ".demo.py"):       # creation script for macOS .sh
    f = open(script_file,"w")
    script = "pwd>>$1\nwhoami>>$1\npython3 " + pyfile_name

    f.write(script)
    f.close()

def work_linux():
	print("\nScript working in Linux.")

def work_mac(script_file = ".script.sh", file_to_write = ".result.txt"):
    print("\nScript working in macOS.")
    try:
        create_py_file_examle()
        create_scr_mac(script_file)
        os.chmod(script_file, 0o777)
        subprocess.run("./"+script_file+" "+file_to_write, text = True, shell=True)		
        # os.chflags(dname+"/"+script_file, 0)                                          # read in Google
        # os.chflags(script_file, stat.UF_IMMUTABLE)                                    # read in Google
    except:
        print("\n!!! Some errors with runnig script:", script_file)

def work_win():
	print("\nScript working in Windows.")


#------------------names of files-------------------------
file_to_write = ".result.txt"     
script_file = ".script.sh"
pyfile_name = ".demo.py"
#---------------------------------------------------------

if __name__ == "__main__":
    print("Work with console.")
    
    # ---------------------change cwd---------------------
    decision = input("For creation new directory for demonstration code print 'Yes', else print nothing: ")
    
    dname = code_dir()
    if decision in ['Yes','yes','y']:
        newCWD = ".HereIsScriptsAndResults"                     # new cwd
        newCWD = dname + "/" + newCWD
        try:
            os.mkdir(newCWD)                                    # create new directory
        except:
            pass
        os.chdir(newCWD)                                        # change cwd
    else:
        newCWD = dname
        os.chdir(newCWD)                                        # change cwd
    
    CodeInfo()
    
    # ---------------------define OS----------------------
    if platform == "linux" or platform == "linux2":             # OS is Linux
        work_linux()            # создаю скрипт для сканирования инфы
    elif platform == "darwin":                                  # OS is MACOS
        work_mac()
        # os.remove(dname+"/"+script_file)
    elif platform == "win32":                                   # OS is Windows
        work_win()
