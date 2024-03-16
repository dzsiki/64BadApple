import base64
import pickle
import numpy as np
import pyautogui
import time
from PIL import ImageGrab
import pyperclip

# Load the converted video
with open('my_array.pkl', 'rb') as f:
    minden = pickle.load(f)

# strings for the save file
savestart = '{"stuff":[{"name":"strange","position":[-100,-100],"par":{"soul":1}},'
saveend = '{"name":"cookie","position":[-1024,1024],"par":{"soul":1}}],"onlyones":{},"resources":[0,0,0,0,0,0,0,0,0,0],"eraserType":0,"hollowHardness":64,"slowdown":{"state":false,"timer":0,"totalTime":0,"multiplyer":0.1,"f":0,"cooldown":0},"plane":0,"version":"1.0.6","switchedplanes":false,"bridge":false,"unlockedEntities":{},"needNoHelp":false,"messengerShownMessages":[0,1,2,3,4,5,6,7,8,9,10],"messengerFiredEvents":[true,true],"messengerShown":0,"existed":{"eraser":true,"eraser2":true,"eraser3":true,"pump":true},"glory":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],"stats":{"totalResourcesMined":[0,0,0,0,0,0,0,0,0,0],"absoluteResourcesCount":0,"maxDepth":0.5437327687437783,"timeEvents":0,"totalPlayTime":70065.5,"totalCubeClicks":0,"machinesBuild":0,"machinesSold":0,"timesTeleported":0,"strangeRockPoked":0,"darkVisited":0,"timeSinceLastDelete":null},"timestamp":1710473574536}'
# szív means heart in Hungarian, coordinates of the heart shape
sziv = [[-5, 24], [-3, 22], [-5, 25], [-3, 23], [-2, 22], [-4, 24], [-5, 26], [-3, 24], [-1, 22], [-5, 27], [0, 22],
        [-4, 27], [0, 23], [-3, 27], [0, 24], [-2, 27], [0, 25], [-1, 27], [0, 26], [0, 27]]


# converting arrays to string (default convert is e.g:[0, 1], it's converting to:[0,0] without the spaces)
def a2s(array):
    output = "["
    for e in array:
        output += str(e) + ","
    output = output[:-1] + "]"
    return output


# class for the cubes
class Cube:
    def __init__(self):
        # materials of the cube
        self.m = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # coordinates of the cube
        self.pose = [0, 0]

    def set_pose(self, x, y):
        self.pose = [x, y]

    # colors is an 8 length array. Replacing the top layer of the cube with colors
    def set_color(self, colors):
        self.m = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.m.extend(colors)

    # converting the cube into string (save file)
    def tos(self):
        return '{"name":"cube","position":' + a2s(self.pose) + ',"par":{"fill":64,"state":2,"resources":' + a2s(
            self.m) + ',"soul":1,"broken":0}},'


# colors for hollow
hollow = [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
# number of the start frame
start = 0
for idx, frame in enumerate(minden[start:]):
    savefile = savestart
    # array for all the cubes in this frame
    allcube = []
    for i in range(43):
        for j in range(30):
            # if it's not the outer ring (extracting channels)
            if i != 0 and i != 42 and j != 0 and j != 29:
                # kocka = cube in Hungarian
                kocka = Cube()

                kocka.set_pose(i - 20, j - 13)
                # if it's the one smaller outer ring (hollows)
                if i == 1 or i == 41 or j == 1 or j == 28:
                    kocka.set_color(hollow)
                else:
                    # idk why I need to transpose the color indexes (it's rotated by ?90deg? by default)
                    # frame[(i - 2) * 26 + (j - 2)] get the color array of the current cube (-2 is because of the outer rings)
                    arr = np.array(frame[(i - 2) * 26 + (j - 2)]).reshape((4, 4))
                    arr = np.transpose(arr)
                    # there is no need for rot90 anymore
                    kocka.set_color(np.rot90(arr, 0).flatten().tolist())
                #add the cube
                allcube.append(kocka)
            else:
                # if it is the outer ring (extracting channels)
                savefile += '{"name":"pump2","position":' + a2s(
                    [i - 20, j - 13]) + ',"par":{"depth":0,"timeStamp":0,"soul":1}},'

    # adding both bottom left and upper right heart to allcube array
    for i in range(len(sziv)):
        kocka = Cube()
        kocka2 = Cube()

        kocka.set_pose(sziv[i][0] + 2, sziv[i][1] + 1)
        kocka.set_color([3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
        kocka2.set_pose(sziv[i][0] + 4, sziv[i][1] - 50)
        kocka2.set_color([3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
        allcube.append(kocka)
        allcube.append(kocka2)

    # adding every cube to the save file string
    for kocka in allcube:
        savefile += kocka.tos()
    savefile += saveend

    # encode the savefile into base64
    saveinbase64 = base64.b64encode(savefile.encode('utf-8'))
    # copy the save file to clipboard
    pyperclip.copy(str(saveinbase64)[2:-1])

    # script for auto import the save into the game then screenshot it and save it in a folder named 64badpics
    pyautogui.click(100, 100)
    pyautogui.press('esc')
    time.sleep(1)
    pyautogui.click(1150, 1050)
    time.sleep(1)
    pyautogui.press('esc')
    time.sleep(1)
    pyautogui.keyDown('shift')
    pyautogui.scroll(-10000)
    pyautogui.keyUp('shift')
    pyautogui.moveTo(2000, 1000, 0.75)
    screenshot = ImageGrab.grab()
    screenshot.save("e:/64badpics/frame" + str(idx + start) + ".png")
    # print the current frame number
    print(start + idx)
