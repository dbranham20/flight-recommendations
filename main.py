from tkinter import *
import tkinter as ttk
import pandas as pd
import os.path

def smallerDF(bigDF,filename):
  # drop all rows that contain airline flights with 0 seats
  DF.drop( DF[ DF['SEATS'] == 0 ].index , inplace=True)

  smallerDF = pd.DataFrame()
  smallerDF['Carrier'] = DF['CARRIER_NAME']
  smallerDF['Origin City'] = DF['ORIGIN_CITY_NAME']
  smallerDF['Destination City'] = DF['DEST_CITY_NAME']
  smallerDF['Month'] = DF['MONTH']
  smallerDF['Aircraft'] = DF['AIRCRAFT_TYPE']
  smallerDF['Seats'] = DF['SEATS']
  smallerDF['Distance'] = DF['DISTANCE']

  # write smaller dataFrame to csv in case needed
  smallerDF.to_csv(filename)
  return smallerDF

def autoMenu():
  print("auto menu")

def manualMenu():
  print("manual menu")






DF = pd.read_csv("ProjectData.csv")

# If the smaller dataframe used for the rest
# of the program has not been made, make it
smallFileName = "filtered_data.csv"

if not os.path.isfile(smallFileName):
  print("Making smaller data file...")
  smallerDF(DF,smallFileName)



master = Tk()
master.title("Flight Recommendations")

mainFrame = Frame(master)
mainFrame.grid(column=0,row=0, sticky=(N,W,E,S))
mainFrame.pack(pady=25, padx=25)

label = Label(mainFrame, text="Please choose a Recommendation Method", font=32)
auto = Button(mainFrame, text="Auto Recommend", height=20, width=40, fg="#ffffff", bg="#3f7049", relief=GROOVE, command=autoMenu)
manual = Button(mainFrame, text="Manual Recommend", height=20, width=40, fg="#ffffff", bg="#4f4977", relief=RIDGE, command=manualMenu)
exitApp = Button(mainFrame, text="Close App", height=10, width=80, fg="#ffffff", bg="#703f3f", command=master.destroy)

label.grid(column=0, row=0, columnspan=2, stick=(W,E))
auto.grid(column=0, row=1, padx=5, pady=5)
manual.grid(column=1, row=1, padx=5, pady=5)
exitApp.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky=(W,E))

master.mainloop()

# get list of all available carriers
carrierDF = DF["UNIQUE_CARRIER_NAME"].unique()


 
# # Add a grid
# mainframe = Frame(master)
# mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
# mainframe.columnconfigure(0, weight = 1)
# mainframe.rowconfigure(0, weight = 1)
# mainframe.pack(pady = 100, padx = 100)
 
# # Create a Tkinter variable
# tkvar = StringVar(master)
 
# # Dictionary with options
# choices = carrierDF.tolist()
 
# popupMenu = OptionMenu(mainframe, tkvar, *choices)
# Label(mainframe, text="Choose an Airline").grid(row = 1, column = 1)
# popupMenu.grid(row = 2, column =1)
 
# # on change dropdown value
# def change_dropdown(*args):
#     print( tkvar.get() )
 
# # link function to change dropdown
# tkvar.trace('w', change_dropdown)
 
# master.mainloop()