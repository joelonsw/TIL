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
  5. GROUP BY : WHERE 구로 검색한 뒤, 열의 값을 기준으로 그룹화하여 집계!
  6. HAVING : GROUP BY의 조건절
  7. SELECT
  8. DISTINCT
  9. ORDER BY

- **쿼리 실행 순서 예시**
  ```sql
  SELECT city AS `도시`, COUNT(city) AS `집계`
  FROM user 
      WHERE user.age >= 18
          GROUP BY city
              HAVING city >= 'b'
                  ORDER BY city;
  ```
  1. FROM 에서 데이터 집합을 만든다
  2. WHERE는 FROM에서 만든 데이터 집합을 조건에 맞게 걸러낸다
  3. GROUP BY는 WHERE에서 필터링한 데이터를 그룹화 한다
  4. HAVING은 GROUP BY에서 집계한 데이터 집합을 다시 조건에 맞게 필터링한다
  5. SELECT는 그룹화하고 필터링한 데이터 집합을 집계한다
  6. ORDER BY는 집계한 데이터 집합을 정렬한다

## Update (수정)
```sql
UPDATE table_name SET col1 = '1' WHERE col2 = 'name';
```
  
## Delete (삭제)
```sql
DELETE FROM table_name where col = '1';
```

## 재귀테이블
```sql
WITH RECURSIVE TEMP_HOUR AS (
  SELECT 0 AS HOUR 
  UNION ALL 
  SELECT HOUR+1
  FROM TEMP_HOUR
  WHERE HOUR < 23
);
```

## IF절
```sql
IF (조건, '참', '거짓') AS 'column 이름'
---
SELECT 
       ANIMAL_TYPE, 
       IF(NAME IS NOT NULL, NAME, 'No name') AS `NAME`, 
       SEX_UPON_INTAKE
FROM ANIMAL_INS;
```

## 문자열
- **합치기**
  - `CONCAT('a', 'b')`

- **자르기**
  - `SUBSTRING(STR, 1, 10)`

## DATETIME
- **연/월/일/시/분/초**
  - `YEAR(DATETIME)`
  - `MONTH(DATETIME)`
  - `DAY(DATETIME)`
  - `HOUR(DATETIME)`
  - `MINUTE(DATETIME)`
  - `SECOND(DATETIME)`

- **DATE_FORMAT()**
  - `DATE_FORMAT(DATETIME, '%Y-%m-%d')`

## TIP
- **COLUMN 중에 NULL이 있을 수도 있으니, IS NOT NULL 조건을 추가해줘야 하나 확인할 것**

- **문제의 조건을 읽고, 조건을 모두 노트에 옮겨 적어두는 것도 방법!**
