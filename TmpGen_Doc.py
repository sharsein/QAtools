# create a program where user specifies a string S, folder location, and X number of files.
# User can specify name of files saved, but default is tmp
# Program saves those files to specified location
# create Gui
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *

# create the window
root = Tk()
root.wm_title("Text File Generator")
root.wm_minsize(width = 650, height = 50)
titleApp = LabelFrame(root, text= "Generate test .txt files")
titleApp.place(anchor = NW) #pack does not let you anchor content to corner
print (titleApp)

## create input field for the name of files. Default is tmp
nameLabel = Label(titleApp, text = "File name")
nameLabel.pack(side = LEFT)
nameEntry = Entry(titleApp, bd = 3) #bd is size of gutter around facet
nameEntry.insert(0,"tmp") #so user knows default name
nameEntry.pack(side = LEFT)

## create input text box for text string. Default is a space
textLabel = Label(titleApp, text = "Text")
textLabel.pack(side = LEFT)
textEntry = Entry(titleApp,bd = 3)
textEntry.pack(side = LEFT)

## create input fields for loop num. Default is 0.
loopLabel = Label(titleApp, text = "Number of files")
loopLabel.pack(side = LEFT)
loopEntry = Entry(titleApp, bd = 3)
loopEntry.pack(side = LEFT)

# functions to check values of each entry field
def checkLoopEntry():
    try:
        enterednumber = int(loopEntry.get())
        print(enterednumber)
        return enterednumber
    except ValueError:
        print ("loop check failed," + loopEntry.get())
        messagebox.showinfo("Invalid input", "Enter number of files to create")
        return 0
def checkFileName():
    enteredname = nameEntry.get()
    if enteredname:
        return enteredname
    else:
        print("Use default file name")
        return "tmp"
def checkContent():
    enteredcontent = textEntry.get()
    if enteredcontent:
        return enteredcontent
    else:
        print("Default to empty")
        return " "
# function that generates files if all values are correct. Exits if user cancels directory
def generate():
    valid = checkLoopEntry()
    if valid is 0:
        print("how many files do you want to create?") # message box called in function
    else:
        filename = checkFileName()
        outString = checkContent()
        root.directory = filedialog.askdirectory()
        if not root.directory:
            # throw message that no directory selected
            messagebox.showinfo("No directory", "You need to save somewhere")
            return "no directory"
        print("directory is" + root.directory)
        filename = root.directory + "/" + filename + "_"
        # debug
        print(filename)
        print(outString)
        # generate
        for index in range(valid):
            absFilePath = filename + str(index) + ".txt"
            outputTestFile = open(absFilePath, 'w')
            outputTestFile.write(outString + "\n" + "\n" + absFilePath)
            outputTestFile.close()

        messagebox.showinfo("Done", "Files created in " + root.directory)

def buttonclicked():
    print("clicked!")
## create button. Note that command= cannot use ()
EnterButton = Button(titleApp, text = "Set Folder", command = generate)
EnterButton.pack(side = BOTTOM)

root.mainloop()


# when clicking an Ok button, this should check field for valid input
# if input is wrong, nothing happens, user can change input field
# if input is correct, folder dialog appears
# after selecting folder, call the files gen function

# function for creating the docs
#def generateFiles(inputText, directory, fileNum, nameText):

