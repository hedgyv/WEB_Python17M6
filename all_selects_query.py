from connection import create_connection
import logging
from psycopg2 import DatabaseError 


if __name__ == '__main__':
    sql_expression_01 = """
        SELECT s.id, s.fullname, ROUND(AVG(g.grade), 2) AS average_grade
        FROM students s
        JOIN grades g ON s.id = g.student_id
        GROUP BY s.id
        ORDER BY average_grade DESC
        LIMIT 5;
        """
    sql_expression_02 = """
        SELECT s.id, s.fullname, ROUND(AVG(g.grade), 2) AS average_grade
        FROM grades g
        JOIN students s ON s.id = g.student_id
        WHERE g.subject_id = 1
        GROUP BY s.id
        ORDER BY average_grade DESC
        LIMIT 1;
        """
    sql_expression_03 = """
        SELECT s.group_id, ROUND(AVG(g.grade), 2) AS average_grade
        FROM students s
        JOIN grades g ON s.id = g.student_id
        WHERE g.subject_id = 1
        GROUP BY s.group_id
        ORDER BY average_grade DESC;
        """
    sql_expression_04 = """
        SELECT ROUND(AVG(grade), 2) AS average_grade
        FROM grades;
        """
    sql_expression_05 = """
        SELECT t.fullname AS teacher_name, string_agg(s.name, ', ') AS courses_taught
        FROM teachers t
        JOIN subjects s ON t.id = s.teacher_id
        where t.id = 1
        GROUP BY t.fullname;
        """
    sql_expression_06 = """
        SELECT g.name AS group_name, string_agg(s.fullname, ', ') AS students_list
        FROM students s
        JOIN groups g ON s.group_id = g.id
        where g.id = 1
        GROUP BY g.name;
        """
    sql_expression_07 = """
        SELECT s.fullname AS student_name, g.name AS group_name,
        sub.name AS subject_name,
        STRING_AGG(CAST(gr.grade AS TEXT), ', ') AS student_grades
        FROM students s
        JOIN groups g ON s.group_id = g.id
        JOIN grades gr ON s.id = gr.student_id
        JOIN subjects sub ON gr.subject_id = sub.id
        where sub.id = 1
        GROUP BY s.fullname, g.name, sub.name;
        """
    sql_expression_08 = """
        SELECT s.id, s.fullname, ROUND(AVG(m.grade), 2) AS average_grade
        FROM teachers s
        JOIN subjects subj ON subj.teacher_id = s.id
        JOIN grades m ON s.id = m.subject_id
        WHERE s.id = 1
        GROUP BY s.id;
        """
    sql_expression_09 = """
        SELECT DISTINCT s.id, s.fullname, subj.id , subj.name
        FROM students s
        JOIN grades m ON s.id = m.student_id
        JOIN subjects subj ON m.subject_id = subj.id
        WHERE s.id = 1;
        """
    sql_expression_10 = """
        SELECT DISTINCT s.id, s.fullname, subj.id , subj.name, t.id, t.fullname
        FROM students s
        JOIN grades m ON s.id = m.student_id
        JOIN subjects subj ON m.subject_id = subj.id
        JOIN teachers t ON subj.teacher_id = t.id
        WHERE s.id = 1 AND t.id = 1;
        """
    sql_expression_11 = """
        SELECT s.id, s.fullname, t.id, t.fullname, ROUND(AVG(m.grade), 2) AS average_grade 
        FROM teachers t
        JOIN subjects subj ON t.id = subj.teacher_id
        JOIN grades m ON subj.id = m.subject_id
        JOIN students s ON m.student_id = s.id
        WHERE s.id = 1 AND t.id = 1
        GROUP BY s.id, t.id, s.fullname, t.fullname;
        """
    sql_expression_12 = """
        SELECT s.id, s.fullname, MAX(m.grade_date) AS max_date
        FROM students s
        JOIN grades m ON s.id = m.student_id
        JOIN subjects subj ON m.subject_id = subj.id
        JOIN groups g ON s.group_id = g.id
        WHERE g.id = 1 AND subj.id = 1 
        GROUP BY s.id, s.fullname
        ORDER BY s.id, max_date DESC;
        """
    
    
    try:
        with create_connection() as conn:
            if conn is not None:
                c = conn.cursor()
                try:
                    c.execute(sql_expression_01)
                    print(c.fetchall())
                    c.execute(sql_expression_02)
                    result = c.fetchall()
                    print(result)
                except DatabaseError as e:
                    logging.error(e)
                finally:
                    c.close()
            else:
                print("Error! cannot create the database connection.")
    except RuntimeError as err:
        logging.error(err)
 
