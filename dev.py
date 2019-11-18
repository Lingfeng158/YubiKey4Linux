import subprocess
import sys
import os
import socket

#script for making distributable
#pyinstaller --add-data 'cmd:.' dev.py

#or 
#pyinstaller -F dev.py
#cp cmd ./dist/

#routines
def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def adding_key(pathToKeys):
    #Ensure YubiKey
    userResponse=''
    print("This module installation process requires present Yubikey")
    print("Please Insert Yubikey and Continue")
    while(userResponse=='' or (userResponse[0] not in ['y','Y','n','N'])):
        userResponse=input("Is yubikey present? [Y]es/[N]o\n")
        if userResponse[0]in ['y', 'Y']:
            print('Please touch the metal plate on YubiKey to continue')
            os.system('pamu2fcfg >  '+pathToKeys)
            print('Key saved at', pathToKeys)
        elif userResponse[0] in ['n', 'N']:
            print('Exit Installation')
            exit()
        else:
            print("Input Invalid")

def adding_backup(pathToKeys):
    userResponse=''
    print("Please Insert Yubikey and Continue")
    while(userResponse=='' or (userResponse[0] not in ['y','Y','n','N'])):
        userResponse=input("Is your backup yubikey present? [Y]es/[N]o\n")
        if userResponse[0]in ['y', 'Y']:
            print('Please touch the metal plate on YubiKey to continue')
            os.system('pamu2fcfg -n >>  '+pathToKeys)
            print('Key added at', pathToKeys)
        elif userResponse[0] in ['n', 'N']:
            print('Exit Adding Backup')
            return
        else:
            print("Input Invalid")
            
def testingUninstaller(pathToBackup, pathToYubico):
    pathToSudo=os.path.join(pathToBackup,'sudo')
    subprocess.run(['rm', '/etc/pam.d/sudo'])
    subprocess.run(['cp', pathToSudo, '/etc/pam.d'])
    subprocess.run(['rm', '-r',pathToYubico])
    
    subprocess.run(['sudo','-k'])
    subprocess.run(['sudo','chown', 'root:root', '/etc/pam.d/sudo'])
    subprocess.run(['sudo','chmod', '755', '/etc/pam.d'])
    subprocess.run(['sudo','chmod', '644', '/etc/pam.d/sudo'])
    os.system('sudo apt-get purge libpam-u2f')

def Uninstaller(pathToBackup, pathToYubico, filename):
    pathToFile=os.path.join(pathToBackup,filename)
    originFile=os.path.join('/etc/pam.d/',filename)
    
    subprocess.run(['sudo','chmod', '777', '/etc/pam.d'])
    subprocess.run(['sudo','chmod', '777', '/etc/pam.d/sudo'])
    subprocess.run(['sudo','rm', originFile])
    subprocess.run(['cp', pathToFile, '/etc/pam.d'])
    
    testingUninstaller(pathToBackup, pathToYubico)
    
    subprocess.run(['sudo','chown', 'root:root', originFile])
    subprocess.run(['sudo','chmod', '644', originFile])
    print("Uninstallation Finished")
    print("Cleaning Up Finished")

def autoVersionChecking():
    #for autochecking
    fd=open('/etc/issue','r')
    lines=fd.readlines()
    return float(lines[0][7:12])>17.05

def manualVersionInput():
    userResponse=''
    while(userResponse=='' or (userResponse[0] not in ['y','Y','n','N'])):
        userResponse=input("Is your Ubuntu System Version 17.10 or newer? [Y]es/[N]o\n")
        if userResponse[0]in ['y', 'Y']:
            return True
        elif userResponse[0]in ['n', 'N']:
            return False
        else:
            print("Input invalid")

def fileIO(pathToFile):
    with open(pathToFile,'r+') as fd:
        lineread=''
        while(not lineread[:20] =='@include common-auth'):
            lineread=fd.readline()
        pos=fd.tell()
        content=fd.read()
        fd.seek(pos)
        fd.write(lineToInsert)
        fd.write(content)
            
#checking internet connection
if not is_connected():
    print("No network present!")
    exit()

#global variable

commandFileName='cmd'
backupFolder='bkup'
isNewVersion=True
#Resolve path
pathToFile=sys.argv[0]
pathToFolder=os.path.dirname(pathToFile)
pathToFolder=os.path.join('.',pathToFolder)
#pathToKeys
home=os.path.expanduser('~')
pathToYubico=os.path.join(home,'.config/Yubico')
subprocess.run(['mkdir',pathToYubico])
pathToKeys=os.path.join(pathToYubico,'u2f_keys')
#pathToBackup
pathToBackup=os.path.join(pathToFolder,backupFolder)
if not os.path.exists(pathToBackup):
    os.mkdir(pathToBackup)
#pathToCmd
pathToCmd=os.path.join(pathToFolder,commandFileName)
#lineToInset
lineToInsert='auth       required   pam_u2f.so\n'

filePath='/etc/pam.d/gdm-password'
fileName='gdm-password'

#Step 1 gathering system information
#Checking Version of Ubuntu        
userResponse=''
print("It is important to have correct version of Ubuntu")
print("For non-Ubuntu user, please check https://support.yubico.com/support/solutions/articles/15000011356-ubuntu-linux-login-guide-u2f and select version at discretion.\n")
print("You can manually select version or let this tool auto-detect")

while(userResponse=='' or (userResponse[0] not in ['y','Y','n','N'])):
    userResponse=input("Do you want to use autocheck? [Y]es/[N]o\n")
    if userResponse[0] in ['y', 'Y']:
        isNewVersion=autoVersionChecking()
    elif userResponse[0] in ['n', 'N']:
        #manually input ubuntu version
        isNewVersion=manualVersionInput()
    else:
        print("Input Invalid")
print("Using newer version: ",isNewVersion)

if(not isNewVersion):
    filePath='/etc/pam.d/lightdm'
    fileName='lightdm'

userResponse=''
while(userResponse=='' or (userResponse[0] not in ['I','i','U','u','t','T'])):
    userResponse=input("What Do you want to do? [I]nstall/[U]ninstall/[T]esting uninstall\n")
    if userResponse[0] in ['U','u']:
        print('Uninstalling Yubikey')
        Uninstaller(pathToBackup, pathToYubico, fileName)
        exit()
    elif userResponse[0]in ['t','T']:
        print('Undoing Changes Made for Testing')
        testingUninstaller(pathToBackup, pathToYubico)
        print('Done')
        exit()
        
    elif userResponse[0]in ['i', 'I']:
        print('Installing')
    else:
        print('Invalid Input')

        

subprocess.run(['chmod', '+x', pathToCmd])
print("Executing Commands")
subprocess.run(['sudo',pathToCmd])

print("Setting Up Modules")
adding_key(pathToKeys)
userResponse=''
while(userResponse=='' or (userResponse[0] not in ['y','Y','n','N'])):
    userResponse=input("Do you want to add extra backup keys? [Y]es/[N]o\n")
    if userResponse[0]in ['y', 'Y']:
        print('Adding Backup')
        adding_backup(pathToKeys)
        userResponse=''
    elif userResponse[0]in ['n', 'N']:
        print('')

        
#backup files
print("Backing Up Important System Configuration Files")
#temporarily unlock permission for folder etc/pam.d
subprocess.run(['sudo','chmod', '777', '/etc/pam.d'])
subprocess.run(['sudo','chmod', '777', '/etc/pam.d/sudo'])

#copy all necessary file to bkup
subprocess.run(['cp','/etc/pam.d/sudo', pathToBackup])
subprocess.run(['cp','/etc/pam.d/sudo', pathToBackup])
        

#Testing
print('Testing configuration with sudo')

###Running testing code and ask for input
fileIO('/etc/pam.d/sudo')

print('If testing failed, please run [T]esting Uninstaller to revert back to normal working system.')
print('Authenticate on YubiKey after typing in admin password')
subprocess.run(['sudo','-k'])
subprocess.run(['sudo','echo','test'])
      
###Finalizing Changes
userResponse=''
while(userResponse=='' or (userResponse[0] not in ['y','Y','n','N'])):
    userResponse=input("Does YubiKey work successfully? [Y]es/[N]o\n")
    if userResponse[0]in ['y', 'Y']:
        print('Finalizing Yubikey Installation')
        subprocess.run(['sudo','chmod', '777', filePath])
        subprocess.run(['cp',filePath, pathToBackup])
        fileIO(filePath)
        #changing permission
        subprocess.run(['sudo','chmod', '755', '/etc/pam.d'])
        subprocess.run(['sudo','chmod', '644', '/etc/pam.d/sudo'])
        subprocess.run(['sudo','chmod', '644', filePath])
        
    elif userResponse[0]in ['n', 'N']:
        testingUninstaller(pathToBackup, pathToYubico)
        print("Installation Failed")
        print("Cleaning Up Finished")
    else:
        print("Input Invalid")


    
