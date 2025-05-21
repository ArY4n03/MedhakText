import tkinter as tk
from tkinter import filedialog
import pickle

import sys

arguments = sys.argv

class GameRunner:

    def __init__(self,master,gamedir,scene):
        self.master =master
        self.master.title("Game Runner")
        self.master.geometry("1200x600")
        self.master.config(bg="grey")
        self.scene_file =scene
        self.gamedir = gamedir
        self.choices_scene_list = []
        self.TitleScreen_options = []
        self.loaded_frames = {"titlescreen":True,"gamescreen":False,"endscreen":False}
        #Frames
        self.TitleScreen = tk.Frame(self.master)
        self.TitleScreen.place(relx= 0 , rely= 0 ,relheight=1,relwidth=1)

        self.GameScreen = tk.Frame(self.master)
        self.GameScreen.place(relx= 0 , rely= 0 ,relheight=1,relwidth=1)

        self.EndScreen = tk.Frame(self.master)
        self.EndScreen.place(relx= 0 , rely= 0 ,relheight=1,relwidth=1)

    #TitleScreen Content
        self.Title = tk.Label(self.TitleScreen,text="Game Runner",font=(None,40)).place(relx= 0.35,rely=0.08)

        self.Play = tk.Button(self.TitleScreen,text="Play",font=(None,30),command=self.startGame)
        self.Play.place(relx=0.43,rely=0.3)

        self.TitleScreen.tkraise()
        #self.GameScreen.tkraise()
    

    def GameScreenContent(self):
        #GameScreen content
            
            #text area
            self.text_area = tk.Text(self.GameScreen,state="disabled",wrap="word")
            self.text_area.place(relx = 0.05, rely = 0.02,relwidth=0.8,relheight=0.6)
            
            #text scroll bar
            self.text_scroll_bar = tk.Scrollbar(self.GameScreen)
            self.text_scroll_bar.place(relx = 0.87, rely = 0.02,relheight=0.6)
            self.text_scroll_bar.config(command = self.text_area.yview)
            self.text_area.config(yscrollcommand= self.text_scroll_bar.set)

            #choice list
            self.choice_list = tk.Listbox(self.GameScreen)
            self.choice_list.place(relx = 0.05, rely = 0.75,relwidth=0.8,relheight=0.2)
            
            #list scroll bar
            self.list_scroll_bar = tk.Scrollbar(self.GameScreen)
            self.list_scroll_bar.place(relx = 0.87, rely = 0.75,relheight=0.2)
            self.list_scroll_bar.config(command = self.choice_list.yview)
            self.choice_list.config(yscrollcommand= self.list_scroll_bar.set)

            #next button
            self.NextButton = tk.Button(self.GameScreen,text="Next",font=(None,25),command=self.change_to_next_scene)
            self.NextButton.place(relx=0.92,rely=0.8)

        #EndScreen Content
            self.EndScreenText = tk.Label(self.EndScreen,text="The End",font=(None,30))
            self.EndScreenText.place(relx=0.4,rely=0.2)

            self.PrintBtn = tk.Button(self.EndScreen,text="Save Story",font=(None,30),command=self.print_story)
            self.PrintBtn.place(relx=0.38,rely=0.7,relheight=0.1,relwidth=0.2)

            self.load_text() #loads the text
            self.update_choices() #it update choices 

    
    def get_sceneFile_data(self,scene_file):
        with open(self.gamedir+"/"+"Scenes/"+scene_file,'r') as file:
            content = file.read()

        return content
    
    def update_text_area(self,text):
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END,text)
        self.text_area.config(state="disabled")
        self.text_area.yview(tk.END)
        
    def load_text(self): #displays the text block
        content = self.get_sceneFile_data(self.scene_file)
        print(content)
        content = content[(content.index("%text%") + 6) : content.index("/text/")]

        self.update_text_area(content)

    def update_choices(self): #update all the choices in choices list
        
        self.choice_list.delete(0,tk.END)

        content = self.get_sceneFile_data(scene_file=self.scene_file)

        content  =content[(content.index(r"%choice%") + 8) : content.index("/choice/")]
        content = content.lstrip()
        content = content.rstrip()
        content = content.split("*end*")
        content.remove("")
        
        for choice in content:
            self.choice_list.insert(tk.END,choice.strip())
        
        self.update_choices_scene()

    def update_choices_scene(self): #update list of scenes corresponding to different choices
        print("update_choices_scene function")
        self.choices_scene_list.clear() #clearig previous scene data every new one loads
        content = self.get_sceneFile_data(scene_file=self.scene_file)

        content  = content[(content.index(r"%redirect%") + 10) : content.index("/redirect/")]
        content = content.lstrip()
        content = content.rstrip()
        content = content.split("*end*")
        content.remove("")
        for choice in content:
            self.choices_scene_list.append(choice.strip())
    
    def change_to_next_scene(self): #called everytime user makes a choice
        choice = self.choice_list.curselection()[0]
        if self.choices_scene_list[choice] != "endscreen":
            self.scene_file = self.choices_scene_list[choice]
            self.load_text()
            self.update_choices()
            self.update_choices_scene()
        else:
            self.change_frame(frame="endscreen")

    def change_frame(self,frame='gamescreen'):
        if frame == 'gamescreen':
            self.GameScreen.tkraise()
            if not self.loaded_frames[frame]:
                self.GameScreenContent()
                self.loaded_frames[frame] = True
                
        elif frame == 'endscreen':
            self.EndScreen.tkraise()
        else:
            self.TitleScreen.tkraise()
    
    def startGame(self):
        self.change_frame()

    def print_story(self):
        self.filename = filedialog.asksaveasfilename(initialfile="untitled.txt",
                                                    defaultextension="*.txt",
                                                    filetypes=[("Text files","*.txt")])
        
        with open(self.filename,'w') as file:
            file.write(self.text_area.get(1.0,tk.END))


if __name__ == "__main__":
    window = tk.Tk()
    scene = arguments[2] if len(arguments) > 1 else ""
    gamerunner = GameRunner(window,arguments[1],arguments[2])
    print(arguments)
    window.mainloop()