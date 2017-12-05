from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from .models import User
from .forms import UploadFileForm
from datetime import datetime   
from user_agents import parse
from django.conf import settings
import smtplib as mail, random, string ,platform
import os

# Create your views here.
def index(request): 
    return render(request, 'index.html')

def login(request):
    email = request.POST.get('txtEmail')
    password = request.POST.get('txtPassword')   
    data = {
        "message_error": ""
    }
    #Server Side Validation     
    validateMsg = validate(email=email, password=password)
    if validateMsg != "OK": 
        data["message_error"]= validateMsg 
        return JsonResponse(data)

    # Case Of Validation Success
    user = User.objects.filter(email = email, password= password)   
    if user.count(): 
        # Case Of Authentication Successe
        request.session["useremail"] = user[0].email
        request.session["username"] = user[0].name
        return JsonResponse(data)

    # Case Of Authentication Fail
    message_error = "Authentication Failed !"
    data["message_error"]= message_error 
    return JsonResponse(data)
def successLogin(request): 
    username = request.session.get("username") 
    if username:
        return render(request, 'success.html', {'username': username})
    return render(request, 'index.html', {'message_error': 'You Must Login'})
def forgetPassword(request):
    return render(request, 'recover-password.html')
def sendResetCode(request): 
    email = request.GET.get('email')
    #Server Side Validation 
    message_error = ""
    #Validate Email 
    validateMsg = validate(email=email)
    if validateMsg !="OK":
        return render(request, 'index.html', {'message_error':validateMsg})         

    # Case Of Validation Success
    user = User.objects.filter(email = email)

    # Case Of Email Not Exist
    if user.count() == 0 : 
        return render(request, 'index.html', {'message_error':'Email Not Exists'})

    # Case Of Exist 
    # 1- Generate Code Of 10 digits (Letters & Numbers)
    resetCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    # 2- Save Reset Code To DB 
    user = user[0]
    user.passwordResetCode = resetCode
    user.passwordResetCodeTime = datetime.now()
    user.save()

    # 3- Send The Email With The Reset Code
    if sendCode(email, resetCode):
        message_success = "The Reset Code Has Been Sent Successfully"
        return render (request, 'recover-password.html',{'message_success' :message_success})
    return render (request, 'recover-password.html',{'message_error' :'Error Sending Mail'})

def calcDistance(request):
    return render(request, "distance-calculator.html", {'google_key': settings.GOOGLE_API_KEY})
def recoverPassword(request):
    email = request.POST.get('txtEmail')
    resetCode = request.POST.get('txtResetCode') 
    newPassword = request.POST.get('txtNewPassword')
    confirmPassword = request.POST.get('txtConfirmNewPassword') 

    #Validation  
    validateMsg = validate(email=email, password=newPassword, confirmPassword=confirmPassword,resetCode=resetCode)    
    if validateMsg != "OK": 
        return render(request, 'recover-password.html', {'message_error2' : validateMsg}) 

    #check user exist
    user = User.objects.filter(email=email)
    if user.count() == 0:
        message_error = "Email Not Exists"
        return render(request, 'recover-password.html', {'message_error2': message_error})
    user = user[0]
 
    if user.passwordResetCode != resetCode:
        message_error = "Wrong Reset Code"
        return render(request, 'recover-password.html', {'message_error2': message_error})

    user.password = newPassword
    user.passwordResetCode = None
    user.passwordResetCodeTime = None
    user.save()
    message_success = 'Password Changed Successfully'
    return render(request, 'recover-password.html', {'message_success2': message_success})
def changeName(request):
    email = request.session.get("useremail") 
    newName = request.POST.get("txtName")
    data = {'error_message': ''} 
    user = User.objects.filter(email = email)
    user=user[0]
    user.name=newName
    user.save()
    return JsonResponse(data)
def changePassword(request):
    email = request.session.get("useremail") 
    password = request.POST.get("txtPassword")
    newPassword = request.POST.get("txtNewPassword")
    confirmPassword = request.POST.get("txtConfirmPassword")
    data = {'message_error': ''} 
    validateMsg = validate(password=newPassword, confirmPassword=confirmPassword)
    if validateMsg != 'OK':
        data['message_error'] = "Retype New Password And Confirm New Password"
        return JsonResponse(data)
    user = User.objects.filter(email = email)
    user=user[0]
    if user.password != password:
        data['message_error'] = "Current Password Not Correct"
        return JsonResponse(data)

    user.password=newPassword
    user.save()
    return JsonResponse(data)
def profilePage(request):
    username = request.session.get("username") 
    useremail = request.session.get("useremail") 
    if username and useremail:
        return render(request, 'profile.html', {'username': username, 'useremail': useremail})
    return render(request, 'index.html', {'message_error': 'You Must Login'})
def uploadFilePage(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
    #    if form.is_valid():
        print ('hereeeeeeeee again')
        handle_uploaded_file(request.FILES.get('file'))
            
        return HttpResponseRedirect('/login_system/uploadFilePage')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
def logout(request):
    try:
        del request.session['username']
        del request.session['useremail']
    except KeyError:
        pass
    return render(request, "index.html")   

def serverAndBrowserInfo(request): 
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    return render(request,"server-and-browser-info.html",{
        "Machine" : platform.machine(),
        "Processor" : platform.processor(),
        "Platform" : platform.platform(),
        "browserFamily": user_agent.browser.family,
        "browserVersion": user_agent.browser.version_string,
    })
def isValidEmail(email):
    isValid = True
    if not email :
        isValid = False  
    return isValid
def isValidPassword(password):
    isValid = True
    if not password :
        isValid = False
    return isValid
def isValidConfrimPassword(password, confirmPassword):
    isValid = True
    if not confirmPassword:
        isValid = False
    if confirmPassword != password:
        isValid = False

    return isValid
def isValidResetCode(resetCode):
    isValid = True
    if not resetCode :
        isValid = False
    return isValid
def validate(email=False, password=False, confirmPassword=False, resetCode=False, oldPassword=False):
    isValid = True
    resultMsg = ""   
    if email != False: 
        if not isValidEmail(email):
            resultMsg += "Not Valid Email - "
            isValid = False

    if password != False: 
        if not isValidPassword(password):
            isValid = False
            resultMsg += "Not Valid Password - "  

    if oldPassword != False: 
        if not isValidPassword(oldPassword):
            isValid = False 
            resultMsg += "Not Valid Old Password - "   
    if confirmPassword != False: 
        if not isValidConfrimPassword(password, confirmPassword):
            isValid = False
            resultMsg += "Not Valid Confirm Password - "

    if resetCode != False: 
        if not isValidResetCode(resetCode):
            isValid = False
            resultMsg += "Not Valid Reset Code - "

    if isValid:
        resultMsg = "OK"
    return resultMsg
def handle_uploaded_file(f):
    if not os.path.exists('uploads/'):
        os.mkdir('uploads/')
    with open('uploads/', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def sendCode(email, code):
    try:
        mailserver = mail.SMTP("smtp.gmail.com")
        mailserver.starttls()
        senderEmail = settings.EMAIL_ADDRESS
        senderPassword = settings.EMAIL_PASSWORD
        mailserver.login(senderEmail, senderPassword)
        msgBody = "Your Password Reset Code : %s"% code
        msg = """From: %s\nTo: %s\nSubject: Password Reset Code \n
                %s""" % (senderEmail, email,msgBody )
        mailserver.sendmail(senderEmail, email, msg)
        return True
    except Exception:
        return False