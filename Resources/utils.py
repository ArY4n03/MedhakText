    #Fetches choices and redirect files from choice list
from pathlib import Path
import pickle

def write_choice_redirectFile(self,file,w='c'):
    for choice in self.ChoiceList.get(0,"end"):
        if w=='c':
            t,_ = choice.split("->")
        else:
            _,t = choice.split("->")

        file.write(f"{t}*end* \n")

#loads scene files in the listbox
def load_scene_files(self,GameDir):
    self.FileList.delete(0,'end')
    path = Path(GameDir) / "Scenes"
    for i in path.glob("*.scene"):
        self.FileList.insert("end",i.name) #tk.END == "end"

#retuns scene path
def scene_path(gameDir,scene):
    scene_folder = "Scenes"
    return Path(gameDir) / scene_folder / scene 

def update_gameSettings(engine):
    if engine.GameDir != "": #if gamedir is != "" then some project is opened
        with open(engine.GameDir +"/Settings.dat","rb+") as file:
            settings = pickle.load(file)
            settings['start_screen'] = engine.startsceneEntry.get()
            settings['title'] = engine.titleEntry.get()
            file.seek(0)
            pickle.dump(settings,file)
            print(settings)