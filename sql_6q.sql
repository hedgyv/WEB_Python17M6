SELECT 
    g.name AS group_name,
    string_agg(s.fullname, ', ') AS students_list
FROM 
    students s
JOIN 
    groups g ON s.group_id = g.id
where g.id = 1
GROUP BY 
    g.name;