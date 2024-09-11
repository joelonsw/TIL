## Elastic Search
### ES Basic
*참고: https://victorydntmd.tistory.com/311*
*참고: https://victorydntmd.tistory.com/312*
#### Cluster
- ES의 가장 큰 시스템 단위. node의 집합
- 클러스터는 여러 노드의 집합. 최초 설치시엔 master 노드만 존재함
  - primary shard: 데이터 저장시 나눠진 파티션. 설치시 5개가 존재
  - replica shard: 고가용성을 위해 존재하는 primary shard의 복제본. 설치시 1개 존재
  - primary - replica 는 각기 다른 노드에 존재함. 
- 정리하자면
  - Cluster: 노드의 집합
  - Node: shard의 집합
  - Shard: 데이터를 저장하는 곳. 

#### Index, Type, Document
- Index: 1개 이상의 primary shard에 매핑. 0개 이상의 replica shard를 가질 수 있음. 
  - RDBMS의 DB와 같은 존재
- Type: DB의 테이블과 유사
- Document: DB의 row와 유사

### QueryDSL
*참고: https://victorydntmd.tistory.com/314*
#### Query Context & Filter Context
- **Query Context**
  - 해당 document가 query절과 얼마나 잘 일치하는가?
  - _score를 통해 document가 얼마나 잘 일치하는지는 점수로 나타냄

- **Filter Context**
  - 해당 document가 query절과 얼마나 잘 일치하는가 
  - true/false로만 반환하며, 점수 X

#### match_all / match_none
- 지정된 index의 모든 document. 

#### match
- 텍스트/숫자/날짜를 통해 특정 검색어가 있는 모든 도큐먼트 조회

#### bool
- must: bool must 절 모든 쿼리가 일치하는 도큐먼트 조회
- should: bool should 절 모든 쿼리 중 하나라도 일치하는 도큐먼트 조회
- must_not: bool must_not 절에 지정된 모든 쿼리가 모두 일치하지 않는 도큐먼트 조회
- filter: must와 같이 filter 절에 지정된 모든 쿼리 일치하는 도큐먼트 찾으나, score 무시

#### term
- 역색인에 명시된 토큰 중 정확한 키워드가 포함된 document 조회
- **정확한 키워드**로 검색하기에 full text search에는 적합하지 않음
  - ES에서는 text 타입은 역색인을 함
  - keyword 타입은 역색인 X
- term은 full text search에 안어울려. 이땐 match 써

#### terms
- 키워드 여러개 중 일치하는 document 조회

#### regexp
- 정규표현식 term 쿼리 사용 가능
- term level 쿼리로, 정확한 키워드 검색한다는 뜻!

### 검색 결과 가공하기
*참고: https://victorydntmd.tistory.com/315*
#### from/size
- pagination을 도입하기 위함
  - from: 쪽수
  - size: 게시글 수

#### sort
- 하나 이상의 특정 필드에 대한 정렬
- 기본 정렬은 _score 내림차순

#### _source filtering
- _source를 통해 데이터에서 특정 필드만 반환하도록 할 수 있음
- SELECT의 특정 컬럼 명시하는 것과 비슷

#### aggregation
- 집계를 의미. aggs 필드를 통해 document 갯수를 통계낼 수 있음
- SQL의 group by와 유사

### Aggregation
*참고: https://www.elastic.co/guide/en/elasticsearch/reference/6.7/search-aggregations.html*
*참고: https://esbook.kimjmin.net/08-aggregations/8.1-metrics-aggregations*
#### 개요
- 서치쿼리에 기반하여 aggregated data를 제공
- **Bucketing**
  - 각 버킷은 특정 키 - 도큐먼트로 연결
  - 각 버킷은 모든 컨텍스트 내 도큐먼트와 평가되어 항목이 맞다면, 버켓으로 투입시킴.
- **Metric**
  - 지표를 트래킹하기 위함
- **Matrix**
  - 여러 필드에서 작동/요청된 문서 필드에서 행렬 결과 생성
- **Pipeline**
  - 타 메트릭 출력을 집계

#### Aggregation 만들기
```
"aggregations": {
  "aggregation_name: {
    "aggregation_type": {
      "aggregation_body"
    }
    [,"meta": {[<meta_data_body>]}]?
    [,"aggregations": {[<sub_aggregation>]+ }]?
  },
  [,"<aggregation_name_2>": { ... } ](
}
```

#### Metrics Aggregations
- aggregate 해올 때, document는 쿼리문의 영향을 받아 이를 기반으로 산정
- **min/max/sum/avg** => **stats**로 한번에 가져올 수도 있음!
    ```
    {
      "size": 0, // 이렇게 지정시, hits에 불필요한 도큐먼트 나타나지 않아 성능 up
      "aggs": {
        "all_passangers": {
          "sum": {
            "field": "passangers"
          }
        }
      }
    }
    ```
- **percentiles/percentile_ranks**

##### Bucket Aggregations
- 주어진 조건으로 분류된 버킷을 만들고, 각 버킷에 소속되는 도큐먼트를 모아 그룹으로 구분
- doc_count에 기본 표시됨
- **range**
  - 각 숫자 필드 값으로 범위를 지정, 각 범위에 해당하는 버킷을 만듦
  - field 옵션에 해당 필드 이름 지정, ranges - from, to 사이에 버킷 안에 넣을 친구들 지정 가능

- **histogram**
  - range와 유사하게 숫자 필드의 범위를 나누는 aggs
  - interval 옵션으로 주어진 간격 크기대로 버킷 구분 가능

- **date_range, date_histogram**
  - 날짜 필드를 기반으로 범위별 버킷 생성도 가능

- **terms**
  - keyword 필드의 문자열을 기반으로 버킷을 나누어 집계!
  - keyword 필드값으로만 사용이 가능!!!!
    - 형태소 분석으로 역색인 들어간 text에는 사용 X
