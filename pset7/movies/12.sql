SELECT title
FROM movies JOIN stars ON id = movie_id
WHERE person_id IN (SELECT id FROM people WHERE name = 'Johnny Depp')
INTERSECT
SELECT title
FROM movies JOIN stars ON id = movie_id
WHERE person_id IN (SELECT id FROM people WHERE name = 'Helena Bonham Carter');
