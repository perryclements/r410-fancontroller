"""
Python fan controller for Dell R410 based on CPU temperature.

By perryclements/r410-fancontroller Github

Based on original script by @marcusvb/r710-fancontroller (GitLab & GitHub)

"""
from subprocess import Popen, PIPE, STDOUT
import time
import string

# Tcase, maximum temperature allowed at the processor Integrated Heat Spreader (IHS).
Tcase = 63

sleepTime = 5
celcius = 'C'
floatDot = '.'

#Do a command and return the stdout of proccess
def sendcommand(cmdIn):
    p = Popen(cmdIn, shell=True, executable="/bin/bash", stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    return p.stdout.read()

#Do a ipmi command, setup for the default command.
def ipmicmd(cmdIn):
    return sendcommand("ipmitool " + cmdIn)

#Gets the CPU temperture from lm-sensors, returns the maximum temperaturre.
def getcputemp():
    cmd = sendcommand('sensors  -u | grep "input"')
    indexes = [pos for pos, char in enumerate(cmd) if char == floatDot]
    cputemperatures = []
    for loc in indexes:
        temp = cmd[int(loc) - 2] + cmd[int(loc) - 1]
        cputemperatures.append(int(temp))

    #return the maximum cpu temperature
    return max(cputemperatures)

#Check if controller was in automode, if so we override to manual.
def checkstatus(status):
    if (status == 5):
        ipmicmd("raw 0x30 0x30 0x01 0x00")

#Main checking function which checks temperatures to the default set above.
def checktemps(status):
    maxCpuT = getcputemp()

    if (maxCpuT <= (Tcase - 7)):
        if (status != 1):
            checkstatus(status)
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x18")
            print("Setting to 3600/2400 RPM, Server is cool")
        status = 1

    elif(maxCpuT > (Tcase - 7) and maxCpuT <= (Tcase -5)):
        if (status != 2):
            checkstatus(status)
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x20")
            print("Setting to 7200/2640 RPM, Server is toasty")
        status = 2

    elif(maxCpuT > (Tcase - 5) and maxCpuT <= (Tcase -3)):
        if (status != 3):
            checkstatus(status)
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x22")
            print("Setting to 7200/2640 RPM, Server is toasty")
        status = 3

    elif(maxCpuT > (Tcase - 3) and maxCpuT <= (Tcase -1)):
        if (status != 4):
            checkstatus(status)
            ipmicmd("raw 0x30 0x30 0x02 0xff 0x24")
            print("Setting to 7200/2640 RPM, Server is toasty")
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
