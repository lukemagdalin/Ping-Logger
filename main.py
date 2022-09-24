from socket import gethostbyname
from pythonping import ping
from datetime import date
import time
import sys
import os

host = "google.com"
size = 40
iterations = 200
delayMs = 100 # ms

directory = "results\\" + host # do not change, probably will break

def main():
    ''' Main function '''
    #generate a filename
    filename = generateFilename(host)
    # loop until stopped by user
    for i in range(1, iterations):
        time.sleep(delayMs/1000)
        # ping the host
        results = str(pingHost(host, size)) + " " + str(delayMs)
        # save the results to a file
        print(results)
        appendToFile(results, filename)

def generateFilename(host):
    '''Generate a filename from a hostname
    :param host: Hostname
    :return: Filename'''
    filename = ""
    exists = True
    i = 0
    while (exists == True):
        today = date.today().strftime('%Y-%m-%d')
        filename = "Results_" + host + "_" + today + "(" + str(i) + ").txt"
        if(checkIfFilenameExists(filename)):
            i += 1
        else:
            exists = False
    return filename

def checkIfFilenameExists(filename):
    '''Check if a file exists
    :param filename: Filename to check
    :return: Boolean'''
    try:
        with open(directory + "\\" + filename, 'r') as f:
            return True
    except FileNotFoundError:
        return False

# Testing custom save directories
def checkIfDirExists(dir):
    '''Check if a directory exists
    :param dir: Directory to check
    :return: Boolean'''
    if os.path.isdir(dir):
        return True
    else:
        return False

def createDir(dir):
    '''Create a directory
    :param dir: Directory to create'''
    try:
        os.mkdir(dir)
    except OSError:
        print("Creation of the directory %s failed, exiting" % dir)
        sys.exit()
    else:
        print("Successfully created the directory %s " % dir)
    
def appendToFile(string, filename):
    '''Append a string to a file
    :param string: String to append
    :param filename: Filename to append to'''
    if(checkIfDirExists(directory) != True):
        createDir(directory)
    with open(directory + "\\" + filename, 'a') as f:
        f.write(string + "\n")

def pingHost(host, size):
    '''Ping a host and return the response time in ms
    :param host: Hostname or IP address
    :param size: Size of the packet to send
    :return: Address, Response time in ms'''
    address = gethostbyname(host)
    response_list = ping(host, size=size)
    for response in response_list:
        if(response.success):
            results = address + " " + str(response.time_elapsed_ms)
        else:
            print(response.error_message)
            results = address + " " + str(False)
    return results 
        
main()