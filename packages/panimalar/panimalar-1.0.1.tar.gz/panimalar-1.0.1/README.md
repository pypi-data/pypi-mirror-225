# Panimalar

A package for students of Panimalar Engineering College.

## Table of Contents
- [Modules](#modules)
  - [rollno](#rollno)
  - [cgpa](#cgpa)
- [Details](#details)
- [Usage](#usage)
- [Release Steps](#release-steps)

## Modules

The Panimalar package consists of the following modules:

### rollno

This module provides functions to work with Panimalar Engineering College roll numbers.

- `isvalid(rollno) => boolean`: Checks if a roll number is valid.
- `get_dept_code(rollno) => string`: Retrieves the department code from a roll number.
- `get_dept(rollno) => string`: Retrieves the department name from a roll number.
- `parse(rollno, required) => string (or) int`: Parses specific details from a roll number based on the requirements.
- `get_year(rollno) => int`: Retrieves the year of joining from a roll number.

### cgpa

This module handles CGPA calculations for students.

#### Classes and Methods

##### Subject

This class stores the credit and grade point of a subject.

Properties:
- `credit`: The credit value of the subject.
- `grade point`: The grade point obtained in the subject.

##### Gpa

This class calculates the GPA (Grade Point Average) based on the subjects.

Methods:
- `addsubject(self, credit: int, grade_point: int)`: Adds a subject with its credit and grade point to the GPA calculation.
- `calc(self) -> float`: Calculates and returns the GPA value.
- `display(self) -> None`: Displays the subjects and their credit points along with the calculated GPA.
- `added(self) -> None`: Notifies that a subject has been added to the GPA calculation.
- `removesubject(self, index: int) -> None`: Removes a subject from the GPA calculation based on its index.

##### Cgpa

This class calculates the CGPA (Cumulative Grade Point Average) based on the GPAs of multiple semesters.

Methods:
- `calc(self)`: Calculates and returns the CGPA value.
- `display(self) -> None`: Displays the semesters and their corresponding GPAs along with the calculated CGPA.
- `added(self) -> None`: Notifies that a semester has been added to the CGPA calculation.
- `removesemester(self, index: int) -> None`: Removes a semester from the CGPA calculation based on its index.

## Details

- **Validate Roll Number**: The `isvalid(rollno)` function can be used to validate whether a given roll number is in the correct format.
- **Parse Details from Roll Number**: The `parse(rollno, required)` function allows extracting specific details from a roll number based on the requirements.

A valid Panimalar roll number follows the format: (YEAROFJOIN)YYYY-PEC-(DEPT)DD-(ROLLNO)XXXX

Example: 2021PECCB101

- 2021: Year of Joining
- PEC: Panimalar Engineering College
- CB: Department (Computer Science and Business Systems)
- 101: Roll Number of Student

## Usage

1. Install the package using pip:
   `pip install panimalar`
2. Import the desired modules and classes into your Python script:
`from panimalar.rollno import isvalid, get_dept_code, parse
from panimalar.cgpa import Gpa, Cgpa`
3. Use the functions and classes according to your requirements. Here's an example:

```
roll_number = "2021PECCB101"
if isvalid(roll_number):
    dept_code = get_dept_code(roll_number)
    print(f"Department code: {dept_code}")

    year_of_joining = parse(roll_number, "YEAROFJOIN")
    print(f"Year of Joining: {year_of_joining}")
```

## Release Steps
To release a new version of the package, follow these steps:

1. Update the version number in pyproject.toml to reflect any major changes, updates, or bug fixes.
2. Add any new modules or functions to the pyproject.toml file.
3. Include any necessary dependencies in the pyproject.toml file.
4. Document the new functions or changes in the README.



