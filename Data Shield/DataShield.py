import sys
import os
import time
import schedule
import shutil 
import hashlib
import zipfile

def make_zip(folder):
    timstamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    zip_name = folder+"_"+timstamp+".zip"

    #open the zip.
    zobj = zipfile.ZipFile(zip_name , 'w' , zipfile.ZIP_DEFLATED)
    
    for root , dirs , files in os.walk(folder):

        for file in files:
            full_path = os.path.join(root , file )
            relative = os.path.relpath(full_path , folder)

            zobj.write(full_path , relative)

    zobj.close()
    return zip_name
def calculate_hash(path):
    hobj = hashlib.md5()

    fobj = open(path , "rb")

    while True:
        data = fobj.read(1024)
        if not data:
            break
        else:
            hobj.update(data)
    
    fobj.close()

    return hobj.hexdigest()

def BackUpFiles(Source, Destination):
    copied_Files = []
    print("Creatting the Backup folder for the backup Process")

    os.makedirs(Destination,exist_ok= True)# for multiple folders (If forder is created go ahead (exist_ok = True))

    for root, dirs, files in os.walk(Source):
        for file in files:
            src_path = os.path.join(root,file)

            relative = os.path.relpath(src_path,Source)
            dest_path = os.path.join(Destination,relative)

            os.makedirs(os.path.dirname(dest_path),exist_ok = True)

            # Copy the files if its new / update
            if(not(os.path.exists(dest_path)) or (calculate_hash(src_path) != calculate_hash(dest_path))):
                shutil.copy2(src_path,dest_path)
                copied_Files.append(relative)
    
    return copied_Files

    
def DataShield(Source = "Data"):  
    Border = "-"*50
    BackupName = "Backup"
    print(Border)  

    print("BackUpProcess Started Succsefully at :",time.ctime())
    print(Border)  
    
    files = BackUpFiles(Source,BackupName)

    zip_file = make_zip(BackupName)
    print(Border)  

    print("Backup completed Successfully.")
    print("Files Copied : ",len(files))
    print("Zip Files grt created : ",zip_file)

    print(Border)  

def main():

    Border = "-"*50
    print(Border)
    print("------  Data Shield System -------")
    print(Border)

    if(len(sys.argv) == 2):
        if(sys.argv[1] == "--h" or sys.argv[1] == "--H"):
            print("This scipt is used to : ")
            print("1 : Text auto backup at given time")
            print("2 : Backup only new and updated files ")
            print("3 : Create and archive of the backup periodically")


        elif(sys.argv[1] == "--u" or sys.argv[1] == "--U"):
            print("Use the automation script as")
            print("ScriptName.py TimeInterval SourceDirectory")
            print("TimeInterval : The time in minutes for periodic scheduling")
            print("SourceDirectory : Name of directory to backed up")

        else:
            print("Unable to proceed as there is no such option")
            print("Please use --h or --u to get more details")
    
    # python Demo.py 5 Data 
    elif(len(sys.argv) == 3):
        print("Inside projects logic")
        print("Time interval : ",sys.argv[1])
        print("Directory name : ",sys.argv[2])

        # Apply the schedular
        schedule.every(int(sys.argv[1])).seconds.do(DataShield, sys.argv[2])
        print(Border)
        print("Data Sheild  System started succesfully")
        print("Time interval in minutes: ",sys.argv[1])
        print("Press Ctrl + C to stop the execution")
        print(Border)
        # Wait till abort
        while True:
            schedule.run_pending()
            time.sleep(1)

    else:
        print("Invalid number of command line arguments")
        print("Unable to proceed as there is no such option")
        print("Please use --h or --u to get more details") 

    print(Border)
    print("--------- Thank you for using our script ---------")
    print(Border)
    
if __name__ == "__main__":
    main()