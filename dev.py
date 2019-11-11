import subprocess
import sys
import os
import socket

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
        if userResponse[0]==('y' or 'Y'):
            print('Please touch the metal plate on YubiKey to continue')
            os.system('pamu2fcfg >  '+pathToKeys)
            print('Key saved at', pathToKeys)
        elif userResponse[0]==('n' or 'N'):
            print('Exit Installation')
            exit()
        else:
            print('Invalid Input')

def adding_backup(pathToKeys):
    userResponse=''
    print("Please Insert Yubikey and Continue")
    while(userResponse=='' or (userResponse[0] not in ['y','Y','n','N'])):
        userResponse=input("Is your backup yubikey present? [Y]es/[N]o\n")
        if userResponse[0]==('y' or 'Y'):
            print('Please touch the metal plate on YubiKey to continue')
            os.system('pamu2fcfg -n >>  '+pathToKeys)
            print('Key added at', pathToKeys)
        elif userResponse[0]==('n' or 'N'):
            print('Exit Adding Backup')
            return


#checking internet connection
if not is_connected():
    print("No network present!")
    exit()

#global variable

commandFileName='cmd'
backupFolder='bkup'
#Resolve path
pathToFile=sys.argv[0]
pathToFolder=os.path.dirname(pathToFile)
pathToFolder=os.path.join(',',pathToFolder)
#pathToKeys
home=os.path.expanduser('~')
pathToYubico=os.path.join(home,'.config/Yubico')
subprocess.run(['mkdir',pathToYubico])
pathToKeys=os.path.join(pathToYubico,'u2f_keys')
#pathToBackup
pathToBackup=os.path.join(pathToFolder,backupFolder)
#pathToCmd
pathToCmd=os.path.join(pathToFolder,commandFileName)
#lineToInset
lineToInsert='auth       required   pam_u2f.so'

subprocess.run(['chmod', '+x', pathToCmd])
print("Executing Commands")
subprocess.run(['sudo',pathToCmd])


print("Setting Up Modules")
adding_key(pathToKeys)
userResponse=''
while(userResponse=='' or (userResponse[0] not in ['y','Y','n','N'])):
    userResponse=input("Do you want to add extra backup keys? [Y]es/[N]o\n")
    if userResponse[0]==('y' or 'Y'):
        print('Adding Backup')
        adding_backup(pathToKeys)
        userResponse=''
    elif userResponse[0]==('n' or 'N'):
        print('')

        
#backup files
print("Backing Up Important System Configuration Files")
#temporarily unlock permission for folder etc/pam.d
subprocess.run(['sudo','chmod', '777', '/etc/pam.d'])

#copy all necessary file to bkup
subprocess.run(['cp','/etc/pam.d/sudo', pathToBackup])
subprocess.run(['cp','/etc/pam.d/gdm-password', pathToBackup])
subprocess.run(['cp','/etc/pam.d/sudo', pathToBackup])

userResponse=''
while(userResponse=='' or (userResponse[0] not in ['y','Y','n','N'])):
    userResponse=input("Do you want to add extra backup keys? [Y]es/[N]o\n")
    if userResponse[0]==('y' or 'Y'):
        print('Adding Backup')
        adding_backup(pathToKeys)
        userResponse=''
    elif userResponse[0]==('n' or 'N'):
        print('')
    else:
        print('')
        
#Checking Version of Ubuntu        
userResponse=''
print("It is important to have correct version of Ubuntu")
print("For non-Ubuntu user, please check https://support.yubico.com/support/solutions/articles/15000011356-ubuntu-linux-login-guide-u2f and select version at discretion.)
print("You can manually select version or let this tool auto-detect")

while(userResponse=='' or (userResponse[0] not in ['y','Y','n','N'])):
    userResponse=input("Do you want to use autocheck? [Y]es/[N]o\n")
    if userResponse[0]==('y' or 'Y'):
        print('Autochecking Ubuntu Version')
        #checking using /etc/issue
    elif userResponse[0]==('n' or 'N'):
        #manually input ubuntu version
#Testing
print('Testing configuration with sudo')

###Running testing code and ask for input

userResponse=''
while(userResponse=='' or (userResponse[0] not in ['y','Y','n','N'])):
    userResponse=input("Does YubiKey work successfully? [Y]es/[N]o\n")
    if userResponse[0]==('y' or 'Y'):
        print('Finalizing Yubikey Installation')
        #adding change to gdm-password (for ubuntu 17.10 and newer)
        #adding change to lightdm (for ubuntu 17.04 and older)
        #changing permission
    elif userResponse[0]==('n' or 'N'):
        print('Testing Failed')
        print('Rolling Back All changes')
        #pasting back original file
        #changing permission


    