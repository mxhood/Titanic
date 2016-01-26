# Daniela Kreimerman and Maxine Hood
# CS111 PS06
# 10/17/15
# titanic.py

from pylab import *

def getKey(s):
    '''Returns that portion of string s to the left of the first equal
    sign, with flanking white space removed.'''
    s=s.strip()  #removes white space
    s=s.split('=')  #creates list through sepeating string by '='
    return str(s[0])    #returns key
    
#print getKey(' age=28.0 ')

def getValue(s):
    '''Returns that portion of string s to the right of the first
    equal sign, with flanking white space removed.'''
    s=s.strip()  #remomves white space
    s=s.split('=')  #creates list through sepeating string by '='
    return str(s[1]) #returns value

#print getValue(' job=Saloon Steward\n')

def passengerDictionaryFromLine(line): 
    '''Given a line describing a passenger from the Titanic database, returns a 
    dictionary of information about this passenger. Each such dictionary has
    possible keys "name", "status" (survivor or victim), "age", "class", and 
    "job", whose values contain information about the passenger. 
    
    For example, for the line 
      "Miss Eugenie Baclini (survivor); age=3.0; class=3rd Class"
    the returned dictionary would be:
      {'name': 'Miss Eugenie Baclini',
       'status': 'survivor',
       'age': '3.0',
       'class': '3rd Class'}
         
    For the line 
      "Mr Ernest Owen Abbott (victim); age=21.0; class=Victualling; job=Lounge Pantry Steward"
    the returned dictionary would be: 
      {'name': 'Mr Ernest Owen Abbott',
       'status': 'victim',
       'age': '21.0',
       'class': 'Victualling',
       'job': 'Lounge Pantry Steward'}
    
    For the line
      'Master Georges Youssef ("George Thomas") Touma (survivor); age=8.0; class=3rd Class\n'
    the returned dictionary would be:    
      {'age': '8.0',
       'class': '3rd Class',
       'name': 'Master Georges Youssef ("George Thomas") Touma',
       'status': 'survivor'} 
       
    Note that not every line has every key. For example, two of the above
    three lines do not have a job field, and so the resulting dictionaries
    do not contain the key "job".
     
    Also note that the first component of a line may contain parentheses other 
    than the ones in "(survivor)" or "(victim)".

    Finally, note that this function should work correctly whether or not the
    given line ends in a newline.'''
    line=line.strip()    #removes white space
    line=line.split(';') #splits str to create liist by ';'
    info={getKey(section): getValue(section) for section in line[1:]} #dict. comp.
    info['status']='victim'  #default status
    info['name']=line[0].strip(' (victim)') #gets everything in name but status
    if 'survivor' in line[0]:  #same as above but for survivor
        info['status']='survivor'
        info['name']=line[0].strip(' (survivor)')
    return info
    
        
#print passengerDictionaryFromLine("Miss Eugenie Baclini (survivor); age=3.0; class=3rd Class")
#print passengerDictionaryFromLine("Mr Ernest Owen Abbott (victim); age=21.0; class=Victualling; job=Lounge Pantry Steward")
#print passengerDictionaryFromLine('Master Georges Youssef ("George Thomas") Touma (survivor); age=8.0; class=3rd Class\n')

def createListOfTitanicPassengers(fileName):
    '''Returns a list of passenger dictionaries, where each element of the
    list is created by calling passengerDictionaryFromLine on a line from 
    the specified file.'''
    files = open(fileName,'r')  #opens file
    lines = files.readlines()   #reads file
    return [passengerDictionaryFromLine(line) for line in lines] #l.c. for pass dict.
    
passengerList = createListOfTitanicPassengers('titanic.txt')
#print len(passengerList)
#print passengerList[2168]
#print passengerList[254]
#print passengerList[2018]

#---------------------------Task 2b---------------------------------------------
def topJobs(num, passengers):
    '''Assume that num is a nonnegative integer and passengers is a list of 
    passenger dictionaries.  Returns a list of num pairs of the form 
    (jobName, jobFrequency), where jobName is the name of a job and jobFrequency 
    is the number of passengers with that job.  These pairs should be the top num 
    most popular jobs, sorted by frequency from highest to lowest. If num is 
    greater than the total number of jobs, a list of all job pairs should be 
    returned.  Some passenger dictionaries have no jobs; these should not be 
    included in the results.'''
    jobDict={} #creates empty dict
    for passDict in passengers: #for each dict. in list of dict.
        if 'job' in passDict:  #if key job is in dict.
            if passDict['job'] not in jobDict: #if job not in jobdict
                jobDict[passDict['job']]=1   #add to jobdict and value=1
            else:
                jobDict[passDict['job']]+=1  #add one to value
    jobList=sorted(jobDict.items())  #sort items
    jobList=[(job[1],job[0]) for job in jobList] #creates list of tuples 
    jobList=sorted(jobList)   #sort list by job[1]
    jobList=[(job[1],job[0]) for job in jobList] #creates list of tuples
    jobList.reverse()  #reverse job list
    return jobList[:num+1]  #return job list from begining(most) to num given

#print 'topJobs(25, passengerList)
#print 'len(topJobs(2500, passengerList))

#---------------------------task 2c---------------------------------------------

def createSurvivalDictionary(passengers):
    '''Given a list of passenger dictionaries, returns a dictionary whose
    keys are all the cabin classes that appear in passengers. The value
    associated with the cabin class name in this resulting dictionary should
    itself be another dictionary that has three key/value pairs: 
      (1) The key "survivors" maps to the number of survivors in that cabin class;
      (2) The key "victims" maps to the number of victims in that cabin class;
      (3) The key "survivalRate" maps to the survival rate in that cabin class
#          (a floating point number rounded to 3 decimal digits)'''
    classesDict={'1st Class':{'survivalRate':0,'survivors':0,'victims':0},
            '2nd Class':{'survivalRate':0,'survivors':0,'victims':0},
            '3rd Class':{'survivalRate':0,'survivors':0,'victims':0}, 
            'A la Carte':{'survivalRate':0,'survivors':0,'victims':0},
            'Deck':{'survivalRate':0,'survivors':0,'victims':0}, 
            'Engine':{'survivalRate':0,'survivors':0,'victims':0},
            'Victualling':{'survivalRate':0,'survivors':0,'victims':0}}
    for passDict in passengers:  #^^creates dict with blank values
        if passDict['status']=='survivor': #if status is survivor
            classesDict[passDict['class']]['survivors']+=1 #adds 1 to value
        elif passDict['status']=='victim': #if status is victim
            classesDict[passDict['class']]['victims']+=1 #adds 1 to value
    for key in classesDict: #for each key in classdict
        classesDict[key]['survivalRate']=round(float(classesDict[key]['survivors'])
                                                /(classesDict[key]['victims']+classesDict[key]['survivors']),3)
    return classesDict  #^calculates the survival rate

#print createSurvivalDictionary(passengerList)

#-----------------------------Task 2d-------------------------------------------

def barChartOfPercentages(tuples, chartTitle, xtitle, ytitle):
    '''Given an (unsorted) list of tuples, each containing a percentage
    (a floating point value between 0.0 and 1.0) and a string, generates a 
    horizontal bar chart, where the highest percentages are shown at the top 
    and others follow in decreasing order. The chartTitle, xtitle, and 
    ytitle are used for labeling the graph. The strings of the tuples are 
    used as ytick labels.'''
    title(chartTitle) #creates title
    xlabel(xtitle)    #creates y label
    ylabel(ytitle)    #creates x label
    tuples.sort()     #sorts the tuples given
    position=range(len(tuples)) 
    data=[eachTuple[0] for eachTuple in tuples] #creates list of percentage
    yTitles=[eachTuple[1] for eachTuple in tuples] #creates list of string
    yticks(position,yTitles) #creates y ticks
    barh(position,data,0.5,color='green',align='center')
    show()

def barChartOfSurvivalRates(passengers): 
    '''Given a list of passenger dictionaries, displays a horizontal bar chart 
    of the sorted percentage of survival rates for each cabin class.'''
    survivalDict=createSurvivalDictionary(passengers) #below: list of tuples of rate then key
    survivalTuples=[(survivalDict[key]['survivalRate'],key) for key in survivalDict]
    barChartOfPercentages(survivalTuples,'Survival rate on Titanic, by class of passenger/crew',
                            'percent survivors','cabin class')
    
#barChartOfSurvivalRates(passengerList)

#------------------------------Task 2e------------------------------------------

def pieChartFromOccurrenceDictionary(occDict):
    '''Assume occDict is an occurrence dictionary maps labels (strings) to 
    occurrences (nonnegative integers). Displays a pie chart illustrating the 
    relative number of occurrences for each label. Pie slices should be
    labeled by the labels, and ordered clockwise from smallest pie slice 
    to largest pie slice starting at 12 o'clock.'''
    figure(1, figsize=(6,6), facecolor='white') 
    occTuples=[(occDict[key],key) for key in occDict] #creates list of tuples: int, string
    occTuples.sort() #sorts tuples by int
    occTuples.reverse() #reverses order
    occValues=[eachTuple[0] for eachTuple in occTuples] #creates list of values
    occKeys=[eachTuple[1] for eachTuple in occTuples] #creates list of keys
    pie(occValues,labels=occKeys,startangle=90) #puts it all together to make chart
    show()

def pieChartOfVictimsCabinClasses(passengers):
    '''Given a list of passenger dictionaries, displays a pie chart showing
    the relative number of victims from each cabin class.'''
    survivalDict=createSurvivalDictionary(passengers)
    victimsDict={key:survivalDict[key]['victims'] for key in survivalDict}
    pieChartFromOccurrenceDictionary(victimsDict) #^^creates dict of class and num of vict.

#pieChartOfVictimsCabinClasses(passengerList)

#-------------------------------Task 2f-----------------------------------------

def getListOfSurvivorsAges(passengers):
    '''Given a list of passenger dictionaries, returns a new list consisting of 
    the ages of all the survivors. For example, if there were three survivors 
    aged 25.0, then three of the entries in the returned list should have value 
    25.0. Note that the returned list is a list of floating point numbers,
    not strings.'''
    return [float(passDict['age']) for passDict in passengers if ('age' in passDict) and (passDict['status']=='survivor')]
    #^^creates list of all ages via list comp. and if passenger gives age and if survived

def histogram(data, numberOfBins):
    '''Assume data is a list of non-negative floating point numbers and 
    numberOfBins is the number of equal-sized bins in which to partition the 
    numbers. Define the "data width" of the data to be one more than the maximum 
    data element. Then each of the equally-sized bins has a bin width that is 
    the data width divded by numberOfBins. Assume these bins are indexed from 
    0 to (numberOfBins - 1). Then the histogram function returns a new list 
    whose length is numberOfBins and whose ith slot contains the number of 
    data elements in the ith bin. 

    For example, suppose L is the list [8.0, 19.0, 3.0, 6.0, 12.0, 7.0].
    The data width of L is 20.0. 
    
    If numberOfBins is 1, then this one bin covers the half-open interval
    [0.0, 20.0) and contains all 6 elements from the list. (In the half-open 
    interval notation [lo, hi), the interval ranges from lo up to, but not 
    including, hi.) So the result of histogram (L, 1) is [6]. 
    
    If numberOfBins is 2, then there are two bins, each with bin width 10.0. 
    The bin at index 0 covers the half-open interval [0.0, 10.0), which contains 
    the 4 numbers 8.0, 3.0, 6.0, and 7.0, and the bin at index 1 covers the 
    half-open interval [10.0, 20.0), which contains the two numbers 19.0 and 
    12.0. So the result of histogram(L, 2) is [4, 2]. 
    
    If numberOfBins is 3, there are three bins, which cover half-open intervals
    [0, 6.66), [6.66, 13.33), and [13.33, 20) that contain 2, 3, and 1 elements
    from the list, respectively. So the result of histogram(L, 3) is 
    [2, 3, 1]. 
    
    In a similar fashion, 
    * histogram(L, 4) results in the list [1, 3, 1, 1].
    * histogram(L, 5) results in the list [1, 2, 1, 1, 1].
    * histogram(L, 6) results in the list [1, 1, 2, 1, 0, 1]
    * histogram(L, 7) results in the list [0, 1, 3, 0, 1, 0, 1]
    '''
    dataWidth=max(data)+1  #calc. datawidth via isntructions given
    binWidth=dataWidth/numberOfBins #given in instructions
    resultList=[0 for num in range(numberOfBins)] #creates correct length list with values=0
    for num in data: #for each number in data(given)
        binNum=int(num/binWidth)
        resultList[binNum]+=1
    return resultList

L=[8.0, 19.0, 3.0, 6.0, 12.0, 7.0]    
#print histogram(L,7)

def barChartOfHistogram(hist, maximum, chartTitle, xtitle, ytitle):
    '''Given a list corresponding to a histogram for a set of data and given 
    the maximum value of the data, displays a vertical bar chart of the 
    histogram. The chart has the specified title. X-axis labels corresponding
    to the interval ranges of the histogram are optional.'''
    title(chartTitle) #creates title
    xlabel(xtitle)    #creates x label
    ylabel(ytitle)    #creates y label
    position=range(len(hist))
    binwidth=maximum/len(hist)  #for use in xtitles
    initialTitle=binwidth/2  #firt x title 
    xTitles=[initialTitle+(binwidth*num) for num in range(len(hist))] #OPTIONAL list of xtitles
    xticks(position,xTitles)
    bar(position,hist,0.5,color='green',align='center') #creates bar graph
    show()


def barChartOfSurvivorsAges(passengers, numberOfAgeGroups):
    '''Given a list of passenger dictionaries, displays a vertical bar chart
    that illustrates the number of survivors in each of the given number of
    equally-sized age groups.'''
    passAges=getListOfSurvivorsAges(passengers) #get list of passages
    hist=histogram(passAges,numberOfAgeGroups) #get data for bar graph
    barChartOfHistogram(hist,max(passAges),'Age Distribution of Titanic survivors','Age','Counts')
    #^^make bar graph

barChartOfSurvivorsAges(passengerList, 12)




