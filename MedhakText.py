#This file will convert game_runner.py to a exe file
import customtkinter as ctk
import tkinter as tk
from customtkinter import filedialog
from tkinter import messagebox as msg
import Resources.engine_utils as eu
import Resources.utils as ut

class YourTale:
    
    def __init__(self,master):
        self.master = master
        self.master.geometry("1200x700")
        self.master.title("Your Tale")
        self.GameDir = ""
        self.toplevelExists = False
        self.selected_file = ""
        self.selected_fileIndex = 0
        self.GameSettings = {"start_screen":"","title":""}

        self.Menu = tk.Menu(self.master)

        self.FileMenu = tk.Menu(self.Menu,tearoff=0)
        self.FileMenu.add_cascade(label="Create Project",command= lambda: eu.createProjectTopLevel(self) )
        self.FileMenu.add_cascade(label="Open Project Folder",command=self.OpenNewFolder)
        self.FileMenu.add_command(label="New Scene(Ctrl + N)",command= lambda: eu.newSceneTopLevel(self))
        self.FileMenu.add_command(label="Save Scene(Ctrl + S)",command=self.save_sceneFile)
        self.FileMenu.add_command(label="Export Project",command=self.chooseDir)

        self.EngineSettings = tk.Menu(self.Menu,tearoff=0)
        self.EngineSettings.add_command(label="Appearance",command=self.save_sceneFile)
        #self.EngineSettings.add_command(label="Themes",command=self.save_sceneFile)


        self.Other = tk.Menu(self.Menu,tearoff=0)
        self.Other.add_command(label="About",command= lambda: self.OtherTabContent("About"))
        self.Other.add_command(label="Version",command= lambda: self.OtherTabContent("Version"))

        self.Menu.add_cascade(label="File",menu=self.FileMenu)
        self.Menu.add_cascade(label="Engine Settings",menu=self.EngineSettings)
        self.Menu.add_cascade(label="Other",menu=self.Other)
        self.master.configure(menu=self.Menu)


        #Frames
        self.startupFrame = ctk.CTkFrame(self.master)
        self.startupFrame.place(relwidth=1,relheight=1)

        self.MainFrame = ctk.CTkFrame(self.master)
        self.MainFrame.place(relwidth=1,relheight=1)

        self.MainFrame.tkraise()
        #Tabs
        self.tabview = ctk.CTkTabview(master=self.MainFrame)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.tabview.add("Editor")
        self.tabview.add("Settings")

        #what the code below does is basically whenever tab changes self.on_tab_change() is called
        self.tabview._segmented_button._command = self.on_tab_change

        # Access individual tabs like frames and add widgets
        self.EditorTab = self.tabview.tab("Editor")
        self.SettingsTab = self.tabview.tab("Settings")

        self.loaded_tabs = {"Editor":False,"Settings":False}

        self.on_tab_change("Editor")

    def Editor_tab(self):
        #Editor
        self.textarea = ctk.CTkTextbox(self.EditorTab) #this is where user enters the text content
        self.textarea.place(relx = 0.1,rely=0.05,relwidth= 0.8,relheight=0.5)

        self.testBtn = ctk.CTkButton(self.EditorTab,text="Test",command=lambda : eu.testProject(self))
        self.testBtn.place(relx=0.9,rely=0)

        ###Creating a frame for scene file manager ###
        self.fileManagerFrame = ctk.CTkFrame(self.EditorTab)
        self.fileManagerFrame.place(relx=0.05,rely=0.6,relwidth=0.3)
        
        self.FileList = tk.Listbox(self.fileManagerFrame)
        self.FileList.place(relx=0.2,rely=0.2,relwidth=0.6)

        #ScrollBar for File(Scene Files) list
        self.ScrollBarFile = ctk.CTkScrollbar(self.fileManagerFrame)
        self.ScrollBarFile.place(relx=0.8,rely=0.2)

        self.FileList.configure(yscrollcommand=self.ScrollBarFile.set)
        self.ScrollBarFile.configure(command=self.FileList.yview)

        ###Creating a frame to hold listbox###
        self.ListFrame = ctk.CTkFrame(self.EditorTab)
        self.ListFrame.place(relx =0.3,rely=0.6,relwidth =0.8)

        self.ChoiceList = tk.Listbox(self.ListFrame)
        self.ChoiceList.place(relx=0.1,rely=0.2,relwidth=0.5)

        #ScrollBar for choice list
        self.ScrollBar = ctk.CTkScrollbar(self.ListFrame)
        self.ScrollBar.place(relx=0.61,rely=0.2)

        self.ChoiceList.configure(yscrollcommand=self.ScrollBar.set)
        self.ScrollBar.configure(command=self.ChoiceList.yview)

        self.addOptionBtn = ctk.CTkButton(self.ListFrame,text="Add Choice",command= lambda: eu.add_choicesTopLevel(self))
        self.addOptionBtn.place(relx=0.65,rely=0.3)

        self.removeOptionBtn = ctk.CTkButton(self.ListFrame,text="Remove Choice",command=self.remove_choices)
        self.removeOptionBtn.place(relx=0.65,rely=0.5)

        self.ShowOptionBtn = ctk.CTkButton(self.ListFrame,text="Show Choice",command=self.choice_info)
        self.ShowOptionBtn.place(relx=0.65,rely=0.7)

        #binding selection event to Filelist
        self.FileList.bind("<<ListboxSelect>>",self.update_editor)
    
    def Settings_Tab(self):
        self.startsceneLabel = ctk.CTkLabel(self.SettingsTab, text="Start Scene :",font=(None,30)).place(relx = 0.1,rely=0.3)
        self.startsceneEntry = ctk.CTkEntry(self.SettingsTab,font=(None,30),width=400)
        self.startsceneEntry.place(relx=0.4,rely=0.3)

        self.TitleLabel = ctk.CTkLabel(self.SettingsTab, text="Start Scene :",font=(None,30)).place(relx = 0.1,rely=0.5)
        self.TitleEntry = ctk.CTkEntry(self.SettingsTab,font=(None,30),width=400)
        self.TitleEntry.place(relx=0.4,rely=0.5)

        self.updateBtn = ctk.CTkButton(self.SettingsTab,font=(None,30),text="Update",command= lambda: ut.update_gameSettings(self))
        self.updateBtn.place(relx =0.3,rely =0.7 )
        
    
    def on_tab_change(self,tabname): #this function is called everytime a tab is changed
        if not self.loaded_tabs[tabname]:
            self.loaded_tabs[tabname] = True
            self.load_tab_content(tabname) #if tab is opened first time then only tab will load

        self.tabview.set(tabname)

    
    def load_tab_content(self,tab="Editor"):
        match tab:
            case "Editor":
                    self.Editor_tab()
            case "Settings":
                    self.Settings_Tab()

    #adds choices in choice list
    def add_choices(self,choice,redirectFile,win):
        self.ChoiceList.insert(tk.END,f"{choice}->{redirectFile}")
        win.destroy()
        self.toplevelExists = False

    #removes choices from choice list
    def remove_choices(self):
        try:
            ch = self.ChoiceList.curselection()[0]
            self.ChoiceList.delete(ch)
        except:
            msg.showerror(message="Please select a choice",title="Error")


    #gives info like choice and scene you will be redirected to when you select that choice
    def choice_info(self):
        try:
            ch = self.ChoiceList.curselection()[0]
            info = self.ChoiceList.get(ch).split("->")
            msg.showinfo(message=f"Choice - {info[0]}\nFile - {info[1]}",title="Choice Info")

        except Exception as e:
            msg.showerror(message="Please select a choice",title="Error")

    #Updates editor everytime a file is selected
    def update_editor(self,*args):

        '''
        This function will run everytime a file is selected in FilelistBox 
        But if I selected something in ChoiceListBox after selecting something in FileListBox this function is called again
        because Even if you click on ChoiceList, self.FileList.curselection() will still return 
        the previously selected index, so update_editor acts like it was triggered again — even though it wasn't!

        so to fix that I created a self.selected_fileIndex which holds the index of the file selected

        so everytime this function will run self.selected_fileIndex will hold the index of currently selected item only
        when length of self.FileList.curselection() is 0 
        '''

        self.selected_fileIndex = self.FileList.curselection()[0] if len(self.FileList.curselection()) > 0 else self.selected_fileIndex
        if self.selected_file != self.FileList.get(self.selected_fileIndex): 

            self.selected_file = self.FileList.get(self.selected_fileIndex)
            
            with open(ut.scene_path(self.GameDir,self.selected_file),"r") as file:
                content = file.read()
            
                try:
                    story_text = content[(content.index("%text%") + 6) : content.index("/text/")]
                    self.update_textArea(story_text)

                    choices = content[(content.index(r"%choice%") + 8) : content.index("/choice/")].strip().split("*end*")
                    choices = [choice for choice in choices if choice != '']
                    redirect_files = content[(content.index(r"%redirect%") + 10) : content.index("/redirect/")].strip().split("*end*")
                    redirect_files = [redirect_file for redirect_file in redirect_files if redirect_file != '']

                    self.update_choices([f"{x}->{y}" for x,y in zip(choices,redirect_files)])
                except Exception as e:
                    msg.showerror(title="Error",message="Failed to load scene files")

    def update_textArea(self,text):
        self.textarea.delete(1.0,tk.END)
        self.textarea.insert(1.0,text)
        
    def update_choices(self,choices):
        self.ChoiceList.delete(0,tk.END)
        for choice in choices:
            self.ChoiceList.insert(tk.END,choice.strip())

    def save_sceneFile(self):
        if self.selected_file != "" and self.GameDir != "":
            with open(ut.scene_path(self.GameDir,self.selected_file),"w") as file:
                file.write("%text% \n")
                file.write(self.textarea.get(1.0,tk.END))
                file.write("/text/ \n")

                if len(self.ChoiceList.get(0,tk.END)) > 0:
                    file.write(r"%choice%"+"\n")
                    ut.write_choice_redirectFile(self,file,w='c')
                    file.write("/choice/" +"\n")

                    file.write(r"%redirect%" +'\n')
                    ut.write_choice_redirectFile(self,file,w='r')
                    file.write("/redirect/ \n")
                else:

                    file.write(r"%choice%"+"\n")
                    file.write("/choice/ \n")
                    
                    file.write(r"%redirect%" +'\n')
                    file.write("/redirect/ \n")

    def CreateNewFile(self,fileName,win):
        if self.GameDir != "":
            with open(ut.scene_path(self.GameDir,fileName + ".scene"),'w') as f:
                f.write("%text% /text/ \n")
                f.write(r"%choice% /choice/ \n")
                f.write(r"%redirect% /redirect/ \n")
                
            
            ut.load_scene_files(self,self.GameDir)
            self.selected_file = fileName

        win.destroy()
        self.toplevelExists =False
    
    def OpenNewFolder(self):
        fileDir = filedialog.askdirectory(title="Select Game Folder")

        if fileDir:
            self.GameDir = fileDir
        
            ut.load_scene_files(self,self.GameDir)
    
    def CreateNewProject(self,title,win):

        dir = filedialog.askdirectory(title="Choose directory")

        if dir:
    
            if eu.create_project(dir,title): 
                msg.showinfo(title="Success",message="Project Created")
                self.GameDir = dir
            else:
                msg.showerror(title="Failed",message="Project creation failed")

        
        win.destroy()
    
    def chooseDir(self):
        dir = filedialog.askdirectory(title="Export Game in > ") #Selecting directory to export game 

        if dir:
            eu.exportProject(dir,self)
        else:
            msg.showerror(title="Error",message="Directory not selected")

    def OtherTabContent(self,info):
        if info == "About":
            msg.showinfo(title="About",message="YourTale \ncreated by Aryan Soy")
        else:
            msg.showinfo(title="Version",message="Version 1.0")



if __name__ == "__main__":
    window = ctk.CTk()
    main = YourTale(window)
    window.mainloop()
