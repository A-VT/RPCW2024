# Quais as cidades de um determinado distrito?
     Exemplifica-se com o distrito "Lisboa"

```sparql
Select * where{
    ?city mapa:distrito "Lisboa"
}
```

# Distribuição de cidades por distrito?
```sparql
SELECT ?distrito (COUNT(?cidade) AS ?nCidades)
WHERE {
  ?cidade mapa:distrito ?distrito .
}
GROUP BY ?distrito
```

# Quantas cidades se podem atingir a partir do Porto?
```sparql
SELECT (COUNT(?cidade) AS ?nCidades)
WHERE {
  ?cidade mapa:tem_origem ?lig .
  ?lig mapa:tem_origem ?porto .
  ?porto mapa:nome "Porto" .
}

```

# Quais as cidades com população acima de um determinado valor?
    Exemplifica-se com o valor populacional 500000 (quinhentos mil).
```sparql
SELECT ?cidade
WHERE {
  ?cidade mapa:populacao ?pop .
  FILTER (xsd:integer(?pop) > 500000)
}
```
