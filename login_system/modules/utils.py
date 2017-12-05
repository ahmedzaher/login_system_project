def isValidEmail(email):
    isValid = True

    if email == "":
        isValid = False

    if email == None:
        isValid = False
    
    return isValid

def isValidPassword(password):
    isValid = True
    if password == "":
        isValid = False

    if password == None:
        isValid = False

    return isValid

def isValidConfrimPassword(password, confirmPassword):
    isValid = True
    if confirmPassword == "":
        isValid = False

    if confirmPassword == None:
        isValid = False

    if confirmPassword != password:
        isValid = False

    return isValid

def isValidResetCode(resetCode):
    isValid = True
    if resetCode == "":
        isValid = False

    if resetCode == None:
        isValid = False
 

    return isValid
