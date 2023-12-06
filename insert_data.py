from connection import create_connection
import logging
from faker import Faker
from random import randint
from psycopg2 import DatabaseError

fake = Faker()

amount_of_students = randint(30,50)
amount_of_groups = 3
amount_of_subjects = randint(5,8)
amount_of_teachers = randint(3,5)
amount_students_in_each_group = int(amount_of_students/amount_of_groups)

if __name__ == '__main__':
    insert_groups_data = """INSERT INTO groups (name) VALUES (%s)"""
    insert_students_data = """INSERT INTO students (fullname, group_id) VALUES(%s, %s) RETURNING id"""
    insert_st_grades = """INSERT INTO grades (student_id, subject_id, grade, grade_date) VALUES(%s, %s, %s, %s)"""
    insert_teachers_data = """INSERT INTO teachers (fullname) VALUES(%s)"""
    insert_subjects_data = """INSERT INTO subjects (name, teacher_id) VALUES(%s, %s)"""
    
    with create_connection() as conn:
        if conn is not None:
            cur = conn.cursor()
            
            #adding groups
            for _ in range(amount_of_groups):
                cur.execute(insert_groups_data, (fake.word(),))
                
            # adding teachers
            for _ in range(amount_of_teachers):
                cur.execute(insert_teachers_data, (fake.name(),))

            #adding subject
            for teacher_id in range(1, amount_of_teachers):
                for _ in range(2):
                    cur.execute(insert_subjects_data, (fake.word(), teacher_id))
                
            #adding student and grades
            for group_id in range(1,amount_of_groups + 1):
                for _ in range(amount_students_in_each_group):
                    cur.execute(insert_students_data, (fake.name(), group_id))
                    student_id = cur.fetchone()[0]
                    for subject_id in range(1, amount_of_subjects+1):
                        for _ in range(amount_of_groups):
                            cur.execute(insert_st_grades, (student_id, subject_id, randint(0, 100), fake.date_this_decade()))
                
        try:
            # Збереження змін
            conn.commit()
        except DatabaseError as e:
            logging.error(e)
            conn.rollback()
        # finally:
        #     # Закриття підключення
        #     cur.close()
        #     conn.close()    