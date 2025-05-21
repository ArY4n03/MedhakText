
import customtkinter as ctk
from pathlib import Path
import pickle
import shutil
import subprocess
import os


python_path = "Python/python"
pyinstaller_path = "Python/Scripts/pyinstaller"

def destroy_topLevel(engine,win):
    win.destroy()
    engine.toplevelExists = False


def add_choicesTopLevel(engine):
    if not engine.toplevelExists:
        engine.toplevelExists = True
        tmpWindow = ctk.CTkToplevel()
        tmpWindow.geometry("300x300")
        tmpWindow.resizable(False,False)
        tmpWindow.attributes("-topmost", True)
        ctk.CTkLabel(tmpWindow,text="Choice : ").place(relx=0,rely=0.2)
        choice = ctk.CTkEntry(tmpWindow)
        choice.place(relx=0.3,rely=0.2)
        ctk.CTkLabel(tmpWindow,text="Redirect File : ").place(relx=0,rely=0.4)
        redirectFile = ctk.CTkEntry(tmpWindow)
        redirectFile.place(relx=0.3,rely=0.4)
        btn = ctk.CTkButton(tmpWindow,text="ADD",command=lambda: engine.add_choices(choice.get(),redirectFile.get(),tmpWindow))
        btn.place(relx=0.3,rely=0.7)
        tmpWindow.protocol("WM_DELETE_WINDOW",lambda: destroy_topLevel(engine,tmpWindow))
        tmpWindow.mainloop()
 
def newSceneTopLevel(engine):
    if not engine.toplevelExists:
        engine.toplevelExists = True
        tmpWindow = ctk.CTkToplevel()
        tmpWindow.geometry("300x300")
        tmpWindow.resizable(False,False)
        tmpWindow.attributes("-topmost", True)
        ctk.CTkLabel(tmpWindow,text="FileName : ").place(relx=0,rely=0.2)
        filename = ctk.CTkEntry(tmpWindow)
        filename.place(relx=0.3,rely=0.2)
        btn = ctk.CTkButton(tmpWindow,text="ADD",command=lambda: engine.CreateNewFile(filename.get(),tmpWindow))
        btn.place(relx=0.3,rely=0.7)
        tmpWindow.protocol("WM_DELETE_WINDOW",lambda: destroy_topLevel(engine,tmpWindow))
        tmpWindow.mainloop()

def appearanceTopLevel(engine):
    if not engine.toplevelExists:
        engine.toplevelExists = True
        tmpWindow = ctk.CTkToplevel()
        tmpWindow.geometry("500x300")
        tmpWindow.resizable(False,False)
        tmpWindow.attributes("-topmost", True)
        ctk.CTkLabel(tmpWindow,text="Change Theme ").place(relx=0,rely=0.2)
        filename = ctk.CTkEntry(tmpWindow)
        filename.place(relx=0.3,rely=0.2)
        btn = ctk.CTkButton(tmpWindow,text="ADD",command=lambda: engine.CreateNewFile(filename.get(),tmpWindow))
        btn.place(relx=0.3,rely=0.7)
        tmpWindow.protocol("WM_DELETE_WINDOW",lambda: destroy_topLevel(engine,tmpWindow))

def createProjectTopLevel(engine):
    if not engine.toplevelExists:
        engine.toplevelExists = True
        tmpWindow = ctk.CTkToplevel()
        tmpWindow.geometry("300x300")
        tmpWindow.resizable(False,False)
        tmpWindow.attributes("-topmost", True)
        ctk.CTkLabel(tmpWindow,text="Game Name : ").place(relx=0,rely=0.2)
        game = ctk.CTkEntry(tmpWindow)
        game.place(relx=0.3,rely=0.2)
        btn = ctk.CTkButton(tmpWindow,text="Browse Folder",command=lambda: engine.CreateNewProject(game.get(),tmpWindow))
        btn.place(relx=0.3,rely=0.7)
        tmpWindow.protocol("WM_DELETE_WINDOW",lambda: destroy_topLevel(engine,tmpWindow))
        tmpWindow.mainloop()


def create_project(dir,title):

    #create a folder with project name and create Scenes folder
    Path(dir + "/" + title + "/Scenes" ).mkdir(parents=True,exist_ok = True)
    #create settings File

    try:
        with open(dir+"/"+title+"/Settings.dat","wb") as file:
            data = {"start_scene":"","title":title,"theme":"Dark"}
            pickle.dump(data,file)

            return True
    except:
        return False


def testProject(engine):
    gameTesterPath = "Resources/" + "game_runnerTest.py"
    gamedir = engine.GameDir
    scene = engine.selected_file
    subprocess.run([python_path,gameTesterPath,gamedir,scene])

def exportProject(exportDir,engine):
    exportDir = exportDir.replace('/',os.sep) # replace / with \
    game_runner_path = Path("Resources/game_runner.py").resolve()
    #choose exort directory
    #build game_runner.py in that location
    subprocess.run([pyinstaller_path,"--onefile","--distpath",exportDir,game_runner_path])
    #after succesfull build copying Scenes folder to  exportdir
    Scenes_dir = Path(engine.GameDir + '/Scenes')
    shutil.copytree(Scenes_dir,exportDir + "/Scenes",dirs_exist_ok=True)
    settingFilePath = Path(engine.GameDir + "/Settings.dat")
    shutil.copy(settingFilePath,exportDir)
    #move the required file to dest folder
    #remove every dirctory except dest
    #rename dest directory