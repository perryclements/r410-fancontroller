"""
Python fan controller for Dell R410 based on CPU temperature.

Created by perryclements/r410-fancontroller Github

Based on original script by marcusvb/r710-fancontroller on Github

"""
from subprocess import Popen, PIPE, STDOUT
import time
import string

Tcase = 68    # Tcase, maximum temperature allowed at the processor Integrated Heat Spreader (IHS).

sleepTime = 10
celcius = 'C'
floatDot = '.'
user = "root"
password = "calvin"
ip = "192.168.x.xx"

#Do a command and return the stdout of proccess
def sendcommand(cmdIn):
    p = Popen(cmdIn, shell=True, executable="/bin/bash", stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    return p.stdout.read()

#Do a ipmi command, setup for the default command.
def ipmicmd(cmdIn):
    return sendcommand("ipmitool " + cmdIn)

#Gets the CPU tempertures from lm-sensors, returns the maximum.
def getcputemp():
    cmd = sendcommand('sensors  -u | grep "input"')
    indexes = [pos for pos, char in enumerate(cmd) if char == floatDot]
    cputemperatures = []
    for loc in indexes:
        temp = cmd[int(loc) - 2] + cmd[int(loc) - 1]
        cputemperatures.append(int(temp))

    #return the maximum cpu temperature
    return max(cputemperatures)

    #return the average cpu temperature
    #return sum(cputemperatures) / int(len(cputemperatures))

#Check if controller was in automode, if so we override to manual.
def checkstatus(status):
    if (status == 5):
        ipmicmd("raw 0x30 0x30 0x01 0x00")

#Main checking function which checks temperatures to the default set above.
def checktemps(status):
    maxCpuT = getcputemp()

    if (maxCpuT <= (Tcase - 9)):
        if (status != 1):
            checkstatus(status)
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x18")
            print("Setting to 4440 RPM, Server is cool")
        status = 1

    elif(maxCpuT > (Tcase - 9) and maxCpuT <= (Tcase -7)):
        if (status != 2):
            checkstatus(status)
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x26")
            print("Setting to 7200 RPM, Server is toasty")
        status = 2

    elif(maxCpuT > (Tcase - 7) and maxCpuT <= (Tcase -5)):
        if (status != 3):
            checkstatus(status)
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x34")
            print("Setting to 7920 RPM, Server is toasty")
        status = 3

    elif(maxCpuT > (Tcase - 5) and maxCpuT <= (Tcase -2)):
        if (status != 4):
            checkstatus(status)
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x36")
            print("Setting to 10320 RPM, Server is toasty")
        status = 4

    else:
        if (status != 5):
            ipmicmd("raw 0x30 0x30 0x01 0x01")
            print("Setting to auto/loud mode, Server it too hot")
        status = 5

    print("Cpu at: " + str(maxCpuT) + " celcius,  Status =" + str(status))
    return status

#Main running function.
def main():
    status = 5
    while True:
        time.sleep(sleepTime)
        status = checktemps(status)
        print("Sleeping for " + str(sleepTime))
if __name__ == '__main__':
    main()

