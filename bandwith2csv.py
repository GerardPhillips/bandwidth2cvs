
switchList = ['192.168.0.16', '192.168.0.17','7150S-1']
username = 'admin'
password = 'admin'
bandwithItems = ["inBitsRate", "outBitsRate"]

def getDate():
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    return(d1)    
    
def prettyBW(bps):
    return str(bps/1000000000) + "G"
	
def percentUtilised(bps, bw):
    temp = str(round(100.0*bps/bw,2)) + "%"	
    #print bps, " ", bw, " ", temp 
    return (temp)	
	

###############################################################
#
# main code
# Read interface info from the list of switches above
# Create a .csv file per switch
#
##############################################################
from jsonrpclib import Server
import pprint
import json 
import csv 
from datetime import date




def main():
    
    today = getDate()
    print "bandwidth2csv running: ", today
  
    cvsBanner = "Port,Speed,Description,In Mbps, In %, Out Mbps, Out %"

    for switch in switchList:
        print "Processing: " + switch
        # create a file per switch
        thisFile = today + "_" + str(switch) + ".csv"
        data_file = open(thisFile, 'w') 
        data_file.write(cvsBanner+"\n")
        
        # open the eAPI connection
        serverString = "http://" + username + ":" + password + "@" + switch + "/command-api"
        object = Server( serverString )         
        
        # Get the current show int    
        response = object.runCmds( 1, [ "enable", "show interfaces"])    
                 
        # Format and print per interface
        temp = response[1]['interfaces']
        
        for interface in response[1]['interfaces']:
            #print interface
            if 'hardware' in response[1]['interfaces'][interface].keys():
                if response[1]['interfaces'][interface]['hardware'] == 'ethernet':
                    #print "interfaceStatistics"
                    if response[1]['interfaces'][interface]['interfaceStatus'] == 'connected':
                        line = str(interface) + "," + response[1]['interfaces'][interface]['description'] + "," + prettyBW(response[1]['interfaces'][interface]['bandwidth'])
                        #print(line)
                        for key in bandwithItems:
                            #print key, temp[interface]['interfaceStatistics'][key]
                            line = line + "," + str(round(response[1]['interfaces'][interface]['interfaceStatistics'][key]/1000000,2)) + "," + percentUtilised(response[1]['interfaces'][interface]['interfaceStatistics'][key], response[1]['interfaces'][interface]['bandwidth'])
                            #print (line)
                        
                        data_file.write(line+"\n")
        
        data_file.close()        
if __name__ == "__main__":
    main()
