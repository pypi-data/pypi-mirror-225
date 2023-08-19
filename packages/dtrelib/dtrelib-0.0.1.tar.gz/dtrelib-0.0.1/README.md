# Drite test reporting engine core
Core library consist of 5 classes, providing main functions for work with clickhouse, tables, table streams and data processing.

## Query
Query class provide interaction with clickhouse database and (re)storing data into Redis caching database 

## ResultSet
ResultSet is a container of data with additional attributes

## ResultSetStream
ResultSetStream is made as a wrapper over ResultSet to make available file-by-file queries

## Processor
Processor consist of set of scalar and vector functions to process datasets in serial processing line.

