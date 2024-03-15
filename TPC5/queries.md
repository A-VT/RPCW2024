# Queries for TPC5

## List of Movies
```sparql
SELECT *
WHERE
{
?film a dbo:Film.
?film dbp:name ?filmName.
?film rdfs:label  ?label.
filter(lang(?label)="en").
}
```

## Directors on a specified movie
```sparql
select distinct ?film ?dir where {
?film a dbo:Film.
?film dbo:director ?dir.
?dir dbp:name ?dirName
?dir dbp:name ?dirName
} LIMIT 100
```

## Main Actors on a specified movie

## Secundary Actors on a specified movie

##