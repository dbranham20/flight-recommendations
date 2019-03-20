# flight-recommendations
A python GUI that recommends flights by carrier based on data given for South Carolina and North Carolina in 2018

## Intial Run
The first time this project is run with `python3 main.py`, the program should read from the larger dataset 
and create the smaller one. Every run after that should read from the smaller data set file and not need the larger one. 
This is done to decrease the reading and compute time required on larger .csv files. 

## Algorithm Explanation
The algorithm used for the auto selection of flights by month is 
quite simple, but effective nonetheless.

The algorithm calculates the percentage, from 0 to 1, of successfully completed 
flights based off of the original columns "DEPARTURES_PERFORMED" and 
"DEPARTURES_SCHEDULED." The average of this score is calculated for each month and
is multipled by 50, to represent the fact that it is worth half of the final score calculated.

The second part of the algorithm is made up of the percentage, from 0 to 1, of the available
seats on each plane. This is based off of the original columns "SEATS" and "PASSENGERS." The
average of this score is calculated for each month and is multiplied by -50, because the higher 
the percentage, the less seats available which, in my opinion, should bring the overall month rank down.

These two total scores are added together to make a final "Algorithm Rank" and then sorted by highest
score. I decided to make the final score "out of 20" because the highest score was ~16 and 20 could be
close enough, but far enough away for the "perfect" score.

In the final version of my project, I hope to keep the algorithm score for each month, but since the 
module used to display the info is a "treeview", I hope to allow each month to be expandable to also
show the top 10 recommended flights for that month as well.
