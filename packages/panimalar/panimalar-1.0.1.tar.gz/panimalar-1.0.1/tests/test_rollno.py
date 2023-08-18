import unittest

from src.rollno import isvalid, parse, get_dept_code, get_dept

class TestParse(unittest.TestCase):

    # ------------------------------------------------------

    # Valid rollno

    # ------------------------------------------------------


    def test_correct_rollno(self):
        self.assertTrue(isvalid('2021PECCB901'))
        self.assertTrue(isvalid('2021PECCB012'))
        self.assertTrue(isvalid('2021PECCB123'))
        self.assertTrue(isvalid('2021PECCB234'))
        self.assertTrue(isvalid('2021PECCB345'))
        self.assertTrue(isvalid('2021PECCB456'))
        self.assertTrue(isvalid('2021PECCB567'))
        self.assertTrue(isvalid('2021PECCB678'))
        self.assertTrue(isvalid('2021PECCB789'))
        self.assertTrue(isvalid('2021PECCB890'))

    def test_correct_dept(self):
        self.assertTrue(isvalid('2021PECCB000'))
        self.assertTrue(isvalid('2021PECCS000'))
        self.assertTrue(isvalid('2021PECIT000'))
        self.assertTrue(isvalid('2021PECEC000'))
        self.assertTrue(isvalid('2021PECEE000'))
        self.assertTrue(isvalid('2021PECCE000'))
        self.assertTrue(isvalid('2021PECME000'))
        self.assertTrue(isvalid('2021PECAD000'))
        self.assertTrue(isvalid('2021PECCC000'))

    def test_correct_year(self):
        self.assertTrue(isvalid('2018PECCB000'))
        self.assertTrue(isvalid('2019PECCB000'))
        self.assertTrue(isvalid('2020PECCB000'))
        self.assertTrue(isvalid('2021PECCB000'))
        self.assertTrue(isvalid('2022PECCB000'))
        self.assertTrue(isvalid('2023PECCB000'))
        self.assertTrue(isvalid('2024PECCB000'))
        self.assertTrue(isvalid('2025PECCB000'))
        self.assertTrue(isvalid('2026PECCB000'))
        self.assertTrue(isvalid('2027PECCB000'))
        self.assertTrue(isvalid('2028PECCB000'))
        self.assertTrue(isvalid('2029PECCB000'))
        self.assertTrue(isvalid('2030PECCB000'))

    def test_lettercase(self):
        self.assertTrue(isvalid('2021peccb000'))
        self.assertTrue(isvalid('2021PECCB000'))
        self.assertTrue(isvalid('2021PeCcB000'))
        self.assertTrue(isvalid('2021pEcCb000'))

    def test_inisvalid_rollno(self):
        self.assertFalse(isvalid('2021PECCB00'))
        self.assertFalse(isvalid('2021PECCB0000'))
        self.assertFalse(isvalid('2021PECCB00000'))
        self.assertFalse(isvalid('2021PECCB000000'))
        self.assertFalse(isvalid('2021PECCB0000000'))
        self.assertFalse(isvalid('2021PECCBXXX'))
        self.assertFalse(isvalid('2021PECCB000X'))
        self.assertFalse(isvalid('2021PECB00X0'))
        self.assertFalse(isvalid('2021PECB00X0'))
    
    def test_inisvalid_dept(self):
        self.assertFalse(isvalid('2021PEC11000'))
        self.assertFalse(isvalid('2021PEC22000'))
        self.assertFalse(isvalid('2021PEC33000'))
        self.assertFalse(isvalid('2021PEC44000'))
        self.assertFalse(isvalid('2021PEC55000'))
        self.assertFalse(isvalid('2021PEC66000'))
        self.assertFalse(isvalid('2021PEC000'))
        self.assertFalse(isvalid('2021PEC0B000'))
        self.assertFalse(isvalid('2021PEC1B000'))
        self.assertFalse(isvalid('2021PEC2B000'))
        self.assertFalse(isvalid('2021PEC3B000'))
        self.assertFalse(isvalid('2021PEC4B000'))
        self.assertFalse(isvalid('2021PEC5B000'))
        self.assertFalse(isvalid('2021PEC6B000'))
        self.assertFalse(isvalid('2021PEC7B000'))
        self.assertFalse(isvalid('2021PEC8B000'))
        self.assertFalse(isvalid('2021PEC9B000'))

    def test_inisvalid_year(self):
        self.assertFalse(isvalid('2007PECCB000'))
        self.assertFalse(isvalid('2008PECCB000'))
        self.assertFalse(isvalid('2009PECCB000'))
        self.assertFalse(isvalid('2000PECCB000'))
        self.assertFalse(isvalid('1000PECCB000'))
        self.assertFalse(isvalid('0000PECCB000'))
        self.assertFalse(isvalid('0009PECCB000'))
        self.assertFalse(isvalid('9900PECCB000'))
        self.assertFalse(isvalid('9999PECCB000'))

    def test_pec(self):
        self.assertFalse(isvalid('2021PITCB000'))
        self.assertFalse(isvalid('2021PITCB000'))
        self.assertFalse(isvalid('2021PCECB000'))
        self.assertFalse(isvalid('2021BECCB000'))
        self.assertFalse(isvalid('2021EPCCB000'))
        self.assertFalse(isvalid('2021MECCB000'))
        self.assertFalse(isvalid('2021CECCB000'))
        self.assertFalse(isvalid('2021EECCB000'))
        self.assertFalse(isvalid('2021PEXCB000'))
        
        
    # ------------------------------------------------------

    # Parse

    # ------------------------------------------------------

    def test_year(self):
        self.assertEqual(parse('2021PECCB000', 'year'), '2021')
        self.assertEqual(parse('2020PECCB000', 'year'), '2020')
        self.assertEqual(parse('2019PECCB000', 'year'), '2019')
        self.assertEqual(parse('2018PECCB000', 'year'), '2018')

    def test_dept(self):
        self.assertEqual(parse('2021PECCB000', 'department_code'), 'CB')
        self.assertEqual(parse('2021PECCS000', 'department_code'), 'CS')
        self.assertEqual(parse('2021PECEC000', 'department_code'), 'EC')
        self.assertEqual(parse('2021PECME000', 'department_code'), 'ME')
        self.assertEqual(parse('2021PECCE000', 'department_code'), 'CE')
        self.assertEqual(parse('2021PECIT000', 'department_code'), 'IT')
        self.assertEqual(parse('2021PECEE000', 'department_code'), 'EE')

    def test_shortrollno(self):
        self.assertEqual(parse('2021PECCB000', 'shortrollno'), '000')
        self.assertEqual(parse('2021PECCB001', 'shortrollno'), '001')
        self.assertEqual(parse('2021PECCB010', 'shortrollno'), '010')
        self.assertEqual(parse('2021PECCB100', 'shortrollno'), '100')
        self.assertEqual(parse('2021PECCB999', 'shortrollno'), '999')

    def test_invalid(self):
        self.assertEqual(parse('2021PECCB000', 'invalid'), None)
        self.assertEqual(parse('2021PECCB00', 'year'), None)
        self.assertEqual(parse('2021PECCB0000', 'year'), None)
        self.assertEqual(parse('2021PECB000', 'dept'), None)
        self.assertEqual(parse('2021PECCB00X', 'shortrollno'), None)
        self.assertEqual(parse('2021PECCB000', 'rollno'), None)

    # ------------------------------------------------------

    # Get Department

    # ------------------------------------------------------


    def test_get_dept(self):
        self.assertEqual(get_dept('2021PECCB000'), 'Computer Science and Business Systems')
        self.assertEqual(get_dept('2021PECCS000'), 'Computer Science and Engineering')
        self.assertEqual(get_dept('2021PECIT000'), 'Information Technology')
        self.assertEqual(get_dept('2021PECEC000'), 'Electronics and Communication Engineering')
        self.assertEqual(get_dept('2021PECEE000'), 'Electrical and Electronics Engineering')
        self.assertEqual(get_dept('2021PECME000'), 'Mechanical Engineering')
        self.assertEqual(get_dept('2021PECCE000'), 'Civil Engineering')
        self.assertEqual(get_dept('2021PECCC000'), 'Computer and Communication Engineering')
        self.assertEqual(get_dept('2021PECME000'), 'Mechanical Engineering')
        self.assertEqual(get_dept('2021PECAD000'), 'Artificial Intelligence and Data Science')

    def test_get_dept_invalid(self):
        self.assertEqual(get_dept('2021PECCB00'), None)
        self.assertEqual(get_dept('2021PECCB0000'), None)
        self.assertEqual(get_dept('2021PECB0B0'), None)
        self.assertEqual(get_dept('2021PITB000'), None)
        self.assertEqual(get_dept('2021PITCB00X'), None)
        self.assertEqual(get_dept('2021PECCB0T0'), None)

    # ------------------------------------------------------

    # Get Dept Code

    # ------------------------------------------------------
    def test_get_dept_code(self):
        self.assertEqual(get_dept_code('2021PECCB000'), 'CB')
        self.assertEqual(get_dept_code('2021PECCS000'), 'CS')
        self.assertEqual(get_dept_code('2021PECIT000'), 'IT')
        self.assertEqual(get_dept_code('2021PECEC000'), 'EC')
        self.assertEqual(get_dept_code('2021PECEE000'), 'EE')
        self.assertEqual(get_dept_code('2021PECME000'), 'ME')
        self.assertEqual(get_dept_code('2021PECCE000'), 'CE')
        self.assertEqual(get_dept_code('2021PECCC000'), 'CC')
        self.assertEqual(get_dept_code('2021PECAD000'), 'AD')

    def test_get_dept_code_invalid(self):
        self.assertEqual(get_dept_code('2021PECCB00'), None)
        self.assertEqual(get_dept_code('2021PECCB0000'), None)
        self.assertEqual(get_dept_code('2021PECB0B0'), None)
        self.assertEqual(get_dept_code('2021PITB000'), None)
        self.assertEqual(get_dept_code('2021PITCB00X'), None)
        self.assertEqual(get_dept_code('2021PECCB0T0'), None)
        



        
if __name__ == '__main__':
    unittest.main()
