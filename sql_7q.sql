SELECT 
    s.fullname AS student_name,
    g.name AS group_name,
    sub.name AS subject_name,
    STRING_AGG(CAST(gr.grade AS TEXT), ', ') AS student_grades
FROM 
    students s
JOIN 
    groups g ON s.group_id = g.id
JOIN 
    grades gr ON s.id = gr.student_id
JOIN 
    subjects sub ON gr.subject_id = sub.id
where sub.id = 1
GROUP BY 
    s.fullname, g.name, sub.name;

