SELECT 
    t.fullname AS teacher_name,
    string_agg(s.name, ', ') AS courses_taught
FROM 
    teachers t
JOIN 
    subjects s ON t.id = s.teacher_id
where t.id = 1
GROUP BY 
    t.fullname;

