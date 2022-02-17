import base64
import re
from io import BytesIO
from PIL import Image

#import face_recognition

from datetime import date
import MySQLdb as mdb

#Library for text message
from twilio.rest import Client
from random import randint
import time


# conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
#                       'Server=DESKTOP-E2NRFQ7;'
#                       'Database=MicaloDB;'
#                       'Trusted_Connection=yes;')

# MyCursor = conn.cursor()

# server = 'micaloserver.database.windows.net'
# database = 'Micalo-DB'
# username = 'micalo'
# password = '{+hja%OM*78}'   
# driver= 'ODBC Driver 17 for SQL Server'

# conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
# MyCursor = conn.cursor()



DBHOST = "mysql-67509-0.cloudclusters.net"
DBNAME = "MicaloDB_VersionMySQL"
DBUSER = "MedDali"
DBPASS = "+hja%OM*78"
DBPORT = 19342

conn = mdb.connect(DBHOST,DBUSER,DBPASS,DBNAME,DBPORT)
MyCursor = conn.cursor()


def base64_to_image(base64_str, image_path=None):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    if image_path:
        img.save(image_path)
    
    return img

def sginUpClient(firstName,lastName,emailUser,phoneUser,passwordUser,imageUser):
    resultSignUp = 0
    # print(type(str(firstName)))
    # print(type(lastName))
    # print(type(emailUser))
    # print(type(phoneUser))
    # print(type(passwordUser))
    # print(type(imageUser))
    try:
        lenImage = len(imageUser)
        # print(type(lenImage))
        MyCursor.execute('''INSERT INTO ClientCompany(firstName,lastName,email,phoneNumber,passwordClient,imageClient,lenImageClient)
        VALUES(%s,%s,%s,%s,%s,%s,%s)''',(firstName,lastName,emailUser,phoneUser,passwordUser,imageUser,lenImage))
        conn.commit()
        print("Connect")
        resultSignUp = 1
        print("Sucess in table ClientCompany") 
    except:
        resultSignUp = 0
        print("The phone number is use it")
    return resultSignUp

#sginUpClient("Mohamed Ali","JAZIRI","meddalijaziri@gmail.com","216 53 786 397","123","")

def signInWithEmailAndPassword(emailAdress,passwordUser):
    SelectRequette=[]
    resultQuerry = MyCursor.execute('''SELECT * FROM ClientCompany WHERE email = (%s) and passwordClient = (%s) '''
    ,(emailAdress,passwordUser))
    for x in MyCursor:
        SelectRequette.append(x[0])
        SelectRequette.append(x[3])
    print(SelectRequette)
    return(SelectRequette)

#signInWithEmailAndPassword("mohamedali.jaziri@eniso.u-sousse.tn","123")

def getImagesFromDB(ImageFromAngularApplication):
    SelectRequette=[]
    SelectRequetteForName=[]
    MyCursor.execute('''SELECT imageClient FROM ClientCompany ''')
    for x in MyCursor:
        SelectRequette.append(x[0])
        
    for y in SelectRequette:
        try:
            base64_to_image(y,"./imageBack\ImageTestFromDB.jpg")

            faceFromAngular = face_recognition.load_image_file(ImageFromAngularApplication)
            ImageForEncoding = face_recognition.load_image_file("./imageBack\ImageTestFromDB.jpg")

            faceFromAngular_encoding = face_recognition.face_encodings(faceFromAngular)[0]
            ImageForEncoding_encoding = face_recognition.face_encodings(ImageForEncoding)[0]

            results = face_recognition.compare_faces([faceFromAngular_encoding], ImageForEncoding_encoding)
        except:
            print("There is some erreur please cheek your position of your picture")
        if(results[0]==True):
            resultQuerry = MyCursor.execute('''SELECT * FROM ClientCompany WHERE lenImageClient = %s''',(len(y),))
            for x in MyCursor:
                SelectRequetteForName.append(x[0])
                SelectRequetteForName.append(x[5])

    #print(SelectRequette)
    return(SelectRequetteForName)


def sginUpCompany(nameCompany,companAct,country,currency,phoneUser):
    resultSignUp = 0
    SelectRequette=""
    logoCompanyInLocal="../../../assets/img/CompanyLogo.png"
    resultQuerry = MyCursor.execute('''SELECT nameCompany FROM Company WHERE nameCompany = (%s)''',(nameCompany,))
    for x in MyCursor:
        SelectRequette = x[0]
    # print(SelectRequette)
    if(not SelectRequette):
        creationDate = date.today()
        MyCursor.execute('''INSERT INTO Company(nameCompany,country,activity,currency,creationDate,phoneNumberClientCompany,
        logoCompany) VALUES(%s,%s,%s,%s,%s,%s,%s)''',(nameCompany,country,companAct,currency,creationDate,phoneUser,logoCompanyInLocal))
        conn.commit()
        resultSignUp = 1
        print("Sucess in table Company") 

    else:
        resultSignUp = 0
        print("The name company is use it")
    return resultSignUp

# print("SignUp company ...")
# sginUpCompany("JustGroupe","eeee","tn","ddddd","+21653786397")

# Generate 4 digits random function
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def sendSMSValidation(emailAdress):
    SelectRequette=""
    resultQuerry = MyCursor.execute('''SELECT phoneNumber FROM ClientCompany WHERE email = (%s)''',(emailAdress,))
    for x in MyCursor:
        SelectRequette = x[0]
    # print(SelectRequette)

    account_sid = 'AC04f5ac0339e91593286199987f5e0210'
    auth_token = '8c8e493805971f3080e93b0dda38b308'
    phoneNumber_twillio = '+17655772935'


    client = Client(account_sid,auth_token)
    valRandom = random_with_N_digits(4)

    message = client.messages.create(
    body = valRandom,
    from_ = phoneNumber_twillio,
    to = SelectRequette
    )
    #print(valRandom)
    MyCursor.execute('''UPDATE ClientCompany SET verifNumber = (%s) WHERE phoneNumber = (%s)''',(valRandom,str(SelectRequette)))
    conn.commit()
    print("Sucess add the verification number")

    print("Check if the time is ready to update the data")
    


def sendSMSUsePhoneNb(phoneNumberToAnCodeLocal):
    # print(phoneNumberToAnCodeLocal)
    account_sid = 'AC04f5ac0339e91593286199987f5e0210'
    auth_token = '8c8e493805971f3080e93b0dda38b308'
    phoneNumber_twillio = '+17655772935'

    client = Client(account_sid,auth_token)
    valRandom = random_with_N_digits(4)

    # print(valRandom)
    message = client.messages.create(
    body = valRandom,
    from_ = phoneNumber_twillio,
    to = phoneNumberToAnCodeLocal
    )
    MyCursor.execute('''UPDATE ClientCompany SET verifNumber =
     (%s) WHERE phoneNumber = (%s)''',(str(valRandom),phoneNumberToAnCodeLocal))
    conn.commit()


def checkTheCodeFromDB(codeNotif):
    SelectRequette=""
    resultQuerry = MyCursor.execute('''SELECT verifNumber FROM ClientCompany WHERE verifNumber = (%s)''',(codeNotif,))
    for x in MyCursor:
        SelectRequette = x[0]
    # print(SelectRequette)

    return SelectRequette


def getInformationClientFromDB(emailAdress):
    SelectRequette=[]
    resultQuerry = MyCursor.execute('''SELECT * FROM ClientCompany WHERE email = (%s)''',(emailAdress,))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequette.append([x for x in row])

    #print(SelectRequette)

    return SelectRequette

def getInformationCompanyDB(phoneUserNumber):
    SelectRequette=[]
    resultQuerry = MyCursor.execute('''SELECT * FROM Company WHERE phoneNumberClientCompany = (%s)''',(phoneUserNumber,))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequette.append([x for x in row])

    # print(SelectRequette)

    return SelectRequette
# getInformationCompanyDB("+21653786397")

def EditInformationOfCompanyDB(phoneUserNumber,nameCompanySend,telePhoneSend,cellNumberSend,webSiteSend,firstNameProfileSend,
    lastNameProfileSend,emailUserCompanySend,citySend,zipCodeSend,logoCompanySend,addressCompanySend,taxRegNumSend):
    
    resultQuerry = MyCursor.execute('''UPDATE Company SET nameCompany = %s,telePhone = %s,cellNumber = %s,webSite = %s,
    firstNameCEO = %s, lastNameCEO = %s, email = %s,City = %s, logoCompany = %s, addressCompany = %s, taxRegNum = %s, ZIPCode = %s
      WHERE phoneNumberClientCompany = %s''',(nameCompanySend,telePhoneSend,cellNumberSend,webSiteSend,firstNameProfileSend,
    lastNameProfileSend,emailUserCompanySend,citySend,logoCompanySend,addressCompanySend,taxRegNumSend,zipCodeSend,phoneUserNumber))

    conn.commit()
    print("Sucess Update into table company !")


def getInformationClientDB(phoneUserNumber):
    SelectRequette=[]
    resultQuerry = MyCursor.execute('''SELECT * FROM ClientCompany WHERE phoneNumber = (%s)''',(phoneUserNumber,))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequette.append([x for x in row])

    #print(SelectRequette)

    return SelectRequette

# getInformationFromClientDB("+21622450528")

def EditInformationOfClientCompanyDB(phoneUserNumber,userProfileImageToDB,FirstNameToDB,LastNameToDB,emailProfileToDB,passwordProfileToDB):
    # print(userProfileImageToDB)
    # print(phoneUserNumber)
    # print(FirstNameToDB)
    # print(LastNameToDB)
    # print(emailProfileToDB)
    # print(passwordProfileToDB)
    resultQuerry = MyCursor.execute('''UPDATE ClientCompany SET firstName = %s,	lastName = %s,email = %s,
    passwordClient = %s, imageClient = %s WHERE phoneNumber = %s''',(FirstNameToDB,LastNameToDB,emailProfileToDB,
    passwordProfileToDB,userProfileImageToDB,phoneUserNumber))
    conn.commit()
    print("Sucess Update into table Client Company !")
    return 1

    

def AddWorkerInDataBase(phoneNumberOfUser,fullName,professionWorker,professionCoefficient,profileWorker,departName,GrossSalary):
    try:
        SelectRequette=""
        resultQuerry = MyCursor.execute('''SELECT companyId FROM Company WHERE phoneNumberClientCompany = (%s)''',(phoneNumberOfUser,))
        for x in MyCursor:
            SelectRequette = x[0]
        # print(SelectRequette)
        yearCreComp = date.today().year

        MyCursor.execute('''INSERT INTO WorkerCompany(fullName,profession,departName,profCoefficient,profileWork,companyId,yearCreationCompte) 
        VALUES(%s,%s,%s,%s,%s,%s,%s)''',(fullName,professionWorker,departName,professionCoefficient,profileWorker,SelectRequette,yearCreComp))
        conn.commit()
        print("Sucess on add into WorkerCompany table")

        resultQuerry = MyCursor.execute('''SELECT * FROM WorkerCompany ''')
        for x in MyCursor:
            SelectRequette = x[0]
        # print(SelectRequette)

        AddInTableSalary(fullName,professionWorker,GrossSalary)
        return 1
    except:
        print("There is an problem to insert into dataBase !!!")
        return 0


def updateInfoWorkerCompanyInDB(userProfileImageSend,departmentNameWorkerSend,professionWorkerSend,
    profitCofficientWorkerSend,salaryWorkerSend,fullNameWorkerSend,idWorkerSend):
    print(salaryWorkerSend)
    MyCursor.execute('''UPDATE WorkerCompany SET fullName = %s, profession = %s, departName = %s, profCoefficient = %s,
    profileWork = %s where idWorker = %s'''
    ,(fullNameWorkerSend,professionWorkerSend,departmentNameWorkerSend,profitCofficientWorkerSend,userProfileImageSend,
    idWorkerSend))
    H_jCostsOnCompany = round((((int(salaryWorkerSend)*14)/300)+((int(salaryWorkerSend)*14*27/100)/365)),3)
    H_jCostsOnSite =round(( H_jCostsOnCompany*2),3)
    HCostsOnCompany = round((H_jCostsOnCompany/8),3)
    HCostsOnSite = round((HCostsOnCompany*2),3)
    
    MyCursor.execute('''UPDATE Salary SET Salary = %s, H_jCostsOnCompany=%s , H_jCostsOnSite=%s,
	HCostsOnCompany=%s, HCostsOnSite=%s where idWorker = %s''',(int(salaryWorkerSend),H_jCostsOnCompany,H_jCostsOnSite,
    HCostsOnCompany,HCostsOnSite,idWorkerSend,))
    print("Sucess update into the table salary and workercompany")
    conn.commit()



def GetAllWorkerCompanyFromDB(phoneNumberOfUser):
    SelectRequette=""
    resultQuerry = MyCursor.execute('''SELECT companyId FROM Company WHERE phoneNumberClientCompany = (%s)''',(phoneNumberOfUser,))
    for x in MyCursor:
        SelectRequette = x[0]
    print(SelectRequette)


    # SelectRequetteStep1=[]
    # resultQuerry = MyCursor.execute('''SELECT WC.fullName, SA.salary FROM WorkerCompany WC, Salary SA where companyId = %s and WC.idWorker = SA.idWorker''',(SelectRequette,))
    # rows = MyCursor.fetchall()
    # for row in rows:
    #     SelectRequetteStep1.append([x for x in row])

    # print(SelectRequetteStep1)


    SelectRequetteStep1=[]
    resultQuerry = MyCursor.execute('''SELECT WC.* ,SA.salary from WorkerCompany WC, Salary SA where companyId = %s and WC.idWorker = SA.idWorker''',(SelectRequette,))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequetteStep1.append([x for x in row])
    #print(SelectRequetteStep1)
    return SelectRequetteStep1


def deleteWorkerFromDataBase(idWorker,fullNameWorker):
    try:
        print(idWorker)
        resultQuerry = MyCursor.execute('''DELETE FROM Salary WHERE idWorker = %s''',(idWorker,))
        conn.commit()
        print("Sucess delete this worker from Salary table")

        resultQuerry = MyCursor.execute('''DELETE FROM workCGOffre WHERE idWorker = %s''',(idWorker,))
        conn.commit()
        print("Sucess delete this worker from workCGOffre table")


        resultQuerry = MyCursor.execute('''DELETE FROM workCGOffreForStep2 WHERE idWorker = %s''',(idWorker,))
        conn.commit()
        print("Sucess delete this worker from workCGOffreForStep2 table")


        resultQuerry = MyCursor.execute('''DELETE FROM workCGOffreForStep3 WHERE idWorker = %s''',(idWorker,))
        conn.commit()
        print("Sucess delete this worker from workCGOffreForStep3 table")

        resultQuerry = MyCursor.execute('''DELETE FROM WorkerCompany WHERE fullName = %s and idWorker = %s''',(fullNameWorker,idWorker))
        conn.commit()
        print("Sucess delete this worker from WorkerCompany table")
            
        return 1
    except:
        print("There is a problem on delete")
        return 0

def getAllWorkerNameFromDB(phoneNumberOfUser):
    SelectRequette=""
    resultQuerry = MyCursor.execute('''SELECT companyId FROM Company WHERE phoneNumberClientCompany = (%s)''',(phoneNumberOfUser,))
    for x in MyCursor:
        SelectRequette = x[0]
    # print(SelectRequette)

    SelectRequette2=[]
    resultQuerry = MyCursor.execute('''SELECT fullName FROM WorkerCompany where companyId = (%s)''',(SelectRequette,))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequette2.append([x for x in row])
    # print(SelectRequette)

    return SelectRequette2


def AddInTableSalary(fullName,professionWorker,GrossSalary):
    print("********************* AddInTableSalary *********************")
    SelectRequette=""

    resultQuerry = MyCursor.execute('''SELECT idWorker FROM WorkerCompany WHERE fullName = (%s) and profession = (%s) ''',(fullName,professionWorker,))
    for x in MyCursor:
        SelectRequette = x[0]
    # print(SelectRequette)

    H_jCostsOnCompany = round((((GrossSalary*14)/300)+((GrossSalary*14*27/100)/365)),3)
    H_jCostsOnSite =round(( H_jCostsOnCompany*2),3)
    HCostsOnCompany = round((H_jCostsOnCompany/8),3)
    HCostsOnSite = round((HCostsOnCompany*2),3)
    MyCursor.execute('''INSERT INTO Salary(idWorker,salary,H_jCostsOnCompany,H_jCostsOnSite,HCostsOnCompany,HCostsOnSite) 
    VALUES(%s,%s,%s,%s,%s,%s)''',(SelectRequette,GrossSalary,H_jCostsOnCompany,H_jCostsOnSite,HCostsOnCompany,HCostsOnSite))
    conn.commit()
    print("Sucess on add into salary table")
    return 1

def insertIntoGlobalOffre(idOffre,phoneNumberOfUser):
    try:
        SelectRequette0=""
        resultQuerry = MyCursor.execute('''SELECT * FROM GlobalOffre WHERE idOffre = (%s)''',(idOffre,))
        for x in MyCursor:
            SelectRequette0 = x
        # print(SelectRequette)
        if(not SelectRequette0):
            SelectRequette=""
            resultQuerry = MyCursor.execute('''SELECT companyId FROM Company WHERE phoneNumberClientCompany = (%s)''',(phoneNumberOfUser,))
            for x in MyCursor:
                SelectRequette = x[0]
            # print(SelectRequette)

            MyCursor.execute('''INSERT INTO GlobalOffre(idOffre,companyId,globalDaysOfWork,globalProposition,globalRevient
            ,globalRevientAndFG,globalMargeBrute,globalMargeNete,globalFinaleMarge) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            ,(idOffre,SelectRequette,0,0,0,0,0,0,0,))
            conn.commit()
            print("Sucess add into GlobalOffre table")
            return 1
        else:
            print("You can't add this offre into GlobalOffre because you have it")
    except:
        print("There is a problem please check your data on table GlobalOffre")
        return 0

def insertIntoOffresStep1(idOffre):
    try:
        SelectRequette=""
        resultQuerry = MyCursor.execute('''SELECT * FROM OffresStep1 WHERE idOffre = (%s)''',(idOffre,))
        for x in MyCursor:
            SelectRequette = x
        # print(SelectRequette)
        if(not SelectRequette):
            MyCursor.execute('''INSERT INTO OffresStep1(idOffre) VALUES(%s)''',(idOffre,))
            conn.commit()
            print("Sucess add into OffresStep1 table")
            return 1
        else:
            print("You can't add this offre into OffresStep1 because you have it")
    except:
        print("There is a problem please check your data on table OffresStep1")
        return 0

def insertIntoworkCGOffre(idOffre,fullName,nbHWOC,nbHWOS,valueSend):
    try:
        SelectRequette=""
        resultQuerry = MyCursor.execute('''SELECT idWorker,profCoefficient FROM WorkerCompany WHERE fullName = (%s)''',(fullName,))
        for x in MyCursor:
            SelectRequette = x
        #print(SelectRequette)

        SelectRequette2=""
        resultQuerry2 = MyCursor.execute('''SELECT HCostsOnCompany,HCostsOnSite FROM Salary WHERE idWorker = (%s) ''',(SelectRequette[0],))
        for x in MyCursor:
            SelectRequette2 = x
        # print(SelectRequette2[0])
        # print(SelectRequette2[1])


        priceRevByWorker = round(((SelectRequette2[1]*nbHWOS) + (SelectRequette2[0]*nbHWOC)),3)
        pricePropByWorker = round((((SelectRequette2[1]*SelectRequette[1])*nbHWOS) + ((SelectRequette2[0]*SelectRequette[1])*nbHWOC)),3)
        coutByWorker = round((priceRevByWorker + (priceRevByWorker * (valueSend / 100))),3)
        margeBrutte = round((pricePropByWorker - priceRevByWorker),3)
        margeNet = round((pricePropByWorker - coutByWorker))
        if margeNet ==0.0:
            margeNetPC = 0.0
        else:
            margeNetPC = round((margeNet / pricePropByWorker) * 100)
        # print("Price Revient: ",priceRevByWorker)
        # print("Price Proposition: ",pricePropByWorker)
        # print("Cout: ",coutByWorker)
        # print("Marge Brute: ",margeBrutte)
        # print("Marge Net: ",margeNet)
        # print("Marge Net: ",margeNetPC,"%")


        MyCursor.execute('''INSERT INTO workCGOffre(idWorker,idOffre,hoursWorkCompany,hoursWorkOutCompany,FG,CostsByWorker,tPropositionByWorker,tRevientByWorker,
        tMargeNet,tMargeBrute,tMargeNetPC) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(SelectRequette[0],idOffre,nbHWOC,nbHWOS,valueSend,coutByWorker,pricePropByWorker,priceRevByWorker
        ,margeBrutte,margeNet,margeNetPC))
        conn.commit()
        print("Sucess add into workCGOffre table")
        return 1
    except:
        print("There is a problem in the table of workCGOffre")
        return 0

def getInformationFromWorkCGOffre(idOffreSend,phoneNumberOfUser):
    # try:
        
    # except:
    #     print("There is a probleme please try again !!")
    #     return 1

    SelectRequette1=""
    resultQuerry = MyCursor.execute('''SELECT companyId FROM Company WHERE phoneNumberClientCompany = (%s)''',(phoneNumberOfUser,))
    for x in MyCursor:
        SelectRequette1 = x[0]
    # print(SelectRequette1)


    SelectRequette2=[]
    resultQuerry2 = MyCursor.execute('''SELECT WC.fullName,WC.profileWork,WCG.hoursWorkCompany,WCG.hoursWorkOutCompany
    ,WCG.tPropositionByWorker,WCG.tRevientByWorker,WCG.CostsByWorker,WCG.FG, WC.companyId,WC.idWorker FROM workCGOffre WCG, WorkerCompany WC, 
    GlobalOffre GO WHERE (WCG.idWorker = WC.idWorker) and (WCG.idOffre = GO.idOffre) and (WCG.idOffre = (%s) and GO.companyId= (%s)) 
    ''',(idOffreSend,SelectRequette1,))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequette2.append([x for x in row])

    #print(SelectRequette2)
    return SelectRequette2

# getInformationFromWorkCGOffre("JustGroup-01","+21622450528")

def updateInformationOfStep1ToDB(FGSend,nbWorkOnCompanySend,nbWorkOnSiteSend,idWorkerNameSend,idOffreSendGlobaleSend):
    SelectRequette=""
    resultQuerry = MyCursor.execute('''SELECT profCoefficient FROM WorkerCompany WHERE idWorker = (%s)''',(idWorkerNameSend,))
    for x in MyCursor:
        SelectRequette = x
    #print(SelectRequette)

    SelectRequette2=""
    resultQuerry2 = MyCursor.execute('''SELECT HCostsOnCompany,HCostsOnSite FROM Salary WHERE idWorker = (%s) ''',(idWorkerNameSend,))
    for x in MyCursor:
        SelectRequette2 = x
    # print(SelectRequette2[0])
    # print(SelectRequette2[1])

    priceRevByWorker = round(((SelectRequette2[1]*nbWorkOnSiteSend) + (SelectRequette2[0]*nbWorkOnCompanySend)),3)
    pricePropByWorker = round((((SelectRequette2[1]*SelectRequette[0])*nbWorkOnSiteSend) + ((SelectRequette2[0]*SelectRequette[0])*nbWorkOnCompanySend)),3)
    coutByWorker = round((priceRevByWorker + (priceRevByWorker * (FGSend / 100))),3)
    margeBrutte = round((pricePropByWorker - priceRevByWorker),3)
    margeNet = round((pricePropByWorker - coutByWorker))
    if margeNet ==0.0:
        margeNetPC = 0.0
    else:
        margeNetPC = round((margeNet / pricePropByWorker) * 100)


    # print(nbWorkOnCompanySend,nbWorkOnSiteSend,FGSend,idWorkerNameSend,type(idOffreSendGlobaleSend))
    MyCursor.execute('''UPDATE workCGOffre SET hoursWorkCompany = (%s), hoursWorkOutCompany = (%s), FG = (%s) , CostsByWorker = (%s),
	tPropositionByWorker = (%s), tRevientByWorker = (%s), tMargeBrute = (%s), tMargeNet =(%s), tMargeNetPC=(%s)
    WHERE workCGOffre.idWorker = (%s) and workCGOffre.idOffre = (%s) '''
    ,(nbWorkOnCompanySend,nbWorkOnSiteSend,FGSend,coutByWorker,pricePropByWorker,priceRevByWorker,margeBrutte,margeNet,margeNetPC,
    idWorkerNameSend,idOffreSendGlobaleSend,))
    print("Sucesss")
    conn.commit()

    # MyCursor.execute('''INSERT INTO workCGOffre(idWorker,idOffre,hoursWorkCompany,hoursWorkOutCompany,FG,CostsByWorker,tPropositionByWorker,tRevientByWorker,
    # tMargeNet,tMargeBrute,tMargeNetPC) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(SelectRequette[0],idOffre,nbHWOC,nbHWOS,valueSend,coutByWorker,pricePropByWorker,priceRevByWorker
    # ,margeBrutte,margeNet,margeNetPC))
    # conn.commit()
    # print("Sucess add into workCGOffre table")

    return 1

# updateInformationOfStep1ToDB(10,10,85,3,"JustGroup-01")

def calculPhase1OffreFromDB(idOffre):
    try:
        print("**************** calculPhase1OffreFromDB ****************")
        SelectRequette1=""
        resultQuerry = MyCursor.execute('''SELECT count(idOffre) FROM workCGOffre WHERE idOffre = (%s)''',(idOffre,))
        for x in MyCursor:
            SelectRequette1 = x[0]
        # print(SelectRequette1)
        if SelectRequette1 == 0:
            # If you will using the update method you will using this lines
            MyCursor.execute('''UPDATE OffresStep1 SET CostsGlobale = %s, totaleProposition = %s, totaleRevient = %s ,
            totaleQtyWork = %s, totaleMargeBrute=%s,totaleMargeNet =%s, totaleMargeNetPC = %s WHERE idOffre = %s'''
            ,(0,0,0,0,0,0,0,idOffre))
            print("Sucesss")
            return 1
                
        else:
            SelectRequette=[]
            resultQuerry = MyCursor.execute('''SELECT SUM(hoursWorkCompany),SUM(hoursWorkOutCompany),SUM(tPropositionByWorker),
            SUM(tRevientByWorker),SUM(CostsByWorker),SUM(tMargeBrute),SUM(tMargeNet) FROM workCGOffre where idOffre = (%s) GROUP BY idOffre''',(idOffre,))
            for x in MyCursor:
                SelectRequette.append(int(x[0]))
                SelectRequette.append(int(x[1]))
                SelectRequette.append(x[2])
                SelectRequette.append(x[3])
                SelectRequette.append(x[4])
                SelectRequette.append(x[5])
                SelectRequette.append(x[6])
                
            totaleDatOfWork = SelectRequette[0]+SelectRequette[1]
            totaleQtyWork = round((totaleDatOfWork / 8.66),2)
            totaleProposition = round(SelectRequette[2],3)
            totaleRevient = round(SelectRequette[3],3)
            CostsGlobale = round(SelectRequette[4],3)
            totaleMargeNet = round(SelectRequette[5],3)
            totaleMargeBrute = round(SelectRequette[6],3)
            totaleMargeNetPC = round(((totaleMargeNet / totaleProposition)*100),3)

            print(totaleProposition)
            print(totaleMargeBrute)
            print(totaleMargeNetPC)

            # If you will using the update method you will using this lines
            MyCursor.execute('''UPDATE OffresStep1 SET totaleQtyWork = (%s),totaleProposition = (%s), totaleRevient = (%s), CostsGlobale=(%s), totaleMargeBrute=(%s),
            totaleMargeNet =(%s), totaleMargeNetPC = (%s) WHERE idOffre = (%s)''',(totaleQtyWork,totaleProposition,totaleRevient,CostsGlobale,totaleMargeBrute,
            totaleMargeNet,totaleMargeNetPC,idOffre))

            # MyCursor.execute('''INSERT INTO OffresStep1(idOffre,totaleQtyWork,totaleProposition,totaleRevient,CostsGlobale,totaleMargeBrute,
            # totaleMargeNet,totaleMargeNetPC) VALUES(?,?,?,?,?,?,?,?)''',
            # (idOffre,totaleQtyWork,totaleProposition,totaleRevient,CostsGlobale,totaleMargeBrute,totaleMargeNet,totaleMargeNetPC))
            conn.commit()
            print("Sucess add into workCGOffre table")
            return 1
        
    except:
        print("There is a problem please check up")
        return 0



def getInformationFromOffresStep1(idOffre,phoneNumberOfUser):
    # print(phoneNumberOfUser)
    SelectRequette1=""
    resultQuerry = MyCursor.execute('''SELECT companyId FROM Company WHERE phoneNumberClientCompany = (%s)''',(phoneNumberOfUser,))
    for x in MyCursor:
        SelectRequette1 = x[0]
    # print(SelectRequette1)

    SelectRequette2=[]
    resultQuerry = MyCursor.execute('''SELECT * from OffresStep1 OS1, GlobalOffre GO where (OS1.idOffre = GO.idOffre) and 
    OS1.idOffre = (%s) and GO.companyId = (%s)''',(idOffre,SelectRequette1,))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequette2.append([x for x in row])
    print(SelectRequette2)

    return SelectRequette2
    

def getInformationFromOffresStep2(idOffre,phoneNumberOfUser):
    # print(phoneNumberOfUser)
    SelectRequette1=""
    resultQuerry = MyCursor.execute('''SELECT companyId FROM Company WHERE phoneNumberClientCompany = (%s)''',(phoneNumberOfUser,))
    for x in MyCursor:
        SelectRequette1 = x[0]
    # print(SelectRequette1)

    SelectRequette2=[]
    resultQuerry = MyCursor.execute('''SELECT * from OffresStep2 OS1, GlobalOffre GO where (OS1.idOffre = GO.idOffre) and 
    OS1.idOffre = (%s) and GO.companyId = (%s)''',(idOffre,SelectRequette1,))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequette2.append([x for x in row])
    #print(SelectRequette2)

    return SelectRequette2
    
def deleteAnWorkerFromOffreUsingDB(workerProfileSend,imageProfileSend,idOffreSendGlobaleSend):
    
    SelectRequette=""
    resultQuerry = MyCursor.execute('''SELECT idWorker from WorkerCompany where fullName = (%s)''',(workerProfileSend,))
    for x in MyCursor:
            SelectRequette = x[0]
    # print(SelectRequette)

    resultQuerry = MyCursor.execute('''DELETE FROM workCGOffre WHERE idWorker = %s and idOffre = %s''',(SelectRequette,idOffreSendGlobaleSend))
    conn.commit()
    print("Sucess delete this worker from WorkerCompany table")
    return 1

def deleteAnWorkerFromOffreStep2UsingDB(workerProfileSend,imageProfileSend,idOffreSendGlobaleSend):
    
    SelectRequette=""
    resultQuerry = MyCursor.execute('''SELECT idWorker from WorkerCompany where fullName = (%s)''',(workerProfileSend,))
    for x in MyCursor:
            SelectRequette = x[0]
    # print(SelectRequette)

    resultQuerry = MyCursor.execute('''DELETE FROM workCGOffreForStep2 WHERE idWorker = %s and idOffre = %s''',(SelectRequette,idOffreSendGlobaleSend))
    conn.commit()
    print("Sucess delete this worker from WorkerCompany table")
    return 1


def checkIntoGlobalOffre(idOffre,phoneNumberOfUser):
    try:
        SelectRequette=""
        resultQuerry = MyCursor.execute('''SELECT companyId FROM Company WHERE phoneNumberClientCompany = (%s)''',(phoneNumberOfUser,))
        for x in MyCursor:
            SelectRequette = x[0]
        #print(SelectRequette)

        SelectRequette2=""
        resultQuerry2 = MyCursor.execute('''SELECT idOffre FROM GlobalOffre WHERE idOffre = (%s) and companyId = (%s)''',(idOffre,SelectRequette,))
        for x in MyCursor:
            SelectRequette2 = x[0]
        #print(SelectRequette2)
        if (not SelectRequette or not SelectRequette2):
            return 0
        else:
            return 1
        print("Sucess check it")
    except:
        print("There is a problem please check your data on table GlobalOffre")
        return 0

def insertIntoOffresStep2(idOffre):
    try:
        MyCursor.execute('''INSERT INTO OffresStep2(idOffre) VALUES(%s)''',(idOffre,))
        conn.commit()
        print("Sucess add into OffresStep2 table")
        return 1
    except:
        print("There is a problem please check your data on table OffresStep2")
        return 0

def insertIntoworkCGOffreStep2(idOffre,fullName,nbHWOC,nbHWOS,valueSend):
    try:
        SelectRequette=""
        resultQuerry = MyCursor.execute('''SELECT idWorker,profCoefficient FROM WorkerCompany WHERE fullName = (%s)''',(fullName,))
        for x in MyCursor:
            SelectRequette = x
        #print(SelectRequette)

        SelectRequette2=""
        resultQuerry2 = MyCursor.execute('''SELECT H_jCostsOnCompany,H_jCostsOnSite FROM Salary WHERE idWorker = (%s) ''',(SelectRequette[0],))
        for x in MyCursor:
            SelectRequette2 = x
        # print(SelectRequette2[0])
        # print(SelectRequette2[1])


        priceRevByWorker = round(((SelectRequette2[1]*nbHWOS) + (SelectRequette2[0]*nbHWOC)),3)
        pricePropByWorker = round((((SelectRequette2[1]*SelectRequette[1])*nbHWOS) + ((SelectRequette2[0]*SelectRequette[1])*nbHWOC)),3)
        coutByWorker = round((priceRevByWorker + (priceRevByWorker * (valueSend / 100))),3)
        margeBrutte = round((pricePropByWorker - priceRevByWorker),3)
        margeNet = round((pricePropByWorker - coutByWorker))
        if margeNet ==0.0:
            margeNetPC = 0.0
        else:
            margeNetPC = round((margeNet / pricePropByWorker) * 100)
        # print("Price Revient: ",priceRevByWorker)
        # print("Price Proposition: ",pricePropByWorker)
        # print("Cout: ",coutByWorker)
        # print("Marge Brute: ",margeBrutte)
        # print("Marge Net: ",margeNet)
        # print("Marge Net: ",margeNetPC,"%")

        MyCursor.execute('''INSERT INTO workCGOffreForStep2(idWorker,idOffre,h_JWorkCompany,h_JWorkOutCompany,FG,CostsByWorker,tPropositionByWorker,tRevientByWorker,
        tMargeNet,tMargeBrute,tMargeNetPC) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(SelectRequette[0],idOffre,nbHWOC,nbHWOS,valueSend,coutByWorker,pricePropByWorker,priceRevByWorker
        ,margeBrutte,margeNet,margeNetPC))
        conn.commit()
        conn.commit()
        print("Sucess add into workCGOffre table")
        return 1  
    except:
        print("There is a problem in the table of workCGOffre")
        return 0

def getInformationFromWorkCGOffreStep2(idOffreSend,phoneNumberOfUser):
    SelectRequette1=""
    resultQuerry = MyCursor.execute('''SELECT companyId FROM Company WHERE phoneNumberClientCompany = (%s)''',(phoneNumberOfUser,))
    for x in MyCursor:
        SelectRequette1 = x[0]
    # print(SelectRequette1)


    SelectRequette2=[]
    resultQuerry2 = MyCursor.execute('''SELECT WC.fullName,WC.profileWork,WCG.h_JWorkCompany,WCG.h_JWorkOutCompany
    ,WCG.tPropositionByWorker,WCG.tRevientByWorker,WCG.CostsByWorker,WCG.FG,WCG.idWorker, WC.companyId FROM workCGOffreForStep2 WCG, WorkerCompany WC, 
    GlobalOffre GO WHERE (WCG.idWorker = WC.idWorker) and (WCG.idOffre = GO.idOffre) and (WCG.idOffre = (%s) and GO.companyId= (%s)) 
    ''',(idOffreSend,SelectRequette1,))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequette2.append([x for x in row])

    #print(SelectRequette2)
    return SelectRequette2


def calculPhase2OffreFromDB(idOffre):
    # try:
    SelectRequette1=""
    resultQuerry = MyCursor.execute('''SELECT count(idOffre) FROM workCGOffreForStep2 WHERE idOffre = (%s)''',(idOffre,))
    for x in MyCursor:
        SelectRequette1 = x[0]
    # print(SelectRequette1)

    if SelectRequette1 == 0:
        # If you will using the update method you will using this lines
        MyCursor.execute('''UPDATE OffresStep2 SET CostsGlobale = %s, totaleProposition = %s, totaleRevient = %s , totaleQtyWork = %s, totaleMargeBrute=%s,
        totaleMargeNet =%s, totaleMargeNetPC = %s WHERE idOffre = %s''',(0,0,0,0,0,0,0,idOffre))
        print("Sucesss")
        return 1
            
    else:

        SelectRequette=[]
        resultQuerry = MyCursor.execute('''SELECT SUM(h_JWorkCompany),SUM(h_JWorkOutCompany),SUM(tPropositionByWorker),
        SUM(tRevientByWorker),SUM(CostsByWorker),SUM(tMargeBrute),SUM(tMargeNet) FROM workCGOffreForStep2 where idOffre = (%s) 
        GROUP BY idOffre''',(idOffre,))
        for x in MyCursor:
            SelectRequette.append(int(x[0]))
            SelectRequette.append(int(x[1]))
            SelectRequette.append(x[2])
            SelectRequette.append(x[3])
            SelectRequette.append(x[4])
            SelectRequette.append(x[5])
            SelectRequette.append(x[6])
                
        print(SelectRequette)
        totaleDatOfWork = SelectRequette[0]+SelectRequette[1]

        totaleQtyWork = round(totaleDatOfWork,2)
        totaleProposition = round(SelectRequette[2],3)
        totaleRevient = round(SelectRequette[3],3)
        CostsGlobale = round(SelectRequette[4],3)
        totaleMargeNet = round(SelectRequette[5],3)
        totaleMargeBrute = round(SelectRequette[6],3)
        totaleMargeNetPC = round(((totaleMargeNet / totaleProposition)*100),3)

        # print(totaleQtyWork)

        # If you will using the update method you will using this lines
        MyCursor.execute('''UPDATE OffresStep2 SET totaleQtyWork = (%s),totaleProposition = (%s), totaleRevient = (%s), CostsGlobale=(%s), totaleMargeBrute=(%s),
        totaleMargeNet =(%s), totaleMargeNetPC = (%s) WHERE idOffre = (%s)''',(totaleQtyWork,totaleProposition,totaleRevient,CostsGlobale,totaleMargeBrute,
        totaleMargeNet,totaleMargeNetPC,idOffre))

        # MyCursor.execute('''INSERT INTO OffresStep1(idOffre,totaleQtyWork,totaleProposition,totaleRevient,CostsGlobale,totaleMargeBrute,
        # totaleMargeNet,totaleMargeNetPC) VALUES(?,?,?,?,?,?,?,?)''',
        # (idOffre,totaleQtyWork,totaleProposition,totaleRevient,CostsGlobale,totaleMargeBrute,totaleMargeNet,totaleMargeNetPC))
        conn.commit()
        print("Sucess add into workCGOffre table")
        return 1
    # except:
    #     print("There is a problem please check up2")
    #     return 0

def updateInformationOfStep2ToDB(nbWorkOnCompanySend,nbWorkOnSiteSend,FGSend,workerNameGlobaleSend,idOffreSendGlobaleSend
    ,idWorkerGlobaleSend):
    print(nbWorkOnCompanySend,nbWorkOnCompanySend,nbWorkOnSiteSend,FGSend,workerNameGlobaleSend,idOffreSendGlobaleSend
    ,idWorkerGlobaleSend)
    SelectRequette=""
    resultQuerry = MyCursor.execute('''SELECT profCoefficient FROM WorkerCompany WHERE idWorker = (%s)''',(idWorkerGlobaleSend,))
    for x in MyCursor:
        SelectRequette = x
    print(SelectRequette)

    SelectRequette2=""
    resultQuerry2 = MyCursor.execute('''SELECT H_jCostsOnCompany,H_jCostsOnSite FROM Salary WHERE idWorker = (%s) ''',(idWorkerGlobaleSend,))
    for x in MyCursor:
        SelectRequette2=x
    
    print(SelectRequette2)

    priceRevByWorker = round(((int(SelectRequette2[1])*nbWorkOnSiteSend) + (int(SelectRequette2[0])*nbWorkOnCompanySend)),3)
    pricePropByWorker = round((((int(SelectRequette2[1])*int(SelectRequette[0]))*nbWorkOnSiteSend) + ((int(SelectRequette2[0])*int(SelectRequette[0]))*nbWorkOnCompanySend)),3)
    coutByWorker = round((priceRevByWorker + (priceRevByWorker * (FGSend / 100))),3)
    margeBrutte = round((pricePropByWorker - priceRevByWorker),3)
    margeNet = round((pricePropByWorker - coutByWorker))
    if margeNet ==0.0:
        margeNetPC = 0.0
    else:
        margeNetPC = round((margeNet / pricePropByWorker) * 100)
    # print("Price Revient: ",priceRevByWorker)
    # print("Price Proposition: ",pricePropByWorker)
    # print("Cout: ",coutByWorker)
    # print("Marge Brute: ",margeBrutte)
    # print("Marge Net: ",margeNet)
    # print("Marge Net: ",margeNetPC,"%")

    MyCursor.execute('''UPDATE workCGOffreForStep2 SET h_JWorkCompany = (%s), h_JWorkOutCompany = (%s), FG = (%s) , CostsByWorker = (%s),
	tPropositionByWorker = (%s), tRevientByWorker = (%s), tMargeBrute = (%s), tMargeNet =(%s), tMargeNetPC=(%s)
    WHERE idWorker = (%s) and idOffre = (%s) '''
    ,(nbWorkOnCompanySend,nbWorkOnSiteSend,FGSend,coutByWorker,pricePropByWorker,priceRevByWorker,margeBrutte,margeNet,margeNetPC,
    idWorkerGlobaleSend,idOffreSendGlobaleSend))
    print("Sucesss")
    conn.commit()
    return 1


def insertIntoOffresStep3(idOffre):
    try:
        MyCursor.execute('''INSERT INTO OffresStep3(idOffre) VALUES(%s)''',(idOffre,))
        conn.commit()
        print("Sucess add into OffresStep3 table")
        return 1
    except:
        print("There is a problem please check your data on table OffresSte3")
        return 0

def insertIntoworkCGOffreStep3(idOffre,fullName,nbHWOC,nbHWOS,valueSend):
    try:      
        if fullName != "General costs":
            SelectRequette=""
            resultQuerry = MyCursor.execute('''SELECT idWorker,profCoefficient FROM WorkerCompany WHERE fullName = (%s)''',(fullName,))
            for x in MyCursor:
                SelectRequette = x
            #print(SelectRequette)

            SelectRequette2=""
            resultQuerry2 = MyCursor.execute('''SELECT H_jCostsOnCompany,H_jCostsOnSite FROM Salary WHERE idWorker = (%s) ''',(SelectRequette[0],))
            for x in MyCursor:
                SelectRequette2 = x
            # print(SelectRequette2[0])
            # print(SelectRequette2[1])


            priceRevByWorker = round(((SelectRequette2[1]*nbHWOS) + (SelectRequette2[0]*nbHWOC)),3)
            pricePropByWorker = round((((SelectRequette2[1]*SelectRequette[1])*nbHWOS) + ((SelectRequette2[0]*SelectRequette[1])*nbHWOC)),3)
            coutByWorker = round((priceRevByWorker + (priceRevByWorker * (valueSend / 100))),3)
            margeBrutte = round((pricePropByWorker - priceRevByWorker),3)
            margeNet = round((pricePropByWorker - coutByWorker))
            if margeNet ==0.0:
                margeNetPC = 0.0
            else:
                margeNetPC = round((margeNet / pricePropByWorker) * 100)
            # print("Price Revient: ",priceRevByWorker)
            # print("Price Proposition: ",pricePropByWorker)
            # print("Cout: ",coutByWorker)
            # print("Marge Brute: ",margeBrutte)
            # print("Marge Net: ",margeNet)
            # print("Marge Net: ",margeNetPC,"%")

            MyCursor.execute('''INSERT INTO workCGOffreForStep3(idWorker,idOffre,h_JWorkCompany,h_JWorkOutCompany,FG,CostsByWorker,tPropositionByWorker,tRevientByWorker,
            tMargeNet,tMargeBrute,tMargeNetPC) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(SelectRequette[0],idOffre,nbHWOC,nbHWOS,valueSend,coutByWorker,pricePropByWorker,priceRevByWorker
            ,margeBrutte,margeNet,margeNetPC))
            conn.commit()
            conn.commit()
            print("Sucess add into workCGOffre table")
        else:
            priceRevByWorker = round(((100*nbHWOS) + (50*nbHWOC)),3)
            pricePropByWorker = round((((100*2.5)*nbHWOS) + ((50*2.5)*nbHWOC)),3)
            coutByWorker = round((priceRevByWorker + (priceRevByWorker * (valueSend / 100))),3)
            margeBrutte = round((pricePropByWorker - priceRevByWorker),3)
            margeNet = round((pricePropByWorker - coutByWorker))
            if margeNet ==0.0:
                margeNetPC = 0.0
            else:
                margeNetPC = round((margeNet / pricePropByWorker) * 100)
            # print("Price Revient: ",priceRevByWorker)
            # print("Price Proposition: ",pricePropByWorker)
            # print("Cout: ",coutByWorker)
            # print("Marge Brute: ",margeBrutte)
            # print("Marge Net: ",margeNet)
            # print("Marge Net: ",margeNetPC,"%")

            MyCursor.execute('''INSERT INTO workCGOffreForStep3(idWorker,idOffre,h_JWorkCompany,h_JWorkOutCompany,FG,CostsByWorker,tPropositionByWorker,tRevientByWorker,
            tMargeNet,tMargeBrute,tMargeNetPC) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(1073,idOffre,nbHWOC,nbHWOS,valueSend,coutByWorker,pricePropByWorker,priceRevByWorker
            ,margeBrutte,margeNet,margeNetPC))
            conn.commit()
        print("Sucess add into workCGOffre3 table")

        return 1
    except:
        print("There is a problem in the table of workCGOffre")
        return 0

def getInformationFromWorkCGOffreStep3(idOffreSend,phoneNumberOfUser):
    SelectRequette1=""
    resultQuerry = MyCursor.execute('''SELECT companyId FROM Company WHERE phoneNumberClientCompany = (%s)''',(phoneNumberOfUser,))
    for x in MyCursor:
        SelectRequette1 = x[0]
    # print(SelectRequette1)


    SelectRequette2=[]
    resultQuerry2 = MyCursor.execute('''SELECT WC.fullName,WC.profileWork,WCG.h_JWorkCompany,WCG.h_JWorkOutCompany
    ,WCG.tPropositionByWorker,WCG.tRevientByWorker,WCG.CostsByWorker,WCG.FG,WCG.idWorker, WC.companyId FROM workCGOffreForStep3 WCG, WorkerCompany WC, 
    GlobalOffre GO WHERE (WCG.idWorker = WC.idWorker) and (WCG.idOffre = GO.idOffre) and (WCG.idOffre = (%s) and GO.companyId= (%s)) 
    ''',(idOffreSend,SelectRequette1))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequette2.append([x for x in row])

    #print(SelectRequette2)
    return SelectRequette2

def deleteAnWorkerFromOffreStep3UsingDB(workerProfileSend,imageProfileSend,idOffreSendGlobaleSend):
    
    SelectRequette=""
    resultQuerry = MyCursor.execute('''SELECT idWorker from WorkerCompany where fullName = (%s)''',(workerProfileSend,))
    for x in MyCursor:
            SelectRequette = x[0]
    # print(SelectRequette)

    resultQuerry = MyCursor.execute('''DELETE FROM workCGOffreForStep3 WHERE idWorker = %s and idOffre = %s''',(SelectRequette,idOffreSendGlobaleSend))
    conn.commit()
    print("Sucess delete this worker from WorkerCompany table")
    return 1

def calculPhase3OffreFromDB(idOffre):
    try:
        SelectRequette1=""
        resultQuerry = MyCursor.execute('''SELECT count(idOffre) FROM workCGOffreForStep3 WHERE idOffre = (%s)''',(idOffre,))
        for x in MyCursor:
            SelectRequette1 = x[0]
        # print(SelectRequette1)

        if SelectRequette1 == 0:
            # If you will using the update method you will using this lines
            MyCursor.execute('''UPDATE OffresStep3 SET CostsGlobale = %s, totaleProposition = %s, totaleRevient = %s, totaleQtyWork = %s, totaleMargeBrute=%s,
            totaleMargeNet =%s, totaleMargeNetPC =%s WHERE idOffre = %s''',(0,0,0,0,0,0,0,idOffre))
            print("Sucesss")
            return 1
                
        else:
            SelectRequette=[]
            resultQuerry = MyCursor.execute('''SELECT SUM(h_JWorkCompany),SUM(h_JWorkOutCompany),SUM(tPropositionByWorker),
            SUM(tRevientByWorker),SUM(CostsByWorker),SUM(tMargeBrute),SUM(tMargeNet) FROM workCGOffreForStep3 where idOffre = (%s) 
            GROUP BY idOffre''',(idOffre,))
            for x in MyCursor:
                SelectRequette.append(int(x[0]))
                SelectRequette.append(int(x[1]))
                SelectRequette.append(x[2])
                SelectRequette.append(x[3])
                SelectRequette.append(x[4])
                SelectRequette.append(x[5])
                SelectRequette.append(x[6])
                    
            totalDayOfWork = SelectRequette[0] + SelectRequette [1]
            totaleQtyWork = round(totalDayOfWork,2)
            totaleProposition = round(SelectRequette[2],3)
            totaleRevient = round(SelectRequette[3],3)
            CostsGlobale = round(SelectRequette[4],3)
            totaleMargeNet = round(SelectRequette[5],3)
            totaleMargeBrute = round(SelectRequette[6],3)

            print(totaleMargeBrute)

            
            if(totaleProposition==0):
                totaleMargeNetPC = 0
            else:
                totaleMargeNetPC = round(((totaleMargeNet / totaleProposition)*100),3)
            # print(totaleQtyWork)

            # If you will using the update method you will using this lines
            MyCursor.execute('''UPDATE OffresStep3 SET totaleQtyWork = (%s),totaleProposition = (%s), totaleRevient = (%s), CostsGlobale=(%s), totaleMargeBrute=(%s),
            totaleMargeNet =(%s), totaleMargeNetPC = (%s) WHERE idOffre = (%s)''',(totaleQtyWork,totaleProposition,totaleRevient,CostsGlobale,totaleMargeBrute,
            totaleMargeNet,totaleMargeNetPC,idOffre))

            # MyCursor.execute('''INSERT INTO OffresStep1(idOffre,totaleQtyWork,totaleProposition,totaleRevient,CostsGlobale,totaleMargeBrute,
            # totaleMargeNet,totaleMargeNetPC) VALUES(?,?,?,?,?,?,?,?)''',
            # (idOffre,totaleQtyWork,totaleProposition,totaleRevient,CostsGlobale,totaleMargeBrute,totaleMargeNet,totaleMargeNetPC))
            conn.commit()
            print("Sucess add into workCGOffre table")
            return 1
    except:
        print("There is a problem please check up3")
        return 0

def getInformationFromOffresStep3(idOffre,phoneNumberOfUser):
    # print(phoneNumberOfUser)
    SelectRequette1=""
    resultQuerry = MyCursor.execute('''SELECT companyId FROM Company WHERE phoneNumberClientCompany = (%s)''',(phoneNumberOfUser,))
    for x in MyCursor:
        SelectRequette1 = x[0]
    # print(SelectRequette1)

    SelectRequette2=[]
    resultQuerry = MyCursor.execute('''SELECT * from OffresStep3 OS1, GlobalOffre GO where (OS1.idOffre = GO.idOffre) and 
    OS1.idOffre = (%s) and GO.companyId = (%s)''',(idOffre,SelectRequette1,))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequette2.append([x for x in row])
    #print(SelectRequette2)

    return SelectRequette2


def updateInformationOfStep3ToDB(nbWorkOnCompanySend,nbWorkOnSiteSend,FGSend,workerNameGlobaleSend,idOffreSendGlobaleSend
    ,idWorkerGlobaleSend):
    
    if workerNameGlobaleSend != "General costs":
        SelectRequette=""
        resultQuerry = MyCursor.execute('''SELECT profCoefficient FROM WorkerCompany WHERE idWorker = (%s)''',(idWorkerGlobaleSend,))
        for x in MyCursor:
            SelectRequette = x
        #print(SelectRequette)

        SelectRequette2=""
        resultQuerry2 = MyCursor.execute('''SELECT H_jCostsOnCompany,H_jCostsOnSite FROM Salary WHERE idWorker = (%s) ''',(idWorkerGlobaleSend,))
        for x in MyCursor:
            SelectRequette2 = x
        # print(SelectRequette2[0])
        # print(SelectRequette2[1])


        priceRevByWorker = round(((SelectRequette2[1]*nbWorkOnSiteSend) + (SelectRequette2[0]*nbWorkOnCompanySend)),3)
        pricePropByWorker = round((((SelectRequette2[1]*SelectRequette[0])*nbWorkOnSiteSend) + ((SelectRequette2[0]*SelectRequette[0])*nbWorkOnCompanySend)),3)
        coutByWorker = round((priceRevByWorker + (priceRevByWorker * (FGSend / 100))),3)
        margeBrutte = round((pricePropByWorker - priceRevByWorker),3)
        margeNet = round((pricePropByWorker - coutByWorker))
        if margeNet ==0.0:
            margeNetPC = 0.0
        else:
            margeNetPC = round((margeNet / pricePropByWorker) * 100)
        # print("Price Revient: ",priceRevByWorker)
        # print("Price Proposition: ",pricePropByWorker)
        # print("Cout: ",coutByWorker)
        # print("Marge Brute: ",margeBrutte)
        # print("Marge Net: ",margeNet)
        # print("Marge Net: ",margeNetPC,"%")

        MyCursor.execute('''UPDATE workCGOffreForStep3 SET h_JWorkCompany = (%s), h_JWorkOutCompany = (%s), FG = (%s) , CostsByWorker = (%s),
	    tPropositionByWorker = (%s), tRevientByWorker = (%s), tMargeBrute = (%s), tMargeNet =(%s), tMargeNetPC=(%s)
        WHERE idWorker = (%s) and idOffre = (%s) '''
        ,(nbWorkOnCompanySend,nbWorkOnSiteSend,FGSend,coutByWorker,pricePropByWorker,priceRevByWorker,margeBrutte,margeNet,margeNetPC,
        idWorkerGlobaleSend,idOffreSendGlobaleSend))
        print("Sucesss")
        conn.commit()

    else:
        priceRevByWorker = round(((100*nbWorkOnSiteSend) + (50*nbWorkOnCompanySend)),3)
        pricePropByWorker = round((((100*2.5)*nbWorkOnSiteSend) + ((50*2.5)*nbWorkOnCompanySend)),3)
        coutByWorker = round((priceRevByWorker + (priceRevByWorker * (FGSend / 100))),3)
        margeBrutte = round((pricePropByWorker - priceRevByWorker),3)
        margeNet = round((pricePropByWorker - coutByWorker))
        if margeNet ==0.0:
            margeNetPC = 0.0
        else:
            margeNetPC = round((margeNet / pricePropByWorker) * 100)
            # print("Price Revient: ",priceRevByWorker)
            # print("Price Proposition: ",pricePropByWorker)
            # print("Cout: ",coutByWorker)
            # print("Marge Brute: ",margeBrutte)
            # print("Marge Net: ",margeNet)
            # print("Marge Net: ",margeNetPC,"%")

        MyCursor.execute('''UPDATE workCGOffreForStep3 SET h_JWorkCompany = (%s), h_JWorkOutCompany = (%s), FG = (%s) , CostsByWorker = (%s),
	    tPropositionByWorker = (%s), tRevientByWorker = (%s), tMargeBrute = (%s), tMargeNet =(%s), tMargeNetPC=(%s)
        WHERE idWorker = (%s) and idOffre = (%s) '''
        ,(nbWorkOnCompanySend,nbWorkOnSiteSend,FGSend,coutByWorker,pricePropByWorker,priceRevByWorker,margeBrutte,margeNet,margeNetPC,
        1073,idOffreSendGlobaleSend))
        print("Sucesss")
        conn.commit()
    print("Sucess update into workCGOffre3 table")

    return 1


def offreFinaleCalculDB(idOffreSend):

    print(idOffreSend)
    SelectRequette1=""
    resultQuerry = MyCursor.execute('''SELECT totaleProposition,totaleRevient,CostsGlobale,totaleMargeBrute,
    totaleMargeNet FROM OffresStep1 WHERE idOffre = (%s)''',(idOffreSend,))
    for x in MyCursor:
        SelectRequette1 = x
    print(SelectRequette1)

    SelectRequette2=""
    resultQuerry = MyCursor.execute('''SELECT totaleProposition,totaleRevient,CostsGlobale,totaleMargeBrute,
    totaleMargeNet FROM OffresStep2 WHERE idOffre = (%s)''',(idOffreSend,))
    for x in MyCursor:
        SelectRequette2 = x
    #print(SelectRequette2)

    SelectRequette3=""
    resultQuerry = MyCursor.execute('''SELECT totaleProposition,totaleRevient,CostsGlobale,totaleMargeBrute,
    totaleMargeNet FROM OffresStep3 WHERE idOffre = (%s)''',(idOffreSend,))
    for x in MyCursor:
        SelectRequette3 = x
    #print(SelectRequette3)

    globalProposition = SelectRequette1[0] + SelectRequette2[0] + SelectRequette3[0]
    globalRevient = SelectRequette1[1] + SelectRequette2[1] + SelectRequette3[1]
    globalRevientAndFG = SelectRequette1[2] + SelectRequette2[2] + SelectRequette3[2]
    globalMargeBrute = SelectRequette1[3] + SelectRequette2[3] + SelectRequette3[3]
    globalMargeNete = SelectRequette1[4] + SelectRequette2[4] + SelectRequette3[4]
        
    globalPropositionFinale = round(globalProposition,3)
    globalRevientFinale = round(globalRevient,3)
    globalRevientAndFGFinale = round(globalRevientAndFG,3)
    globalMargeBruteFinale = round(globalMargeBrute,3)
    globalMargeNeteFinale = round(globalMargeNete,3)

    if globalPropositionFinale == 0:
        globalFinaleMarge = 0
    else:
        globalFinaleMarge = (globalMargeNeteFinale / globalPropositionFinale)*100

    # # print(globalProposition)
    # # print(globalRevient)
    # # print(globalRevientAndFG)
    # # print(globalMargeBrute)
    # # print(globalMargeNete)
    # # print(globalFinaleMargeFinale)

    resultQuerry = MyCursor.execute('''UPDATE GlobalOffre SET globalProposition = %s,globalRevient = %s,globalRevientAndFG = %s,globalMargeBrute = %s,
    globalMargeNete = %s, globalFinaleMarge = %s WHERE idOffre = %s''',(globalPropositionFinale,globalRevientFinale,globalRevientAndFGFinale,
    globalMargeBruteFinale,globalMargeNeteFinale,globalFinaleMarge,idOffreSend))
    conn.commit()
    return 1

def getAllInformationOfOffreStep1FromDB(idOffreSend,phoneNumberOfUser):
    SelectRequette=[]
    resultQuerry = MyCursor.execute('''SELECT * from OffresStep1 WHERE idOffre = %s''',(idOffreSend,))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequette.append([x for x in row])    
    
    # print(SelectRequette)
    return SelectRequette

def getAllInformationOfOffreStep2FromDB(idOffreSend,phoneNumberOfUser):
    SelectRequette=[]
    resultQuerry = MyCursor.execute('''SELECT * from OffresStep2 WHERE idOffre = %s''',(idOffreSend,))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequette.append([x for x in row])    
    
    # print(SelectRequette)
    return SelectRequette

def getAllInformationOfOffreStep3FromDB(idOffreSend,phoneNumberOfUser):
    SelectRequette=[]
    resultQuerry = MyCursor.execute('''SELECT * from OffresStep3 WHERE idOffre = %s''',(idOffreSend,))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequette.append([x for x in row])    
    
    print(SelectRequette)
    return SelectRequette

def getAllInformationOfAnWorkerFromDBForStep2(idOffreSend,phoneNumberOfUser):
    SelectRequette=[]
    resultQuerry = MyCursor.execute('''SELECT WCGO2.*,WC.profileWork,WC.fullName from workCGOffreForStep2 WCGO2, WorkerCompany WC WHERE WCGO2.idOffre = %s and
    WCGO2.idWorker = WC.idWorker''',(idOffreSend,))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequette.append([x for x in row])
    return SelectRequette

def getAllInformationOfAnWorkerFromDBForStep3(idOffreSend,phoneNumberOfUser):
    SelectRequette=[]
    resultQuerry = MyCursor.execute('''SELECT WCGO3.*,WC.profileWork,WC.fullName from workCGOffreForStep3 WCGO3, WorkerCompany WC WHERE WCGO3.idOffre = %s and
    WCGO3.idWorker = WC.idWorker''',(idOffreSend,))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequette.append([x for x in row])
    return SelectRequette
        
def getAllInformationOfAnWorkerFromDB(idOffreSend,phoneNumberOfUser):
    SelectRequette=[]
    resultQuerry = MyCursor.execute('''SELECT WCGO.*,WC.profileWork,WC.fullName from workCGOffre WCGO, WorkerCompany WC WHERE WCGO.idOffre = %s and
    WCGO.idWorker = WC.idWorker''',(idOffreSend,))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequette.append([x for x in row])

    print(SelectRequette)

    return SelectRequette

getAllInformationOfAnWorkerFromDB("JustGroup-01","+21653786397")


def getInformationOffreFinale(idOffreSend):
    SelectRequette=[]
    resultQuerry = MyCursor.execute('''SELECT * from GlobalOffre WHERE idOffre = %s''',(idOffreSend,))
    rows = MyCursor.fetchall()
    for row in rows:
        SelectRequette.append([x for x in row])
    # print(SelectRequette)
    return SelectRequette



# Testing the function part
#getInformationOffreFinale("Eniso-01")
#checkIntoGlobalOffre("Eniso-0111","+216 53 786 397")
#getInformationFromOffresStep1("JustGroup-01")
#getInformationFromWorkCGOffre("JustGroup-01")

#insertIntoworkCGOffre("JustGroup-01","Mohamed Ali Jaziri",18,4,70)
#insertIntoworkCGOffre("Mohamed Ali Jaziri",16,4,70)
#getAllWorkerNameFromDB()
#GetAllWorkerCompanyFromDB()
#getInformationClientFromDB("meddalijaziri@gmail.com")

#modifCodeSMSUsePhoneNb("meddalijaziri@gmail.com")

#sendSMSUsePhoneNb("+216 20 855 417")
#sendSMSUsePhoneNb("+216 53 786 397")

#sendSMSValidation("meddalijaziri@gmail.com")
#resultSignUp = sginUpCompany("JaziriMeca","Industry","Tunisia","3-10 employees","Tunisia Dinars","+216 22 450 528")
#print(resultSignUp)
#print(getImagesFromDB())
#signInWithEmailAndPassword("meddalijaziri@gmail.com","123")