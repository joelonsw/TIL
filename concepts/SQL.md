## SQL

## Create (생성)
```sql
CREATE TABLE table_name {
    id int NOT NULL,
    name char(50) NOT NULL,
    address char(50),
    CONSTRAINT id_pk PRIMARY KEY(id)
}

INSERT INTO table_name (col1, col2, col3) VALUES (val1, val2, val3);
```

## Read (조회)
```sql
SELECT * FROM table_name;
SELECT * FROM table_name WHERE col1 = '1';
SELECT * FROM table_name WHERE col2 LIKE "SQL%";
SELECT * FROM table_name WHERE date BETWEEN '1997-01-01' AND '1997-12-31';
SELECT * FROM table_name WHERE id IN (1, 2 ,3);
SELECT * FROM table_name ORDER BY col1;
SELECT * FROM table_name LIMIT 5;
SELECT * FROM table_name GROUP BY col1;
SELECT * FROM table_name GROUP BY col1 HAVING col2 = '1';
```

- **쿼리 실행 순서**
  1. FROM
  2. ON
  3. JOIN
  4. WHERE
  5. GROUP BY
  6. HAVING
  7. SELECT
  8. DISTINCT
  9. ORDER BY

## Update (수정)
```sql
UPDATE table_name SET col1 = '1' WHERE col2 = 'name';
```
  
## Delete (삭제)
```sql
DELETE FROM table_name where col = '1';
```
