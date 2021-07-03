"""
Testing

"""

import psycopg2
import random

def DataUpdate(userid,age,intent):
    mydb =  psycopg2.connect(user='admin', password='kK0sk0NxoiiDaO4', host='db', port= '5432', database='RASA_Covid') 
    mycursor = mydb.cursor() 
    #sql = 'CREATE TABLE covid_user_data (userid VARCHAR(255), age int, intent VARCHAR(255), FirstDose VARCHAR(255), BothDose VARCHAR(255), NoDose VARCHAR(255), Vaccine VARCHAR(255), Gender VARCHAR(255), Region_Access VARCHAR(255), Region_Cases VARCHAR(255), Feedback1 VARCHAR(255), Feedback2 VARCHAR(255), Feedback3 VARCHAR(255), Feedback4 VARCHAR(255));'
    sql='INSERT INTO covid_user_data (userid, age, intent) VALUES ("{0}",{1}, "{2}");'.format(userid,age, intent) 
    mycursor.execute(sql) 
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

def Select_Age(userid):
    print('userid is: ', userid)
    mydb =  psycopg2.connect(user='admin', password='kK0sk0NxoiiDaO4', host='db', port= '5432', database='RASA_Covid') 
    mycursor = mydb.cursor()
    sql = """select age from covid_user_data where userid='{0}';""".format(userid)
    mycursor.execute(sql) 
    rows = mycursor.fetchall()
    if len(list(rows)) < 1:
        return[("There are no resources matching your query.")]
    else:
        return[rows[0]]

def Select_Gender(userid):
    print('userid is: ', userid)
    mydb =  psycopg2.connect(user='admin', password='kK0sk0NxoiiDaO4', host='db', port= '5432', database='RASA_Covid') 
    mycursor = mydb.cursor()
    sql = """select Gender from covid_user_data where userid='{0}';""".format(userid)
    mycursor.execute(sql) 
    rows = mycursor.fetchall()
    if len(list(rows)) < 1:
        return[("There are no resources matching your query.")]
    else:
        print(f'Gender from database is: {rows[0]}')
        return[rows[0]]

def Update_Gender(userid, gender):
    print('userid is: ', userid)
    mydb =  psycopg2.connect(user='admin', password='kK0sk0NxoiiDaO4', host='db', port= '5432', database='RASA_Covid') 
    mycursor = mydb.cursor()
    sql = """update covid_user_data 
                set Gender = '{0}'  where userid = '{1}';""".format(gender, userid) 
    mycursor.execute(sql)  
    mydb.commit()
    print("record updated") 

def Update_first_dose_info(userid):
    print('userid is: ', userid)
    mydb =  psycopg2.connect(user='admin', password='kK0sk0NxoiiDaO4', host='db', port= '5432', database='RASA_Covid') 
    mycursor = mydb.cursor()
    sql = """update covid_user_data 
                set FirstDose = "Yes" where userid = '{0}';""".format(userid) 
    mycursor.execute(sql)  
    mydb.commit()
    print("record updated")           

def Update_both_dose_info(userid):
    print('userid is: ', userid)
    mydb =  psycopg2.connect(user='admin', password='kK0sk0NxoiiDaO4', host='db', port= '5432', database='RASA_Covid') 
    mycursor = mydb.cursor()
    sql = """update covid_user_data 
                set BothDose= "Yes" where userid = '{0}';""".format(userid) 
    mycursor.execute(sql) 
    mydb.commit()
    print("record updated")

def Update_no_dose_info(userid):
    print('userid is: ', userid)
    mydb =  psycopg2.connect(user='admin', password='kK0sk0NxoiiDaO4', host='db', port= '5432', database='RASA_Covid') 
    mycursor = mydb.cursor()
    sql = """update covid_user_data 
                set NoDose= "Yes" where userid = '{0}';""".format(userid) 
    mycursor.execute(sql) 
    mydb.commit()
    print("record updated")

def Select_First_Dose(userid):
    print('userid is: ', userid)
    mydb =  psycopg2.connect(user='admin', password='kK0sk0NxoiiDaO4', host='db', port= '5432', database='RASA_Covid') 
    mycursor = mydb.cursor()
    sql = """select FirstDose from covid_user_data where userid= '{0}';""".format(userid)
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    if len(list(rows)) < 1:
        return[("There are no resources matching your query.")]
    else:
        return[rows[0]]

def Select_Both_Dose(userid):
    print('userid is: ', userid)
    mydb =  psycopg2.connect(user='admin', password='kK0sk0NxoiiDaO4', host='db', port= '5432', database='RASA_Covid') 
    mycursor = mydb.cursor()
    sql = """select BothDose from covid_user_data where userid = '{0}';""".format(userid)
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    if len(list(rows)) < 1:
        return[("There are no resources matching your query.")]
    else:
        return[rows[0]]

def Select_No_Dose(userid):
    print('userid is: ', userid)
    mydb =  psycopg2.connect(user='admin', password='kK0sk0NxoiiDaO4', host='db', port= '5432', database='RASA_Covid') 
    mycursor = mydb.cursor()
    sql = """select NoDose from covid_user_data where userid = '{0}';""".format(userid)
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    if len(list(rows)) < 1:
        return[("There are no resources matching your query.")]
    else:
        return[rows[0]]

def Update_vaccine_info(userid, vaccine_name):
    print('userid is: ', userid)
    print('vaccine_name is: ', vaccine_name)
    mydb =  psycopg2.connect(user='admin', password='kK0sk0NxoiiDaO4', host='db', port= '5432', database='RASA_Covid') 
    mycursor = mydb.cursor()
    sql = """update covid_user_data 
                set Vaccine = '{0}' where userid = '{1}';""".format(vaccine_name,userid) 
    mycursor.execute(sql) 
    mydb.commit()

def Update_region_info_Access(userid, regions):
    print('userid is: ', userid)
    print('Region is: ', regions)
    mydb =  psycopg2.connect(user='admin', password='kK0sk0NxoiiDaO4', host='db', port= '5432', database='RASA_Covid')
    mycursor = mydb.cursor()
    sql = """update covid_user_data 
                set Region_Access = '{0}' where userid = '{1}';""".format(regions,userid)
    mycursor.execute(sql)
    mydb.commit()

def Update_region_info_Cases(userid, regions):
    print('userid is: ', userid)
    print('Region is: ', regions)
    mydb =  psycopg2.connect(user='admin', password='kK0sk0NxoiiDaO4', host='db', port= '5432', database='RASA_Covid')
    mycursor = mydb.cursor()
    sql = """update covid_user_data 
                set Region_Cases = '{0}' where userid = '{1}';""".format(regions,userid)
    mycursor.execute(sql)
    mydb.commit()

def Update_Feedback_info1(userid, feedback):
    print('userid is: ', userid)
    print('feedback is: ', feedback)
    mydb =  psycopg2.connect(user='admin', password='kK0sk0NxoiiDaO4', host='db', port= '5432', database='RASA_Covid') 
    mycursor = mydb.cursor()
    sql = """update covid_user_data 
                set Feedback1 = '{0}' where userid = '{1}';""".format(feedback, userid) 
    mycursor.execute(sql) 
    mydb.commit()
def Update_Feedback_info2(userid, feedback):
    mydb =  psycopg2.connect(user='admin', password='kK0sk0NxoiiDaO4', host='db', port= '5432', database='RASA_Covid') 
    mycursor = mydb.cursor()
    sql = """update covid_user_data 
                set Feedback2 = '{0}' where userid = '{1}';""".format(feedback, userid) 
    mycursor.execute(sql) 
    mydb.commit()
def Update_Feedback_info3(userid, feedback):
    mydb =  psycopg2.connect(user='admin', password='kK0sk0NxoiiDaO4', host='db', port= '5432', database='RASA_Covid') 
    mycursor = mydb.cursor()
    sql = """update covid_user_data 
                set Feedback3 = '{0}' where userid = '{1}';""".format(feedback, userid) 
    mycursor.execute(sql) 
    mydb.commit()
def Update_Feedback_info4(userid, feedback):
    mydb =  psycopg2.connect(user='admin', password='kK0sk0NxoiiDaO4', host='db', port= '5432', database='RASA_Covid') 
    mycursor = mydb.cursor()
    sql = """update covid_user_data 
                set Feedback4 = '{0}' where userid = '{1}';""".format(feedback, userid) 
    mycursor.execute(sql) 
    mydb.commit()
