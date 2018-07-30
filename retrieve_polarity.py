import glob
import collections
from datetime import datetime

########################################################################
########################################################################
# In order to use this script, set your opinionfinder's text files as: #
#  - in the first line add timestamp data                              #
#  - after add the comment                                             #
########################################################################
########################################################################

# insert path of your opinionfinder project
path = "data_sentiment"

# take all subjclueslen1polar files
files_scraped = glob.glob(path + "/*/subjclueslen1polar")
# take all comments in order to find timestamp date
files_scraped2 = glob.glob(path + "/*/")
files_scraped3 = []


for f in files_scraped2:
    files_scraped3.append(f[:f.find("_auto")])

ff = zip(files_scraped, files_scraped3) #list of tuple

list_of_mood = []
#for all file in the directory
for files in ff:
   #print files
   file = open(files[0], "r")
   countPolarity = 0
   count_number = 0
   c_d = open(files[1], "r")

   tmp_datetime = c_d.readline()
   comment_date = datetime.fromtimestamp(float(tmp_datetime))

   #print comment_date
   year = comment_date.strftime('%Y%m')[:4]
   month = comment_date.strftime('%Y%m')[4:6]

   lines =file.readlines()
   # analyze polarity
   for line in lines:
   		l = line[line.find('mpqapolarity="')+14:(len(line)-3)]
   		if l == "strongneg":
   			countPolarity = countPolarity - 2
   			count_number += 1
   		elif l == "weakneg":
   			countPolarity = countPolarity - 1
   			count_number += 1
   		elif l == "neutral":
            # don't count neutral polarity (for means)
   			countPolarity = countPolarity + 0
   		elif l == "weakpos":
   			countPolarity = countPolarity + 1
   			count_number += 1
   		elif l == "strongpos":
   			countPolarity = countPolarity + 2
   			count_number += 1

   if count_number == 0: # if we don't have comments
   	list_of_mood.append( str(year) + "-" + str(month) + " " + "0" )
   else: # means
      list_of_mood.append( str(year) + "-" + str(month) + " " + str( float(countPolarity) / int(count_number) ) )


######################################################################
######################################################################
#                  print data aggregated by month                    #
######################################################################
######################################################################
somma = {}
count = {}

s_n = 0
w_n = 0
n = 0
w_p = 0
s_p = 0

for x in sorted(list_of_mood):
   # take date from list_of_mood
   key = x[:7]
   if x[:4] == "2018":
      if float(x[7:]) > 0:
         s_p += 1
      if float(x[7:]) == 0:
         n += 1
      if float(x[7:]) < 0:
         s_n += 1

   if not key in somma.keys():
      somma[key] = 0
      count[key] = 0


   somma[key] += float(x[7:])
   count[key] += 1

print s_p
print n
print s_n

for key, values in somma.iteritems():
   somma[key] /= count[key]

start = sorted(list_of_mood)[0][:7].split("-")
end = sorted(list_of_mood)[-1][:7].split("-")
#print end
start_year = int(start[0])
start_month = int(start[1])

end_year = int(end[0])
end_month = int(end[1])

while (start_year != end_year) or (start_month != end_month):
   key = "%d-%02d" %(start_year,start_month)

   if not key in somma.keys():
      somma[key] = 0
   start_month += 1
   if start_month > 12:
      start_month = 1
      start_year += 1

for key in sorted(somma):
   print str(key) + " " + str(somma[key]).replace(".",",")
