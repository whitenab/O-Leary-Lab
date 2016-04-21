import statistics
import math
import csv
import glob
import os
from matplotlib import pyplot as plt
from natsort import natsorted

"""Column Values"""
volts = 0
amps = 1
gauss = 2
khz = 3
g2 = 4
sdg2 = 5
amp2 = 6
var2 = 7
amp1 = 8
var1 = 9

g2in_fn = 1
g2ot_fn = 2
eit_fn = 3

g2inFile = 'G2IN Compilation'
g2otFile = 'G2OT Compilation'
eitrawFile = 'EIT no sum Compilation'
eitsumFile = 'EIT sum Compilation'
nmorFile = 'NMOR Compilation'

outputfolder = '\\Data Ouput' #For Saving Data to

"""File Parsing Section"""
#Gather all files names
#.csv.xls for this particular situation 
#Add an extension chooser   !
def globbing():
    return glob.glob('./*.csv.xls')

#Clean up file names for use in get g2
def clean_glob():
    dirty = globbing()
    clean = []
    for dirt in dirty:
        clean.append(dirt[2:])
    clean = natsorted(clean)
    return clean
    
def sort_glob(unsorted):
    return natsorted(unsorted)
    
#Read Entire File in to memory
def read_file(a):
    with open(a,'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        next(reader)
        next(reader)
        next(reader)
        rows = [r for r in reader]
    return rows

def raw_files():
    allfiles = []
    for name in clean_glob():
        allfiles.append(read_file(name))
    return allfiles
    
def select_files(inoteit):
    allfiles = raw_files()
    specfiles = []
    count = 1
    filenum = inoteit
    for file in allfiles:
        if count == filenum:
            specfiles.append(file)
            filenum +=3
        count +=1
    return specfiles

"""File Writing Section"""

def write_file(name, data):
    where = os.getcwd() + '\\' + outputfolder + '\\' + name + '.csv'
    with open(where,'w') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',',lineterminator = '\n')
        for row in data:
            writer.writerow(row)
        
    
#takes read_file stuff
#takes raw_files()
# x = khz or similar
# y = g2 or EIT or similar

            
        
"""Data Gathering Section"""
#Gets data from full data intake in read_file
#Data - 
def get_data(data,x,y):
    file_info = []
    for i in data:
        file_info.append([float(i[x]),float(i[y])])
    col1 = [row[0] for row in file_info]
    col2 = [row[1] for row in file_info]
   # print(col1)
   # print(col2)
    return list(zip(col1,col2))
    
#Send zipped list of x's and y's
def graph(data):
    data = list(zip(*data))
    plt.plot(data[0],data[1])
    plt.xlim([-10,10])
    plt.ylim([-1,1])
    plt.show()
 
   
def gather_all_g2_in():
    #all files in directory read 
    allg2 = []
    #For files - Get G2IN & kHz
    for name in clean_glob():
        allg2.append(get_data(read_file(name),khz,g2))
    return allg2

"""Do Some Calcs"""
def assemble(data,x,y): 
    output = [[] for y in range(0,len(data[0]))]
    count = 0
    for sets in data:
        for row in sets:
            output[count].append(float(row[x]))
            output[count].append(float(row[y]))
            count += 1
        count = 0
    return output
#data = raw_files() data
#x = khz or similar
#y = amp1
#z = amp2
def EITsum_assemble(data,x,y,z):
    output = [[] for y in range(0,len(data[0]))]
    count = 0
    
    for sets in data:
        for row in sets:
            output[count].append(float(row[x]))
            output[count].append(float(row[y])+float(row[z]))
            count += 1
        count = 0
    return output
    
def nmor_assemble(data,x,y,z):
    output = [[] for y in range(0,len(data[0]))]
    count = 0
    for sets in data:
        for row in sets:
            output[count].append(row[x])
            output[count].append(math.asin((float(row[y])+float(row[z])/(float(row[y])-float(row[z])))))
            count += 1
        count = 0
    return output
    
def make_folder():
    where = os.getcwd()
    newpath = (where + outputfolder)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        
"""Run It!"""

def run_it():
    make_folder()
    write_file(g2inFile,assemble(select_files(g2in_fn),khz,g2))
    write_file(g2otFile,assemble(select_files(g2ot_fn),khz,g2))
    write_file(eitsumFile,EITsum_assemble(select_files(eit_fn),khz,amp1,amp2))
   # write_file(nmorFile,nmor_assemble(select_files(eit_fn),khz,amp1,amp2))
    