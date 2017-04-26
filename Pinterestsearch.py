# asks user for a keyword
# asks user for number of images
# asks user for a directory
# google image search for keyword
# saves images to directory

from bs4 import BeautifulSoup
import requests
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import re
import html5lib #played with using this to see if it worked better than html.parser. No difference

# hard coded supported browsers
browsers = {}
browsers['User-Agent'] = "Chrome/57.0.2987.110"
idirectory = "C:\\Users\\qa\\Documents\\testPicPin"


# support functions for google search
def htmlTosoup(url):
    response = requests.get(url, headers=browsers)
    try:
        soup = BeautifulSoup(response.content, "html.parser")
        print("yay soup")
        print(str(response.content))
    except e as Exception:
        print(str(e))
    return soup

# function that does a google image search for a keyword
#imgNum not used. Will be used so user can specify number of images returned.
def getGoogleImg(imgSearch, imgNum, imgDir):
    resultspage = "http://www.pinterest.com/search/pins/?q=" + imgSearch
    print(resultspage)
    resultsSoup = htmlTosoup(resultspage)
    #print(resultsSoup)

    ###### pipe resultsSoup to a file###########
    ### Unicode error for Pinterest, weird because it works for google and Pycharm is set to UTF-8
    #with open(imgDir + "/" + imgSearch + "_resultsSoup" + ".txt", 'w') as f:
        #f.write(str(resultsSoup))
    #################

    ''' to get full size images:
            create a list of href from <a class = "pinImageWrapper"
            for each href, call htmlTosoup(www.pinterest.com + href value)
            imagesOnimgPage = htmlTosoup return value.find_all("img")
            for i in imagesOnimgPage:
                biglink = i['src']
            ListofFullsizeImages.append(biglink)
            subString="https://s-media-cache-ak0.pinimg.com/564x/"
            if ListofFullsizeImages[index] starts with the subString
            save
        '''
    print("full size search done")
    pinWrappers = resultsSoup.find_all("a", class_="pinImageWrapper")
    ListofFullsizeImages = []
    if (imgNum > 25):
        print("Still need to figure this shit out. Defaulting to 25 for now")
        '''Search returns 25 containers that contain links to full size images
        Each full size image link contains the full size image and 10 containers with suggested results images
        So I can keep calling a function that grabs the big image then goes to the link of the suggested result image
        until imgNum is reached. This seems really slow though'''
        imgNum = 25
    if (imgNum < 26):
        for pinWrapper in pinWrappers:
            pinLink = pinWrapper['href']
            print("fullimgext=" + pinLink) #only getting 25 results...
            pinUrl = "https://www.pinterest.com" + str(pinLink)
            print("pinUrl=" + pinUrl)
            pinSoup = htmlTosoup(pinUrl)
            imagesOnPage = pinSoup.find_all("img")
            print("tmp code line 68. Defaulting to 25 images for now")
            for imgElement in imagesOnPage:
                fullImglink = imgElement['src']
                print("fullImglink=" + fullImglink)
                if not (fullImglink.startswith("https://s-media-cache-ak0.pinimg.com/236x/")) :
                    ListofFullsizeImages.append(fullImglink)
    numFullLinks = len(ListofFullsizeImages)
    print("number of full size image links=" + str(numFullLinks))
    if numFullLinks < 1:
        return
    else:
        for num in range(numFullLinks):
            imgData = requests.get(ListofFullsizeImages[num])
            if imgData.status_code == 200:
                with open(imgDir + "/" + imgSearch + "_full_" + str(num) + ".jpg", 'wb') as f:
                    f.write(imgData.content)
            else:
                print("link failed")

###############################################################

    print("\n getGoogleImg needs code " + ", " + imgSearch + ", " + str(imgNum) + ", " + imgDir)


#####################################################
#GUI setup
root = Tk()
root.wm_title("Pinterest scraper")
root.wm_minsize(width = 650, height = 50)
titleApp = LabelFrame(root, text= "Download images from Pinterest")
titleApp.place(anchor = NW) #pack does not let you anchor content to corner
print (titleApp)

## create input field for the name of files. Default is tmp
nameLabel = Label(titleApp, text = "Keyword")
nameLabel.pack(side = LEFT)
nameEntry = Entry(titleApp, bd = 3) #bd is size of gutter around facet
#nameEntry.insert(0,"tmp") #so user knows default name
nameEntry.pack(side = LEFT)

## create input fields for loop num. Default is 0.
numLabel = Label(titleApp, text = "Number of files")
numLabel.pack(side = LEFT)
numEntry = Entry(titleApp, bd = 3)
numEntry.pack(side = LEFT)

# functions to check values of each entry field
def checknumEntry():
    try:
        enterednumber = int(numEntry.get())
        print(enterednumber)
        return enterednumber
    except ValueError:
        print ("num check failed," + numEntry.get())
        print ("defaulting to 25")
        return 25
def checkKeyword():
    enteredkey = nameEntry.get()
    if enteredkey:
        return enteredkey
    else:
        print("Defaulting to image")
        return "image"

def userInput():
    keywordinput = checkKeyword()
    numFiles = checknumEntry()
    root.directory = filedialog.askdirectory()
    if not root.directory:
        # throw message that no directory selected
        messagebox.showinfo("No directory", "You need to save somewhere")
        return "no directory"
    print("directory is" + root.directory)
    getGoogleImg(keywordinput, numFiles, root.directory)
    messagebox.showinfo("Done", "Images saved to " + root.directory)

EnterButton = Button(titleApp, text="Set Folder", command=userInput)
EnterButton.pack(side=BOTTOM)

root.mainloop()




