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
def getSmallerDF():
  currDF = pd.read_csv("filtered_data.csv")
  return currDF

def theAlgorithm(DF):

  # calculate success % and available seat % from given columns and sort
  DF['Success Percentage'] = (DF['Departures Performed']/DF['Departures Scheduled'])
  DF['Available Percentage'] = (DF['Passengers']/DF['Seats'])

  # get columns with above 100% rating and replace with 100%
  above100 = DF['Success Percentage'] > 100
  DF.loc[above100, 'Success Percentage'] = 100

  scoreDF = pd.DataFrame(columns=("Month","Average Success %", "Average Available Seats %", "Distance", "Algorithm Score"))
  monthList = []

  # for loop that converts month numbers to names
  for month in range(1,13):
    monthList.append(cal.month_name[month])

  scoreDF['Month'] = monthList  
  averageSuccessList = []
  averageSeatList = []
  averageDistanceList = []

  # for loop for actual score calculation
  for month in range(1,13):
    # pull all months that have the matching loop number
    monthRows = DF['Month'] == month

    # find these rows and get their average, add to list
    averageSuccessList.append((DF.loc[monthRows, 'Success Percentage']).mean())
    averageSeatList.append((DF.loc[monthRows, 'Available Percentage']).mean())
    averageDistanceList.append((DF.loc[monthRows, 'Distance']).mean())

  scoreDF['Distance'] = averageDistanceList
  scoreDF['Average Success %'] = averageSuccessList
  scoreDF['Average Available Seats %'] = averageSeatList


  # gets minimum value for available seats and distance
  minAvailable = scoreDF['Average Available Seats %'].min() * -.25
  minDistance = scoreDF['Distance'].min()

  # get the weighted scores of each column
  successScore = scoreDF['Average Success %'] * .50
  availableSeatScore = scoreDF['Average Available Seats %'] *-.25
  distanceScore = scoreDF['Distance'] * -.25

  # Algorithm is as follows
  # algScore = (successScore * .5) + ((availableSeatScore adjust by minimum possible score) + (distance score adjusted by minumum possible))
  scoreDF['Algorithm Score'] = (successScore) + ((availableSeatScore - minAvailable) + (((distanceScore / scoreDF['Distance'].max()) - (minDistance / scoreDF['Distance'].max())) * -.25))
  scoreDF.sort_values(by=['Algorithm Score'], inplace=True, ascending=False)

  scoreDF["Algorithm Score"] = scoreDF["Algorithm Score"].round(3)
  
  return scoreDF


# function that is called when clicking the "auto" button
def autoMenu(filePath):
  DF = getSmallerDF()
  display(DF,"Default Flight Recommendations","#3f7049")

def display(DF,mode,color):  
  
  # If the user's input returned now flights, get the full dataset for display
  if(DF.empty):
    DF = getSmallerDF()
    mode = "Default Flight Recommendations"


  # Run the algorithm on the dataset
  scoreDF = theAlgorithm(DF)

  # Tkinter styles and setting up of Treeview
  style = ttk.Style()
  style.configure("Treeview", padding=20, fieldbackground=color, font=('Helvetica', 15))

  autoFrame = Toplevel(master)

  autoFrame.title(mode)       
  autoFrame.grid_rowconfigure(0,weight=1)
  autoFrame.grid_columnconfigure(0,weight=1)

  # More Treeview
  autoFrame = ttk.Treeview(autoFrame,height=12,columns=('Month', 'Algorithm Score (Out of 1)'), style='Treeview')
  autoFrame.heading('#0', text='Month')
  autoFrame.heading('#1', text='Algorithm Score (Out of 1)')
  autoFrame.column('#1')
  autoFrame.column('#0')
  autoFrame.grid(row=4, columnspan=2, sticky='nsew')
  
  for index,month in scoreDF.iterrows():
    #insert month into treeview    
    monthRow = autoFrame.insert('', 'end', text=month["Month"], values=(month['Algorithm Score']))

    #pull flights from the current iterated month, offset 1
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

  def refreshList():
    # Default values for dropdowns
    airlineVar.set("Choose an Airline")
    originVar.set("Choose your Origin City")
    destinationVar.set("Choose your Destination City")
    planeVar.set("Choose your preferred plane")

  #get all of the entries and store in variables
  def manualLookup():
    airline = airlineVar.get()
    origin = originVar.get()
    dest = destinationVar.get()
    plane = planeVar.get()

    # if the first option is not selected, the program
    # still has a Dataframe to look through and filter on
    filterDF = DF
    backupDF = DF

    # filter on only the fields that don't have the default value
    if(airline != "Choose an Airline"):
      filterDF = DF.loc[DF['Carrier'] == airline]
      
      # the backupDF (which we know has data) is only used
      # when the filtering causes an empty dataset
      if(filterDF.empty):
        filterDF = backupDF
    
    if(origin != "Choose your Origin City"):
      backupDF = filterDF
      filterDF = filterDF.loc[DF['Origin City'] == origin]
      
      if(filterDF.empty):
        filterDF = backupDF
    
    if(dest != "Choose your Destination City"):
      backupDF = filterDF
      filterDF = filterDF.loc[DF['Destination City'] == dest]
      
      if(filterDF.empty):
        filterDF = backupDF
    
    if(plane != "Choose your preferred plane"):
      backupDF = filterDF
      filterDF = filterDF.loc[DF['Aircraft'] == int(plane)]
      
      if(filterDF.empty):
        filterDF = backupDF

    # end of manual mode, sending dataframe to be displayed
    display(filterDF, "Manual Flight Recommendations","#4f4977")

  DF = getSmallerDF()
  manualFrame = Toplevel(master)

  manualFrame.columnconfigure(0, weight=1)
  manualFrame.rowconfigure(0, weight=1)
  manualFrame.title("Custom Flight Recommendations") 

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

  # Default values for dropdowns
  airlineVar.set("Choose an Airline")
  originVar.set("Choose your Origin City")
  destinationVar.set("Choose your Destination City")
  planeVar.set("Choose your preferred plane")

  # Create all of the labels and optionmenus 
  airlineMenu = OptionMenu(manualFrame, airlineVar, *airlineChoices)
  originMenu = OptionMenu(manualFrame, originVar, *originChoices)
  destinationMenu = OptionMenu(manualFrame, destinationVar, *destinationChoices)
  planeMenu= OptionMenu(manualFrame, planeVar, *planeChoices)
  generate = Button(manualFrame, text="Generate", height=5, width=30,fg="#ffffff", bg="#4f4977", command=manualLookup)
  refresh = Button(manualFrame, text="Reset", height=5, width=30,fg="#ffffff", bg="#703f3f", command=refreshList)

  airlineMenu.config(width=20, height=5)
  originMenu.config(width=20, height=5)
  destinationMenu.config(width=20, height=5)
  planeMenu.config(width=20, height=5)

  airlineMenu.grid(row = 2, column = 1,sticky=(E), padx=5, pady=5)
  originMenu.grid(row = 2, column = 2,sticky=(E) ,padx=5, pady=5)
  destinationMenu.grid(row = 2, column = 3,sticky=(E), padx=5, pady=5)
  planeMenu.grid(row = 2, column = 4,sticky=(E), padx=5, pady=5)
  generate.grid(column=0,row=3,columnspan=4, padx=5, pady=5, sticky=(W,E))
  refresh.grid(column=4,row=3,columnspan=2, padx=5, pady=5, sticky=(W,E))



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

label.grid(column=0, row=0, columnspan=2, sticky=W+E)
auto.grid(column=0, row=1, padx=5, pady=5)
manual.grid(column=1, row=1, padx=5, pady=5)
exitApp.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky=W+E)


# # Test and Validation code
# DF = pd.read_csv("test_data.csv")
# testDF = theAlgorithm(DF)
# testDF.to_csv("test_results.csv")

master.mainloop()