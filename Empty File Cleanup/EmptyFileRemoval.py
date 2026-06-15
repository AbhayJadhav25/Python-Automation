import sys
import os
import time
import schedule
import smtplib as s


def DeleteEmptyFiles(DirectoryName):

  if(not(os.path.exists(DirectoryName))):
    print("No such Directory is Avilable.")
    return
  
  if(not(os.path.isdir(DirectoryName))):
    print("Unable to Scan. This is Not a Directory.")
    return
  
  Border = "-"*50
  CurrentTime = time.ctime()
  FileName = "Report%s.log" %(CurrentTime)
  FileName = FileName.replace(":","_")
  FileName = FileName.replace(" ","_")
  Fobj = open(FileName , "w")
  Fobj.write(Border)
  Fobj.write("-"*11+"Remove Empty File Automation"+"-"*11)
  Fobj.write("Start Scanning at "+CurrentTime+"\n")

  
  FileCount = 0 
  EmptyFiles = 0
  for Folder , subFolder , File in os.walk(DirectoryName):

    for Fname in File:

      Fname = os.path.join(Folder , Fname)
      Fsize = os.path.getsize(Fname)
      FileCount+=1
      if(Fsize == 0):
        os.remove(Fname)
        EmptyFiles+=1
  Fobj.write("Total Files = "+str(FileCount)+"\n")
  Fobj.write("Total Empty Files = "+str(EmptyFiles)+"\n")
  Fobj.write("This Log is Created at "+time.ctime()+"\n")
  Fobj.write("-"*20+"Thank You!"+"-"*20+"\n")
  Fobj.write(Border+"\n")

def main():

  if(len(sys.argv)!=2):
    print("Invalid Number of Arguments.")
    print("Please specify the name of Directory.")
    return
  
  schedule.every().minute.do(lambda: DeleteEmptyFiles(sys.argv[1]))

  while(True):
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
  main()