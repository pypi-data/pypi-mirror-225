import regex


# Regex for rollno
regex_rollno = r'^(20[1-3]{1}[0-9]{1})(PEC)([A-Z]{2})([0-9]{3})$'

def isvalid(rollno):
    """
    Check if rollno is valid (eg. 2021PECCB001)
    Returns True if valid, False otherwise
    """

    

    # Check if rollno is valid
    if regex.match(regex_rollno, rollno.strip().upper()):
        return True
    else:
        return False


def parse(rollno, required):

    """
    Parse rollno
    Returns parsed rollno if valid, None otherwise
    Required = year, college_code, department_code, shortrollno
    """


    # Check if rollno is valid
    if isvalid(rollno):

        # Match regex
        re = regex.match(regex_rollno, rollno.strip().upper())

    
        # Return required
        if required == 'year':
            # Get year
            year = re.group(1)
            return year
        
        elif required == 'college_code':
            # Get college code
            college_code = re.group(2)
            return college_code
        
        elif required == 'department_code':
            # Get department code
            department_code = re.group(3)
            return department_code
        
        elif required == 'shortrollno':
            # Get shortrollno
            shortrollno = re.group(4)
            return shortrollno
        
        else:
            return None
    else:
        return None


def get_dept_code(rollno):
    """
    Get department code from rollno
    Returns department code if valid, None otherwise
    """

    # Check if rollno is valid
    if isvalid(rollno):

        # Get department code
        department_code = parse(rollno, 'department_code')

        return department_code
    else:
        return None


def get_dept(rollno):
    """
    Get department from rollno
    Returns department name if valid, None otherwise
    """

    # Check if rollno is valid
    if isvalid(rollno):
        departments = {
            'CB': 'Computer Science and Business Systems',
            'CS': 'Computer Science and Engineering',
            'IT': 'Information Technology',
            'EC': 'Electronics and Communication Engineering',
            'EE': 'Electrical and Electronics Engineering',
            'CE': 'Civil Engineering',
            'CC': 'Computer and Communication Engineering',
            'ME': 'Mechanical Engineering',
            'AD': 'Artificial Intelligence and Data Science'
        }

        # Get department code
        department_code = parse(rollno, 'department_code')


        # Get department name and return
        try:
            department=  departments[department_code]
        except KeyError:
            return None
        
        return department
    else:
        return None
    
    
def get_year(rollno):
    """
    Get year from rollno
    Returns year if valid, None otherwise
    """

    # Check if rollno is valid
    if isvalid(rollno):

        # Get year
        year = parse(rollno, 'year')

        return year
    else:
        return None