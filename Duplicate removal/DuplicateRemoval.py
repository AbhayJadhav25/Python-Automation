import hashlib
import os 

import time

def CreateLog(DeletedFiles):
    
    CurrentTime = time.ctime()

    LogFile = "DuplicateFileReport_%s.log" % CurrentTime
    LogFile = LogFile.replace(":", "_")
    LogFile = LogFile.replace(" ", "_")

    Border = "-" * 50

    with open(LogFile, "w") as Fobj:

        Fobj.write(Border + "\n")
        Fobj.write("Duplicate File Cleaner Report\n")
        Fobj.write(Border + "\n")

        Fobj.write("Execution Time : %s\n\n" % CurrentTime)

        Fobj.write("Deleted Duplicate Files:\n")

        for File in DeletedFiles:
            Fobj.write(File + "\n")

        Fobj.write("\nTotal Deleted Files : %d\n" % len(DeletedFiles))
        Fobj.write("Report Generated At : %s\n" % time.ctime())

        Fobj.write(Border + "\n")

def CalculateCheckSum(FileName):
    fobj = open(FileName,"rb")# open in binery mode
    hobj = hashlib.md5() 

    Buffer = fobj.read(1024)
    while(len(Buffer)> 0):
        hobj.update(Buffer)
        Buffer = fobj.read(1024)
        
    fobj.close()
    return hobj.hexdigest()# return Checksum

def FindDuplicate(DirectoryName = "Folder1"):
    Ret = False
    Ret = os.path.exists(DirectoryName)

    if (Ret == False):
        print("There is no such Directory.. ")
        return
    
    Duplicate = {}
    for FolderName,SubFolderName,FileName in os.walk(DirectoryName):
        for fName  in FileName:
            fName = os.path.join(FolderName,fName)
            CheckSum = CalculateCheckSum(fName)

            if CheckSum in Duplicate:
                Duplicate[CheckSum].append(fName)
            else:
                Duplicate[CheckSum] = [fName]

    return Duplicate  

def DisplayResult(MyDict):
    Result = list(filter(lambda X : len(X)> 1, MyDict.values()))
    count = 0
    for value in Result:
        for SubValue in value:
            count = count+1
            print(SubValue)
        print("Value of Count is :",count)
        count = 0  

def DeleteDuplicate(Path="Folder1"):

    MyDict = FindDuplicate(Path)

    Result = list(filter(lambda X: len(X) > 1, MyDict.values()))

    DeletedFiles = []

    count = 0

    for value in Result:

        for SubValue in value:

            count += 1

            if count > 1:
                print("Deleted File :", SubValue)
                os.remove(SubValue)

                DeletedFiles.append(SubValue)

        count = 0

    print("Total Deleted Files :", len(DeletedFiles))

    CreateLog(DeletedFiles)


def main():
    DeleteDuplicate()

if __name__ =="__main__":
    main()