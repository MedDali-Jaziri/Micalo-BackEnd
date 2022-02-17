from os import name
from flask import Flask
from flask import redirect,request, jsonify,make_response
from flask_cors import CORS, cross_origin
#import face_recognition

from BackEndScriptClient import *



# creates a Flask application, named app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
def index():
    return 'Hello World 2022 !!'


@app.route("/client/signupClient", methods=['POST'])
@cross_origin()
def signUpClient():
    req = request.json 
    dataSend = req['dataSend']
    imageUser = req['imageUser']
    imageEncoding=""
    if(imageUser=="0"):
        print("There is non image in this profile")
        imageUser = " "
        imageEncoding = " "
        # print(imageUser)

    firstName = dataSend["firstName"]
    lastName = dataSend["lastName"]
    emailUser = dataSend["emailUser"]
    phoneUser = dataSend["phoneUser"]
    passwordUser = dataSend["passwordUser"]

    # print(firstName)
    # print(lastName)
    # print(emailUser)
    # print(phoneUser)
    # print(passwordUser)

    if(not imageUser): 
        base64_to_image(imageUser,"./imageBack\ImageForEncoding.jpg")
        image = face_recognition.load_image_file("./imageBack\ImageForEncoding.jpg")
        imageEncoding = face_recognition.face_encodings(image)[0]
        # print(type(str(imageEncoding)))
    
    resultSignUp = sginUpClient(firstName,lastName,emailUser,phoneUser,passwordUser,imageUser)
    # print(resultSignUp)

    response_body = {
        "test" : "test",
        "resultSignUp": resultSignUp # 0: the phone number is use it | 1: ok ok
    }
    return jsonify(response_body)


@app.route("/client/signIn", methods=['POST'])
@cross_origin()
def signInClient():
    req = request.json 
    dataSend = req['dataSend']
    emailAdress = dataSend["emailAdress"]
    passwordUser = dataSend["passwordUser"]


    faceRecogn = req['faceRecogn']
    print("******** SignIn ********")
    # # print(emailAdress)
    # # print(passwordUser)
    # #print(faceRecogn)

    # if(faceRecogn == "../assets/img/default-avatar.jpg" or not faceRecogn):
    #     print("We don't work with face recogniton")
    #     #print(emailAdress)
    #     #print(passwordUser)
    #     resultLogin = signInWithEmailAndPassword(emailAdress,passwordUser)
    #     if(not resultLogin):
    #         variableLogin = 0
    #         print("Login not sucess")
    #     else:
    #         variableLogin = 1
    #         #print(resultLogin)
    #         print("Login sucess")
    #         response_body = {
    #         "variableLogin" : variableLogin,
    #         "resultLogin": resultLogin
    #         }
    #         #You should to remove the comm in the next line
    #         #sendSMSValidation(emailAdress)

    # #There is some problem in the methode of face recognition and we will see it soon
    # else:
    #     base64_to_image(faceRecogn,"./imageBack\ImageFromAngularApplication.jpg")
    #     ImageFromAngularApplication = "./imageBack\ImageFromAngularApplication.jpg"
    #     resultLogin = getImagesFromDB(ImageFromAngularApplication)

    #     if(not resultLogin):
    #         variableLogin = 0
    #         print("Login not sucess")
    #     else:
    #         variableLogin = 1
    #         print("Login sucess")
    #         #sendSMSValidation(emailAdress)
    #         response_body = {
    #         "variableLogin" : variableLogin,
    #         "resultLogin" : resultLogin
    #         }
    #         return jsonify(response_body)

    resultLogin = signInWithEmailAndPassword(emailAdress,passwordUser)
    if(not resultLogin):
        variableLogin = 0
        print("Login not sucess")
    else:
        variableLogin = 1
        print("Login sucess")
        #sendSMSValidation(emailAdress)
    response_body = {
        "variableLogin" : variableLogin,
        "resultLogin" : resultLogin
    }
    #You should to remove the comm in the next line
    #sendSMSValidation(emailAdress)
    return jsonify(response_body)


@app.route("/company/signupCompany", methods=['POST'])
@cross_origin()
def signupCompany():
    req = request.json 
    dataSend = req['dataSend']
    nameCompany = dataSend["nameCompany"]
    companAct = dataSend["companAct"]
    country = dataSend["country"]
    numberWorker = dataSend["numberWorker"]
    currency = dataSend["currency"]
    phoneUser = dataSend["phoneUser"]

    # print(nameCompany)
    resultSignUpCompany = sginUpCompany(nameCompany,companAct,country,currency,phoneUser)

    # print(resultSignUpCompany)

    response_body = {
        "test" : "test",
        "resultSignUpCompany": resultSignUpCompany # 0: the name of company is use it | 1: ok ok
    }
    return jsonify(response_body)


@app.route("/client/sendAnotherCodePhone", methods=['POST'])
@cross_origin()
def sendAnotherCodePhone():
    req = request.json 
    phoneNumberToAnCodeLocal = req['phoneNumberToAnCodeLocal']
    # print(phoneNumberToAnCodeLocal)
    sendSMSUsePhoneNb(phoneNumberToAnCodeLocal)

    response_body = {
        "test" : "test",
    }

    return jsonify(response_body)

@app.route("/client/checkCodeNotif", methods=['POST'])
@cross_origin()
def checkCodeNotif():
    req = request.json 
    dataSend = req['dataSend']
    codeNotif = dataSend['codeNotif']
    # print(codeNotif)

    resutFunction = checkTheCodeFromDB(codeNotif)

    if(not resutFunction):
        variableCodeCheck = 0
        print("There's not code !")
    else:
        variableCodeCheck=1
        print("The code it's right !")
        response_body = {
            "variableCodeCheck" : variableCodeCheck,
        }
        return jsonify(response_body)

    response_body = {
        "variableCodeCheck" : variableCodeCheck
    }
    return jsonify(response_body)


@app.route("/client/getInformationClient", methods=['POST'])
@cross_origin()
def getInformationClient():
    print("**************** Inormation Of Client ****************")
    req = request.json 
    dataSend2 = req['dataSend2']
    # print(dataSend2)
    emailAdress = dataSend2['emailAdress']
    print(emailAdress)

    resutFunction = getInformationClientFromDB(emailAdress)
    #print(resutFunction)
    # print(type(resutFunction))
    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)


@app.route("/company/getInformationFromCompanyDB", methods=['POST'])
@cross_origin()
def getInformationFromCompanyDB():
    print("**************** Inormation Of Company ****************")
    req = request.json 
    phoneUserNumber = req['phoneUserNumber']
    # print(phoneUserNumber)

    resutFunction = getInformationCompanyDB(phoneUserNumber)
    #print(resutFunction)
    # print(type(resutFunction))
    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)

@app.route("/company/EditInformationOfCompany", methods=['POST'])
@cross_origin()
def EditInformationOfCompany():
    print("**************** Edit Information Of Company ****************")
    req = request.json 
    phoneUserNumber = req['phoneUserNumber']
    nameCompanySend = req['nameCompanySend']
    telePhoneSend = req['telePhoneSend']
    cellNumberSend = req['cellNumberSend']
    webSiteSend = req['webSiteSend']
    firstNameProfileSend = req['firstNameProfileSend']
    lastNameProfileSend = req['lastNameProfileSend']
    emailUserCompanySend = req['emailUserCompanySend']
    citySend = req['citySend']
    zipCodeSend = req['zipCodeSend']
    logoCompanySend = req['logoCompanySend']
    addressCompanySend = req['addressCompanySend']
    taxRegNumSend = req['taxRegNumSend']

    # print(zipCodeSend)
    resutFunction = EditInformationOfCompanyDB(phoneUserNumber,nameCompanySend,telePhoneSend,cellNumberSend,webSiteSend,firstNameProfileSend,
    lastNameProfileSend,emailUserCompanySend,citySend,zipCodeSend,logoCompanySend,addressCompanySend,taxRegNumSend)
    # print(resutFunction)
    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)

@app.route("/client/ClientCompany", methods=['POST'])
@cross_origin()
def getInformationFromClientDB():
    print("**************** Inormation Of Client ****************")
    req = request.json 
    phoneUserNumber = req['phoneUserNumber']
    # print(phoneUserNumber)

    resutFunction = getInformationClientDB(phoneUserNumber)
    #print(resutFunction)
    # print(type(resutFunction))
    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)

@app.route("/client/updateInfoClientCompany", methods=['POST'])
@cross_origin()
def editInfoClientCompany():
    print("**************** Edit Information Of Client Company ****************")
    req = request.json 
    phoneUserNumber = req['phoneUserNumber']
    userProfileImageToDB = req['userProfileImageToDB']
    FirstNameToDB = req['FirstNameToDB']
    LastNameToDB = req['LastNameToDB']
    emailProfileToDB = req['emailProfileToDB']
    passwordProfileToDB = req['passwordProfileToDB']

    # print(zipCodeSend)
    resutFunction = EditInformationOfClientCompanyDB(phoneUserNumber,userProfileImageToDB,FirstNameToDB,LastNameToDB,emailProfileToDB,passwordProfileToDB)
    # print(resutFunction)
    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)

@app.route("/company/AddWorkerInDB", methods=['POST'])
@cross_origin()
def AddWorkerInDB():
    print("**************** ADD Worker In DB  ****************")
    req = request.json 
    phoneNumberOfUser = req['phoneNumberOfUser']
    profileWorker = req['imageProfileForUserSend']
    dataSend = req['dataSend']
    fullName = dataSend['fullName']
    professionWorker = dataSend['professionWorker']
    professionCoefficient = dataSend['professionCoefficient']
    departName = dataSend['departName']
    GrossSalary = dataSend['GrossSalary']
    resutFunction = AddWorkerInDataBase(phoneNumberOfUser,fullName,professionWorker,professionCoefficient,profileWorker,departName,GrossSalary)
    # print(resutFunction)
    response_body = {
        "resutFunction" : resutFunction,
    }
    return jsonify(response_body)


@app.route("/company/updateInfoWorkerCompany", methods=['POST'])
@cross_origin()
def updateInfoWorkerCompany():
    print("**************** Update Info Worker Company In DB  ****************")
    req = request.json 
    userProfileImageSend = req['userProfileImageSend']
    departmentNameWorkerSend = req['departmentNameWorkerSend']
    professionWorkerSend = req['professionWorkerSend']
    profitCofficientWorkerSend = req['profitCofficientWorkerSend']
    salaryWorkerSend = req['salaryWorkerSend']
    fullNameWorkerSend = req['fullNameWorkerSend']
    idWorkerSend = req['idWorkerSend']

    resutFunction = updateInfoWorkerCompanyInDB(userProfileImageSend,departmentNameWorkerSend,professionWorkerSend,
    profitCofficientWorkerSend,salaryWorkerSend,fullNameWorkerSend,idWorkerSend)
    # print(resutFunction)
    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)





@app.route("/company/addInTableSalary", methods=['POST'])
@cross_origin()
def addInTableSalary():
    print("**************** ADD Salary In DB  ****************")
    req = request.json 
    dataSend = req['dataSend']
    fullName = dataSend['fullName']
    professionWorker = dataSend['professionWorker']
    GrossSalary = dataSend['GrossSalary']

    resutFunction = AddInTableSalary(fullName,professionWorker,GrossSalary)
    # print(resutFunction)
    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)

@app.route("/company/GetAllWorkerCompany", methods=['POST'])
@cross_origin()
def GetAllWorkerCompany():
    print("**************** GET Worker From DB  ****************")
    req = request.json 
    phoneNumberOfUser = req['phoneNumberOfUser']

    resutFunction = GetAllWorkerCompanyFromDB(phoneNumberOfUser)

    #print(resutFunction)
    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)

@app.route("/company/deleteWorkerFromDB", methods=['POST'])
@cross_origin()
def deleteWorkerFromDB():
    print("**************** Delete Worker From DB  ****************")
    req = request.json 
    idWorker = req['idWorker']
    fullNameWorker = req['fullNameWorker']

    # print(idWorker)
    # print(fullNameWorker)
    resutFunction = deleteWorkerFromDataBase(idWorker,fullNameWorker)

    # print(type(resutFunction))
    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)

@app.route("/company/getAllWorkerName", methods=['POST'])
@cross_origin()
def getAllWorkerName():
    print("**************** get all name of Worker From DB  ****************")
    req = request.json 
    phoneNumberOfUser = req['phoneNumberOfUser']

    resutFunction = getAllWorkerNameFromDB(phoneNumberOfUser)

    # print(type(resutFunction))
    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)

@app.route("/company/Step1Offre", methods=['POST'])
@cross_origin()
def Step1Offre():
    print("**************** Step1 Offre  From DB  ****************")
    req = request.json 
    dataSend = req['dataSend']
    idOffre = dataSend['idOffre']
    fullName = dataSend['fullName']
    nbHWOC = dataSend['nbHWOC']
    nbHWOS = dataSend['nbHWOS']
    valueSend = req['valueSend']
    phoneNumberOfUser = req['phoneNumberOfUser']
    
    resutFunction1 = insertIntoGlobalOffre(idOffre,phoneNumberOfUser)
    #Not now the next script
    resutFunction2 = insertIntoOffresStep1(idOffre)
    resutFunction3 = insertIntoworkCGOffre(idOffre,fullName,nbHWOC,nbHWOS,valueSend)
    # if(resutFunction1==1 and resutFunction3==1):
    #     resutFunction = 1
    # else:
    #     resutFunction = 0
    resutFunction = 1
    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)

@app.route("/company/getOffreById", methods=['POST'])
@cross_origin()
def getOffreById():
    print("**************** get Offre By Id Offre From DB  ****************")
    req = request.json 
    idOffreSend = req['idOffreSend']
    phoneNumberOfUser = req['phoneNumberOfUser']
    resutFunctionGIFWCGO = getInformationFromWorkCGOffre(idOffreSend,phoneNumberOfUser)

    response_body = {
        "resutFunctionGIFWCGO" : resutFunctionGIFWCGO,
    }
    return jsonify(response_body)

@app.route("/company/getOffreStep2ById", methods=['POST'])
@cross_origin()
def getOffreStep2ById():
    print("**************** get Offre Step2 By Id Offre From DB  ****************")
    req = request.json 
    idOffreSend = req['idOffreSend']
    phoneNumberOfUser = req['phoneNumberOfUser']
    resutFunctionGIFWCGO = getInformationFromWorkCGOffreStep2(idOffreSend,phoneNumberOfUser)

    response_body = {
        "resutFunctionGIFWCGO" : resutFunctionGIFWCGO,
    }
    return jsonify(response_body)

@app.route("/company/updateInformationOfStep1", methods=['POST'])
@cross_origin()
def updateInformationOfStep1():
    print("**************** update Information of step1 offre ****************")
    req = request.json 
    workerNameGlobaleSend = req['workerNameGlobaleSend']
    FGSend = req['FGSend']
    nbWorkOnCompanySend = req['nbWorkOnCompanySend']
    nbWorkOnSiteSend = req['nbWorkOnSiteSend']
    idWorkerNameSend = req['idWorkerNameSend']
    idOffreSendGlobaleSend = req['idOffreSendGlobaleSend']
    resutFunction = updateInformationOfStep1ToDB(FGSend,
    nbWorkOnCompanySend,nbWorkOnSiteSend,idWorkerNameSend,idOffreSendGlobaleSend)

    response_body = {
        "resutFunction" : resutFunction,
    }
    return jsonify(response_body)

@app.route("/company/calculPhase1Offre", methods=['POST'])
@cross_origin()
def calculPhase1Offre():
    print("**************** calcul Phase1 Offre From DB  ****************")
    req = request.json 
    idOffreSend = req['idOffreSend']
    phoneNumberOfUser = req['phoneNumberOfUser']
    resutFunction1 = calculPhase1OffreFromDB(idOffreSend)
    resutFunction = getInformationFromOffresStep1(idOffreSend,phoneNumberOfUser)
    # print(resutFunction)

    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)

@app.route("/company/deleteAnWorkerFromOffre", methods=['POST'])
@cross_origin()
def deleteAnWorkerFromOffre():
    print("**************** delete An Worker From Offre From DB  ****************")
    req = request.json 
    workerProfileSend = req['workerProfileSend']
    imageProfileSend = req['imageProfileSend']
    idOffreSendGlobaleSend = req['idOffreSendGlobaleSend']
    resutFunction = deleteAnWorkerFromOffreUsingDB(workerProfileSend,imageProfileSend,idOffreSendGlobaleSend)
    resultFunction = calculPhase1OffreFromDB(idOffreSendGlobaleSend)
    # print(resutFunction)

    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)

@app.route("/company/deleteAnWorkerFromOffreStep2", methods=['POST'])
@cross_origin()
def deleteAnWorkerFromOffreStep2():
    print("**************** delete An Worker From Offre From DB  ****************")
    req = request.json 
    workerProfileSend = req['workerProfileSend']
    imageProfileSend = req['imageProfileSend']
    idOffreSendGlobaleSend = req['idOffreSendGlobaleSend']
    resutFunction = deleteAnWorkerFromOffreStep2UsingDB(workerProfileSend,imageProfileSend,idOffreSendGlobaleSend)
    resultFunction = calculPhase2OffreFromDB(idOffreSendGlobaleSend)
    # print(resutFunction)

    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)

@app.route("/company/Step2Offre", methods=['POST'])
@cross_origin()
def Step2Offre():
    print("**************** Step 2 Offre  From DB  ****************")
    req = request.json 
    dataSend = req['dataSend']
    idOffre = dataSend['idOffre']
    fullName = dataSend['fullName']
    nbHWOC = dataSend['nbHWOC']
    nbHWOS = dataSend['nbHWOS']
    valueSend = req['valueSend']
    phoneNumberOfUser = req['phoneNumberOfUser']
    
    resutFunction1 = checkIntoGlobalOffre(idOffre,phoneNumberOfUser)
    if(resutFunction1 == 1):
        #Not now the next script
        resutFunction2 = insertIntoOffresStep2(idOffre)
        resutFunction3 = insertIntoworkCGOffreStep2(idOffre,fullName,nbHWOC,nbHWOS,valueSend)
        resutFunction = 1
    else:
        resutFunction = 0
    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)


@app.route("/company/calculPhase2Offre", methods=['POST'])
@cross_origin()
def calculPhase2Offre():
    print("**************** calcul Phase2 Offre From DB  ****************")
    req = request.json 
    idOffreSend = req['idOffreSend']
    phoneNumberOfUser = req['phoneNumberOfUser']
    resutFunction1 = calculPhase2OffreFromDB(idOffreSend)
    resutFunction = getInformationFromOffresStep2(idOffreSend,phoneNumberOfUser)
    # print(resutFunction)

    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)

@app.route("/company/updateInformationOfStep2", methods=['POST'])
@cross_origin()
def updateInformationOfStep2():
    print("**************** update Information of step2 offre ****************")
    req = request.json 
    nbWorkOnCompanySend = req['nbWorkOnCompanySend']
    nbWorkOnSiteSend = req['nbWorkOnSiteSend']
    FGSend = req['FGSend']
    workerNameGlobaleSend = req['workerNameGlobaleSend']
    idOffreSendGlobaleSend = req['idOffreSendGlobaleSend']
    idWorkerGlobaleSend = req['idWorkerGlobaleSend']

    resutFunction = updateInformationOfStep2ToDB(nbWorkOnCompanySend,nbWorkOnSiteSend,FGSend,workerNameGlobaleSend,idOffreSendGlobaleSend
    ,idWorkerGlobaleSend)

    response_body = {
        "resutFunction" : resutFunction,
    }
    return jsonify(response_body)

@app.route("/company/Step3Offre", methods=['POST'])
@cross_origin()
def Step3Offre():
    print("**************** Step 3 Offre  From DB  ****************")
    req = request.json 
    dataSend = req['dataSend']
    idOffre = dataSend['idOffre']
    fullName = dataSend['fullName']
    nbHWOC = dataSend['nbHWOC']
    nbHWOS = dataSend['nbHWOS']
    valueSend = req['valueSend']
    phoneNumberOfUser = req['phoneNumberOfUser']

    # print(idOffre)
    # print(fullName)
    # print(nbHWOC)
    # print(nbHWOS)
    # print(valueSend)
    # print(phoneNumberOfUser)

    resutFunction1 = checkIntoGlobalOffre(idOffre,phoneNumberOfUser)
    if(resutFunction1 == 1):
        #Not now the next script
        resutFunction2 = insertIntoOffresStep3(idOffre)
        resutFunction3 = insertIntoworkCGOffreStep3(idOffre,fullName,nbHWOC,nbHWOS,valueSend)
        resutFunction = 1
    else:
        resutFunction = 0
    response_body = {
        "resutFunction3" : resutFunction
    }
    return jsonify(response_body)

@app.route("/company/getOffreStep3ById", methods=['POST'])
@cross_origin()
def getOffreStep3ById():
    print("**************** get Offre Step3 By Id Offre From DB  ****************")
    req = request.json 
    idOffreSend = req['idOffreSend']
    phoneNumberOfUser = req['phoneNumberOfUser']
    resutFunctionGIFWCGO = getInformationFromWorkCGOffreStep3(idOffreSend,phoneNumberOfUser)

    response_body = {
        "resutFunctionGIFWCGO" : resutFunctionGIFWCGO,
    }
    return jsonify(response_body)

@app.route("/company/deleteAnWorkerFromOffreStep3", methods=['POST'])
@cross_origin()
def deleteAnWorkerFromOffreStep3():
    print("**************** delete An Worker From Offre From DB  ****************")
    req = request.json 
    workerProfileSend = req['workerProfileSend']
    imageProfileSend = req['imageProfileSend']
    idOffreSendGlobaleSend = req['idOffreSendGlobaleSend']
    resutFunction = deleteAnWorkerFromOffreStep3UsingDB(workerProfileSend,imageProfileSend,idOffreSendGlobaleSend)
    resultFunction = calculPhase3OffreFromDB(idOffreSendGlobaleSend)

    # print(resutFunction)

    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)


@app.route("/company/calculPhase3Offre", methods=['POST'])
@cross_origin()
def calculPhase3Offre():
    print("**************** calcul Phase3 Offre From DB  ****************")
    req = request.json 
    idOffreSend = req['idOffreSend']
    phoneNumberOfUser = req['phoneNumberOfUser']
    resutFunction1 = calculPhase3OffreFromDB(idOffreSend)
    resutFunction = getInformationFromOffresStep3(idOffreSend,phoneNumberOfUser)
    # print(resutFunction)

    response_body = {
        "resutFunction" : resutFunction
    }
    return jsonify(response_body)


@app.route("/company/updateInformationOfStep3", methods=['POST'])
@cross_origin()
def updateInformationOfStep3():
    print("**************** update Information of step3 offre ****************")
    req = request.json 
    nbWorkOnCompanySend = req['nbWorkOnCompanySend']
    nbWorkOnSiteSend = req['nbWorkOnSiteSend']
    FGSend = req['FGSend']
    workerNameGlobaleSend = req['workerNameGlobaleSend']
    idOffreSendGlobaleSend = req['idOffreSendGlobaleSend']
    idWorkerGlobaleSend = req['idWorkerGlobaleSend']

    resutFunction = updateInformationOfStep3ToDB(nbWorkOnCompanySend,nbWorkOnSiteSend,FGSend,workerNameGlobaleSend,idOffreSendGlobaleSend
    ,idWorkerGlobaleSend)

    response_body = {
        "resutFunction" : resutFunction,
    }
    return jsonify(response_body)



@app.route("/company/getAllInformationOfAnWorker", methods=['POST'])
@cross_origin()
def getAllInformationOfAnWorker():
    print("**************** Get All Information Of AnWorker From DB  ****************")
    req = request.json
    idOffreSend = req['idOffreSend']
    phoneNumberOfUser = req['phoneNumberOfUser']
    resutFunction1 = getAllInformationOfAnWorkerFromDB(idOffreSend,phoneNumberOfUser)
    resutFunction2 = getAllInformationOfOffreStep1FromDB(idOffreSend,phoneNumberOfUser)
    resutFunction3 = getAllInformationOfAnWorkerFromDBForStep2(idOffreSend,phoneNumberOfUser)
    resutFunction4 = getAllInformationOfOffreStep2FromDB(idOffreSend,phoneNumberOfUser)
    resutFunction5 = getAllInformationOfAnWorkerFromDBForStep3(idOffreSend,phoneNumberOfUser)
    resutFunction6 = getAllInformationOfOffreStep3FromDB(idOffreSend,phoneNumberOfUser)
    resutFunction7 = offreFinaleCalculDB(idOffreSend)
    resutFunction8 = getInformationOffreFinale(idOffreSend)
    # print(resutFunction6)
    response_body = {
        "resutFunction1" : resutFunction1,
        "resutFunction2" : resutFunction2,
        "resutFunction3" : resutFunction3,
        "resutFunction4" : resutFunction4,
        "resutFunction5" : resutFunction5,
        "resutFunction6" : resutFunction6,
        "resutFunction8" : resutFunction8,
    }
    return jsonify(response_body)

# @app.route("/company/offreFinale", methods=['POST'])
# @cross_origin()
# def offreFinale():
#     print("**************** offreFinale From DB  ****************")
#     req = request.json 
#     idOffreSend = req['idOffreSend']
#     phoneNumberOfUser = req['phoneNumberOfUser']
#     resutFunction1 = offreFinaleCalculDB(idOffreSend)
#     resutFunction2 = getInformationOffreFinale(idOffreSend)

#     response_body = {
#         "resutFunction2" : resutFunction2
#     }
#     return jsonify(response_body)

# run the application
if __name__ == "__main__":
    app.run(debug=True)