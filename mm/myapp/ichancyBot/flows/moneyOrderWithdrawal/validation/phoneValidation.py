

def phoneValidation(phone_number:str):
    if len(phone_number) != 10 or not (phone_number[1:len(phone_number)].isdigit() and phone_number[0] == "0"):
         # print(phone_number !=10)
         # print(phone_number[1:len(phone_number)])
         # print(phone_number[0]==0)
         return False
    # print(phone_number !=10)
    # print(phone_number[1:len(phone_number)])
    # print(phone_number[0]=="0")
    return True
    