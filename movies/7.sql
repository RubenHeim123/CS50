SELECT movies.title, ratings.rating fROM movies
JOIN ratings ON ratings.movie_id = movies.id
WHERE year = 2010
ORDER BY rating DESC, title;
