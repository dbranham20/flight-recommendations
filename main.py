from tkinter import *
import tkinter as ttk
import pandas as pd
import os.path


# reads the larger DF and cuts it down to only the necessary data
def smallerDF(bigDF,filename):
  # drop all rows that contain airline flights with 0 seats
  DF.drop( DF[ DF['SEATS'] == 0 ].index , inplace=True)

  # drop all rows with airlines that had no departures scheduled
  DF.drop( DF[ DF['DEPARTURES_SCHEDULED'] == 0].index, inplace=True)

  # pull out only the columns needed
  smallerDF = pd.DataFrame()
  smallerDF['Carrier'] = DF['CARRIER_NAME']
  smallerDF['Origin City'] = DF['ORIGIN_CITY_NAME']
  smallerDF['Destination City'] = DF['DEST_CITY_NAME']
  smallerDF['Month'] = DF['MONTH']
  smallerDF['Aircraft'] = DF['AIRCRAFT_TYPE']
  smallerDF['Seats'] = DF['SEATS']
  smallerDF['Distance'] = DF['DISTANCE']
  smallerDF['Departures Performed'] = DF['DEPARTURES_PERFORMED']
  smallerDF['Departures Scheduled'] = DF['DEPARTURES_SCHEDULED']

  # write smaller dataFrame to csv in case needed
  smallerDF.to_csv(filename)
  return smallerDF


# function to read the smaller .csv into a dataframe
def getSmallerDF(filePath):
  currDF = pd.read_csv(filePath)
  return currDF


# function that is called when clicking the "auto" button
def autoMenu(filePath):
  print("auto")


# function that is called when clicking the "manual" button
def manualMenu(filePath):

 # on change dropdown value
  def onSelect(value):
      print("Value chosen is: " + str(value))

  DF = getSmallerDF(filePath)
  manualFrame = Toplevel(master)
  # manualFrame.geometry("500x500")

  manualFrame.columnconfigure(0, weight=1)
  manualFrame.rowconfigure(0, weight=1)

  # finds all of the unique values for airlines
  airlineChoices = DF['Carrier'].unique().tolist()
  originChoices = DF['Origin City'].unique().tolist()
  destinationChoices = DF['Destination City'].unique().tolist()
  planeChoices = DF['Aircraft'].unique().tolist()

  # Create tkinter variables
  airlineVar = StringVar(value=airlineChoices[0])
  originVar = StringVar(value=originChoices[0])
  destinationVar = StringVar(value=destinationChoices[0])
  planeVar = StringVar(value=planeChoices[0])

  promptLabel = Label(manualFrame, text="Choose an Airline")
  originLabel = Label(manualFrame, text="Choose your Origin City")
  destinationLabel = Label(manualFrame, text="Choose your Destination City")
  planeLabel = Label(manualFrame, text="Choose your preferred plane")
  airlineMenu = OptionMenu(manualFrame, airlineVar, *airlineChoices, command=onSelect)
  originMenu = OptionMenu(manualFrame, originVar, *originChoices, command=onSelect)
  destinationMenu = OptionMenu(manualFrame, destinationVar, *destinationChoices, command=onSelect)
  planeMenu= OptionMenu(manualFrame, planeVar, *planeChoices, command=onSelect)

  promptLabel.grid(row = 1, column = 1)
  airlineMenu.grid(row = 1, column = 2)
  originLabel.grid(row = 2, column = 1)
  originMenu.grid(row = 2, column = 2)
  destinationLabel.grid(row = 3, column = 1)
  destinationMenu.grid(row = 3, column = 2)
  planeLabel.grid(row = 4, column = 1)
  planeMenu.grid(row = 4, column = 2)



  # print(airlineVar.get())
  # print(originVar.get())
  # print(destinationVar.get())
  # print("Plane chosen is: " + planeVar.get())
  # link function to change dropdown
  # airlineVar.trace('w', lambda: change_dropdown(airlineVar))
  # originVar.trace('w', change_dropdown)
  # destinationVar.trace('w', change_dropdown)
  # planeVar.trace('w', change_dropdown)
  
  # auto.mainloop()




# Start of Main
DF = pd.read_csv("ProjectData.csv")

# If the smaller dataframe used for the rest
# of the program has not been made, make it
smallFileName = "filtered_data.csv"
if not os.path.isfile(smallFileName):
  print("Making smaller data file...")
  smallerDF(DF,smallFileName)

# Start to build the GUI for main menu
master = Tk()
master.title("Flight Recommendations")

mainFrame = Frame(master)
mainFrame.grid(column=0,row=0, sticky=(N,W,E,S))
mainFrame.pack(pady=25, padx=25)

# build all of the buttons and labels. Lambda keyword allows me to pass an argument in the "command" parameter
label = Label(mainFrame, text="Please choose a Recommendation Method", font=32)
auto = Button(mainFrame, text="Auto Recommend", height=20, width=40, fg="#ffffff", bg="#3f7049", relief=GROOVE, command= lambda: autoMenu(smallFileName))
manual = Button(mainFrame, text="Manual Recommend", height=20, width=40, fg="#ffffff", bg="#4f4977", relief=RIDGE, command= lambda: manualMenu(smallFileName))
exitApp = Button(mainFrame, text="Close App", height=10, width=80, fg="#ffffff", bg="#703f3f", command=master.destroy)

label.grid(column=0, row=0, columnspan=2, stick=(W,E))
auto.grid(column=0, row=1, padx=5, pady=5)
manual.grid(column=1, row=1, padx=5, pady=5)
exitApp.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky=(W,E))

master.mainloop()
