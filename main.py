from tkinter import *
import tkinter as ttk
import pandas as pd 

DF = pd.read_csv("ProjectData.csv")

DF.drop( DF[ DF['SEATS'] == 0 ].index , inplace=True)


# get list of all available carriers
carrierDF = DF["UNIQUE_CARRIER_NAME"].unique()
smallerDF = pd.DataFrame()

smallerDF['Carrier'] = DF['CARRIER_NAME']
smallerDF['Origin City'] = DF['ORIGIN_CITY_NAME']
smallerDF['Destination City'] = DF['DEST_CITY_NAME']
smallerDF['Month'] = DF['MONTH']
smallerDF['Aircraft'] = DF['AIRCRAFT_TYPE']
smallerDF['Seats'] = DF['SEATS']
smallerDF['Distance'] = DF['DISTANCE']


smallerDF.to_csv("small_data.csv")

root = Tk()
root.title("Flight Recommendations")
 
# Add a grid
mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 100)
 
# Create a Tkinter variable
tkvar = StringVar(root)
 
# Dictionary with options
choices = carrierDF.tolist()
 
popupMenu = OptionMenu(mainframe, tkvar, *choices)
Label(mainframe, text="Choose an Airline").grid(row = 1, column = 1)
popupMenu.grid(row = 2, column =1)
 
# on change dropdown value
def change_dropdown(*args):
    print( tkvar.get() )
 
# link function to change dropdown
tkvar.trace('w', change_dropdown)
 
root.mainloop()