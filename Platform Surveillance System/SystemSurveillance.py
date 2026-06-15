#Command line Input.

import psutil
import sys
import os
import time
import schedule

def CreateLog(FolderName):
  Border = "-"*50
  Ret = False
  Ret = os.path.exists(FolderName)

  if Ret:
    Ret = os.path.isdir(FolderName)
    if Ret == False:
      print("Unable to create folder.")
      
  else:
    os.mkdir(FolderName)
    print("Directory for logs create successfullly.")
  
  timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
  
  FileName = os.path.join(FolderName , "Report_%s.log" %timestamp)
  # print("logs file gets created with name  :  ",FileName) 
  
  fobj = open(FileName , "w")
  
  fobj.write(Border+"\n")
  fobj.write("--------Platform Surveillance System--------\n")
  fobj.write("Log Created at : "+time.ctime()+"\n")
  fobj.write(Border+"\n\n")

  fobj.write("----------System Report-------------\n")

  # print("CPU Usage : ",psutil.cpu_percent())
  fobj.write("CPU Usage : %s %%\n" %psutil.cpu_percent())
  fobj.write(Border+"\n")

  mem = psutil.virtual_memory()
  # print("RAM Usage : " , psutil.percent())
  fobj.write(Border+"\n")
  fobj.write("RAM Usage : %s %%\n" %mem.percent)
  fobj.write(Border+"\n")
  fobj.write("\n Disk Usage Report \n")

  for part in psutil.disk_partitions():
    try:
      usage = psutil.disk_usage(part.mountpoint)
      # print(f"{part.mountpoint} used {usage.percent}%")
      fobj.write("%s --> %s %% used\n" %(part.mountpoint , usage.percent))
    except:
      pass
  fobj.write(Border+"\n")

  net = psutil.net_io_counters()
  fobj.write("\nNetwork Usage Report\n")
  fobj.write("Sent : %.2f MB\n" %(net.bytes_sent / (1024*1024)))
  fobj.write("Received : %.2f MB\n" %(net.bytes_recv / (1024*1024)))
  fobj.write("\n"*15)

  #pr

  Data = ProcessScan()
  for info in Data:
    fobj.write("PID : %s\n" %info.get("pid"))
    fobj.write("Name : %s\n" %info.get("name"))
    fobj.write("Username : %s\n" %info.get("username"))
    fobj.write("Status : %s\n" %info.get("status"))
    fobj.write("Start Time  : %s\n" %info.get("create_time"))
    fobj.write("CPU %% : %.2f\n" %info.get("cpu_percent"))
    fobj.write("Memory percent %% : %.2f\n" %info.get("Memory_percent"))
    fobj.write(Border+"\n")
  fobj.write(Border+"\n")
  fobj.write("--------------End Of Log File------------------")
  fobj.write(Border+"\n")  
  
  fobj.close()
  
def ProcessScan():
  listProcess = []

  #Warm up for CPU percent
  for proc in psutil.process_iter():
    try:
      proc.cpu_percent()
    except:
      pass
  
  time.sleep(0.2)

  for proc in psutil.process_iter():
    try:
     info = proc.as_dict(attrs = ["pid" , "name"  ,"username", "status" , "create_time" ])
     #Convert create_time
     try:
      info["create_time"] = time.strftime("%Y-%m-%d %H:%m:%S" , time.localtime(info["create_time"]))
     except:
        info["create_time"] = "NA"
     info["cpu_percent"] = proc.cpu_percent(None)
     info["Memory_percent"] = proc.memory_percent()

     listProcess.append(info)
    except (psutil.NoSuchProcess , psutil.AccessDenied , psutil.ZombieProcess):
      pass
  return listProcess

def main():
  
  if(len(sys.argv) == 2):
    if(sys.argv[1]=="--h" or sys.argv[1]=="--H"):
      print("This script is used to : ")
      print("1 : Create automatic logs")
      print("2 : Execute perodically")
      print("3 : Sends mail with the log.")
      print("4 : Store information about processes")
      print("5 : Store information about CPU")
      print("6 : Store information about RAM usage")
      print("7 : Store information about RAM secondary storage.")
    
    elif(sys.argv[1]=="--u" or sys.argv[1]=="--U"):
      print(f"Use the automation script as \nScriptName.py Timeinterval DirectoryName\nTimeinterval : The time in minutes for periodic scheduling\nDirectoryName : NAme of directory to create auto logs.\n")
      
    else :
      print("Unable to proceed as there is no such option.")
      print("Please use --h or --u to get more details.")

  #python Demo.py 5 directory
  elif(len(sys.argv)==3):
    
    #Apply the scheduler
    schedule.every(int(sys.argv[1])).seconds.do(CreateLog , sys.argv[2])

    #wait till abort.
    while True:
      schedule.run_pending()
      time.sleep(1)
  else:
    print("Invalid Number of command line arguments.")
    print("Unable to proceed as there is no such option.")
    print("Please use --h or --u to get more details.")

if __name__ == "__main__":
  main()