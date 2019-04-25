from tkinter import *
from tkinter import ttk
import pandas as pd
import os.path
import calendar as cal
from datetime import datetime
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
  smallerDF['Passengers'] = DF['PASSENGERS']
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
  DF = getSmallerDF(filePath)
  
  # calculate success % and available seat % from given columns and sort
  DF['Success Percentage'] = (DF['Departures Performed']/DF['Departures Scheduled'])
  DF['Available Percentage'] = (DF['Passengers']/DF['Seats'])

  # get columns with above 100% rating and replace with 100%
  above100 = DF['Success Percentage'] > 100
  DF.loc[above100, 'Success Percentage'] = 100

  scoreDF = pd.DataFrame(columns=("Month","Average Success %", "Average Available Seats %", "Algorithm Score"))
  monthList = []

  # for loop that converts month numbers to names
  for month in range(1,13):
    monthList.append(cal.month_name[month])

  scoreDF['Month'] = monthList  
  averageSuccessList = []
  averageSeatList = []

  # for loop for actual score calculation
  for month in range(1,13):
    # pull all months that have the matching loop number
    monthRows = DF['Month'] == month

    # find these rows and get their average, add to list
    averageSuccessList.append((DF.loc[monthRows, 'Success Percentage']).mean())
    averageSeatList.append((DF.loc[monthRows, 'Available Percentage']).mean())

  scoreDF['Average Success %'] = averageSuccessList
  scoreDF['Average Available Seats %'] = averageSeatList

  # The actual algorithm implementation, I consider average flight success to help each
  # month's score. While the higher the available seats percentage, the more it hurts
  # the overall score.
  scoreDF['Algorithm Score'] = (50 * scoreDF['Average Success %']) + (-50 * scoreDF['Average Available Seats %'])
  scoreDF.sort_values(by=['Algorithm Score'], inplace=True, ascending=False)

  scoreDF["Algorithm Score"] = scoreDF["Algorithm Score"].round(3)

  style = ttk.Style()
  style.configure("Treeview", padding=20, fieldbackground="#238c63", font=('Helvetica', 15))

  autoFrame = Toplevel(master)

  autoFrame.title("Automatic Flight Recommendations")       
  autoFrame.grid_rowconfigure(0,weight=1)
  autoFrame.grid_columnconfigure(0,weight=1)

  # Set the treeview
  autoFrame = ttk.Treeview(autoFrame,height=12,columns=('Dose', 'Modification date'), style='Treeview')

  autoFrame.heading('#0', text='Month')
  autoFrame.heading('#1', text='Algorithm Score (Out of 20)')
  autoFrame.column('#1')
  autoFrame.column('#0')
  autoFrame.grid(row=4, columnspan=2, sticky='nsew')
  


  for index,month in scoreDF.iterrows():
    #insert month into treeview
    monthRow = autoFrame.insert('', 'end', text=month["Month"], values=month['Algorithm Score'])

    #pull flights from the current iterated month
    monthNum = datetime.strptime(month["Month"], '%B')
    monthFlightList = DF.loc[DF['Month'] == monthNum.month]
    
    # get the relevant info for sub menus
    carriers = monthFlightList["Carrier"].tolist()
    number = monthFlightList["Aircraft"].tolist()
    city = monthFlightList["Origin City"].tolist()
    
    # only keep the first 5
    carriers = carriers[:5]
    number = number[:5]
    city = city[:5]

    # insert list of flights for each month as sub menu
    for (carr, num, city) in zip(carriers, number, city): 
      autoFrame.insert(monthRow, "end", text=carr, values=(num,city))


# function that is called when clicking the "manual" button
def manualMenu(filePath):
  selectionList = []
 # on change dropdown value
  def onSelect(value):
    selectionList.append(str(value))

  def manualLookup():
    print(selectionList)


  DF = getSmallerDF(filePath)
  manualFrame = Toplevel(master)

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

  # Create all of the labels and optionmenus 
  promptLabel = Label(manualFrame, text="Choose an Airline")
  originLabel = Label(manualFrame, text="Choose your Origin City")
  destinationLabel = Label(manualFrame, text="Choose your Destination City")
  planeLabel = Label(manualFrame, text="Choose your preferred plane")
  airlineMenu = OptionMenu(manualFrame, airlineVar, *airlineChoices, command=onSelect)
  originMenu = OptionMenu(manualFrame, originVar, *originChoices, command=onSelect)
  destinationMenu = OptionMenu(manualFrame, destinationVar, *destinationChoices, command=onSelect)
  planeMenu= OptionMenu(manualFrame, planeVar, *planeChoices, command=onSelect)
  generate = Button(manualFrame, text="Generate", height=5, width=40,fg="#ffffff", bg="#4f4977", command=manualLookup)

  promptLabel.grid(row = 1, column = 1,sticky=(N))
  airlineMenu.grid(row = 1, column = 2,sticky=(E))
  originLabel.grid(row = 2, column = 1,sticky=(W))
  originMenu.grid(row = 2, column = 2,sticky=(E))
  destinationLabel.grid(row = 3, column = 1,sticky=(W))
  destinationMenu.grid(row = 3, column = 2,sticky=(E))
  planeLabel.grid(row = 4, column = 1,sticky=(W))
  planeMenu.grid(row = 4, column = 2,sticky=(E))
  generate.grid(column=0,row=5,columnspan=3, padx=5, pady=5, sticky=(W,E))


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