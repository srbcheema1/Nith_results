from util.limits import base_year

def get_year(roll):
    roll = str(roll)
    if(roll[0]=='i'):#iitu
        year = roll[5:7]
    else:
        year = roll[0:2]
    return year


def get_college(roll):
    roll = str(roll)
    if(roll[0]=='i'):#iitu
        college = "iiitu"
    else:
        college = "nith"
    return college


def get_c_id(roll):
    roll = str(roll)
    if(roll[0]=='i'):#iitu
        c_id="iiituna"
    else:
        c_id="scheme"
    return c_id


def get_num(roll):
    roll = str(roll)
    if(roll[2]=='m' or roll[2]=='M'):
        num=roll[5:7]
    elif(roll[0]=='i'):
        num=roll[8:10]
    else:
        num=roll[3:5]
    return num


def get_branch(roll):
    roll = str(roll)
    if(roll[2]=='m' or roll[2]=='M'):
        branch=roll[2:4].lower()
        branch+=str(roll[4])
    elif(roll[0]=='i'):
        branch='una'+roll[7]
    else:
        branch=roll[2]
    return branch


def get_branch_name(branch):
    branch_data = {
            "1":"Civil",
            "2":"Electrical",
            "3":"Mechanical",
            "4":"Ece",
            "5":"Cse",
            "6":"Architecture",
            "7":"Chemical",
            "8":"Material",
            "mi5":"Cse_dual",
            "mi4":"Ece_dual",
            "una1":"Cse_una",
            "una2":"Ece_una",
            "una3":"IT_una",
            "0":"unknown"
    }
    if(branch in branch_data):
        return branch_data[branch]
    else:
        return branch_data['0']


def get_curr_year(roll):
    year = get_year(roll)
    curr_year = base_year - int(year) + 1
    return str(curr_year)
