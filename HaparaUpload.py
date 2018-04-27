# Resources used:
# https://support.hapara.com/hc/en-us/articles/201625846-Automating-Data-Loads-with-cURL
# https://stackoverflow.com/questions/25491090/how-to-use-python-to-execute-a-curl-command

import requests, os, logging, csv, configparser
from datetime import datetime

# Setup config file
config = configparser.ConfigParser()
config.read('config.ini')

# Read info from Config, assign to variables
domainname = config['HAPARA']['DOMAIN']
passkey = config['HAPARA']['PASSKEY']

FilemakerCSV = config['LOCAL_CONFIG']['CSV_SOURCE'] # Export CSV in this order: SchoolEmail, Group, Platoon
outputfolder = config['LOCAL_CONFIG']['TMP_FOLDER']

currentClass = config['GRIZZLY']['CURRENT_CLASS']
currentSemester = config['GRIZZLY']['CURRENT_SEMESTER']

# Setup logging
logging.basicConfig(filename='HaparaUpload.log',level=logging.DEBUG)
logging.info('Beginning Hapara Processing: %s' % str(datetime.now()))

#
def csvcreator(csvfilename, headers):
    csvfile = os.path.join(os.path.sep, outputfolder, csvfilename)
    stucsv_out = open(csvfile, 'w', newline='')  # changed from 'wb' to 'w', newline='' for Python3 compatibility
    stucsv_out.write(headers)
    stucsv_out.close()


def csvreader(filepath):
    r = open(filepath, newline='')
    readcsv = csv.reader(r)
    # next(readcsv) # Skip headers
    return readcsv


def csvwriter(csvfilename, row):
    csvfile = os.path.join(os.path.sep, outputfolder, csvfilename)

    with open(csvfile, 'a', newline='') as f:  # Changed 'w' to 'a', otherwise was overwriting everything
        writer = csv.writer(f)
        writer.writerow(row)
        logging.info('Wrote row: ' + str(row))
        f.close()

def pltEndGen(plt):
    if plt is "1":
        ending = "st"
    elif plt is "2":
        ending = "nd"
    elif plt is "3":
        ending = "rd"
    elif plt is "4":
        ending = "th"
    else:
        ending = "ERROR"
    return ending


def haparaRowGen(group, contractclasslist, SchoolEmail, Group, Platoon, currentClass):
    row = []

    row.append(SchoolEmail)
    row.append(Platoon + pltEndGen(Platoon) + "-platoon-" + currentClass)

    print("Generating info for " + SchoolEmail + " who is in " + Group + " Group.")
    for item in group:
        row.append(Group[:1].lower() + "-" + item + "-" + currentClass)

    for item in contractclasslist:
        row.append(item + "-" + currentClass)

    print(row)

    return row


def createStudentHaparaList():
    filename = "HaparaStudents.csv"  # Setup in a temp directory sometime, handle deletion
    header = "email,class,class,class,class,class,class,class,class,class,class,class"  # \r\n
    print("Creating file in output folder...")
    print(filename)


    csvcreator(filename, header)

    # Setup Group lists. Probably should break this out into config.ini at some point in time instead of hard coded
    if currentSemester is "1":
        agroup = ["algebra","study-hall","us-history","career-planning","health-science","english"]
        bgroup = ["english","study-hall", "health-science", "career-planning", "algebra", "us-history"]
        cgroup = ["geometry","career-planning","us-history","health-science","english","study-hall"]
        dgroup = ["english","geometry","health-science","career-planning","us-history","study-hall"]
        egroup = ["health-science","career-planning","study-hall","algebra","us-history","english"]
        fgroup = ["health-science","career-planning","study-hall","geometry","government","english"]
        ggroup = ["health-science","english","algebra","us-history","career-planning","study-hall"]
        hgroup = ["career-planning","geometry","health-science","study-hall","english","us-history"]
        igroup = ["health-science","english","geometry","government","career-planning","study-hall"]
    elif currentSemester is "2":
        agroup = ["algebra","study-hall","us-history","career-planning","fine-arts","english"]
        bgroup = ["english","study-hall","fine-arts","career-planning","algebra","us-history"]
        cgroup = ["geometry","career-planning","us-history","fine-arts","english","study-hall"]
        dgroup = ["english","geometry","fine-arts","career-planning","us-history","study-hall"]
        egroup = ["fine-arts","career-planning","study-hall","algebra","us-history","english"]
        fgroup = ["fine-arts","career-planning","study-hall","geometry","economics","english"]
        ggroup = ["fine-arts","english","algebra","us-history","career-planning","study-hall"]
        hgroup = ["career-planning","geometry","fine-arts","study-hall","english","us-history"]
        igroup = ["fine-arts","english","geometry","economics","career-planning","study-hall"]
    else:
        print('Something went wrong, the current semester is not coded properly')
        logging.error('Current semester is not coded properly. Semester is: %s' % currentSemester)

    print("Generating file...")
    for SchoolEmail, Group, Platoon, Class1SemesterContract01, Class1SemesterContract02, Class1SemesterContract03,Class1SemesterContract04,Class1SemesterContract05,Class1SemesterContract06,Class1SemesterContract07,Class2SemesterContract01,Class2SemesterContract02,Class2SemesterContract03,Class2SemesterContract04,Class2SemesterContract05,Class2SemesterContract06,Class2SemesterContract07,ClassTechMentor,ClassYearbook in csvreader(FilemakerCSV):

        classlist = ""
        contractclasslist = []

        if currentSemester is "1":
            if Class1SemesterContract01 == "yes":
                contractclasslist.append("contract-class-1")
            else:
                pass
            if Class1SemesterContract02:
                contractclasslist.append("contract-class-2")
            else:
                pass
            if Class1SemesterContract03:
                contractclasslist.append("contract-class-3")
            else:
                pass
            if Class1SemesterContract04:
                contractclasslist.append("contract-class-4")
            else:
                pass
            if Class1SemesterContract05:
                contractclasslist.append("contract-class-5")
            else:
                pass
            if Class1SemesterContract06:
                contractclasslist.append("contract-class-6")
            else:
                pass
            if Class1SemesterContract07:
                contractclasslist.append("contract-class-7")
            else:
                pass

        if currentSemester is "2":
            if Class2SemesterContract01 == "yes":
                contractclasslist.append("contract-class-1")
            else:
                pass
            if Class2SemesterContract02:
                contractclasslist.append("contract-class-2")
            else:
                pass
            if Class2SemesterContract03:
                contractclasslist.append("contract-class-3")
            else:
                pass
            if Class2SemesterContract04:
                contractclasslist.append("contract-class-4")
            else:
                pass
            if Class2SemesterContract05:
                contractclasslist.append("contract-class-5")
            else:
                pass
            if Class2SemesterContract06:
                contractclasslist.append("contract-class-6")
            else:
                pass
            if Class2SemesterContract07:
                contractclasslist.append("contract-class-7")
            else:
                pass
        if ClassTechMentor:
            contractclasslist.append("tech-mentors")
        if ClassYearbook:
            contractclasslist.append("yearbook")

        if Group is "A":
            csvwriter(filename, haparaRowGen(agroup, contractclasslist, SchoolEmail, Group, Platoon, currentClass))
        elif Group is "B":
            csvwriter(filename, haparaRowGen(bgroup, contractclasslist, SchoolEmail, Group, Platoon, currentClass))
        elif Group is "C":
            csvwriter(filename, haparaRowGen(cgroup, contractclasslist, SchoolEmail, Group, Platoon, currentClass))
        elif Group is "D":
            csvwriter(filename, haparaRowGen(dgroup, contractclasslist, SchoolEmail, Group, Platoon, currentClass))
        elif Group is "E":
            csvwriter(filename, haparaRowGen(egroup, contractclasslist, SchoolEmail, Group, Platoon, currentClass))
        elif Group is "F":
            csvwriter(filename, haparaRowGen(fgroup, contractclasslist, SchoolEmail, Group, Platoon, currentClass))
        elif Group in ("G1", "G2", "G3"):
            csvwriter(filename, haparaRowGen(ggroup, contractclasslist, SchoolEmail, Group, Platoon, currentClass))
        elif Group is "H":
            csvwriter(filename, haparaRowGen(hgroup, contractclasslist, SchoolEmail, Group, Platoon, currentClass))
        elif Group is "I":
            csvwriter(filename, haparaRowGen(igroup, contractclasslist, SchoolEmail, Group, Platoon, currentClass))
        else:
            print("Whoops, something went wrong here")

def HaparaUpload(csvfile):
    url = 'https://td-admin.appspot.com/%s/csvupload' % domainname
    print(url)
    files = {'uploadFile': open(csvfile, 'r')}  # switch from 'rb' to 'r' for Python3 compatibility
    payload = {'passkey' : passkey,
               'multipleYears' : 'Y'}
    print(payload)
    # headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, files=files, data=payload)
    print(r.text)
    print(r.status_code)
    logging.info('Status Code of Upload: %s at time: %s' % (r.status_code, str(datetime.now())) )


def main():
    print('Here we go...')
    createStudentHaparaList()
    csvfile = os.path.join(outputfolder, 'HaparaStudents.csv')
    #HaparaUpload(csvfile)
    logging.info('End of Hapara Processing: %s' % (str(datetime.now())))

if __name__ == "__main__" :
    main()


