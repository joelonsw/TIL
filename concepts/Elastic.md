## Elastic
*참고: https://esbook.kimjmin.net/*
*참고: https://www.youtube.com/watch?v=Ks0P49B4OsA&list=PLhFRZgJc2afp0gaUnQf68kJHPXLG16YCf*

### 1. Elastic Stack 소개
- **ElasticSearch**
    - Full Text Search 강점
    - 타 플랫폼 연동이 쉬움
    - 오픈 소스 (루씬 기반)
    - 실시간 분석 시스템
        - 배치 기반의 분석 시스템
        - 소스 데이터, 분석을 수행할 프로그램 올려 놓고 분석을 실행해 결과 셋 도출
        - ElasticSearch 클러스터가 실행되고 있는 동안에는 계속해서 데이터가 입력됨
        - 그와 동시에 실시간에 가까운 속도로 색인된 데이터의 검색/집계 가능
    - Full Text 검색 엔진
        - inverted file index 구조로 데이터 저장
        - JSON 형식으로 응답 전달
        - 복합적인 정보 포함하는 형식 문서 그대로 전달
        - logstash를 통해 CSV, Apache log, syslog 등으로 변환
    - REST API 지원
    - 멀티테넌시
        - 서로 다른 인덱스 별도 커넥션 없이 하나의 질의로 묶어서 검색/하나의 출력으로 도출

- **Logstash**
    - 데이터 수집/저장을 위한 프로젝트
    - 데이터 수집의 도구가 필요했던 ElasticSearch가 입력 수단으로 Logstash 도입
    - LogStash의 데이터 처리 과정
        - `입력 -> 필터 -> 출력`

- **Kibana**
    - ElasticSearch의 검색 결과 시각화
        - Discover: 색인된 소스 데이터들의 검색, 시계열 기반 시간 히스토그램 그래프 출력
        - Visualize: 집계 데이터를 통해 통계 차트로
        - Dashboard: Visualize로 만들어진 시각화 도구 조합 => 대시보드 화면

- **Beats**
    - Logstash의 데이터 수집이 부피가 커짐으로써 자원을 많이 요하게 됨
    - 모든 단말에 Logstash 도입? => 부담스러움
    - Beats를 통해 가볍게 데이터 수집할 수 있도록 지원

### 2. ElasticSearch 시작하기
- **데이터 색인**
  - 색인(indexing): 데이터가 검색될 수 있는 구조로 변경하기 위해 원본 문서를 **검색어 토큰**들로 변환하여 저장하는 과정
  - 인덱스(index): 색인 과정을 거친 결과물, 또는 색인된 데이터가 저장되는 저장소
  - 검색(search): 인덱스에 들어있는 검색어 토큰들을 포함하고 있는 문서 찾아가는 과정
  - 질의(query): 사용자가 원하는 문서 찾기/집계 결과 출력하기

- **설치 및 실행**
  - 노드(master, data, ingest, ml)
    - 각자의 노드들이 서로 다른 역할을 수행하도록 클러스터를 구성할 수 있다. 
    - 모든 디폴트 값은 true
    - 노드는 명시된 모든 역할들을 수행
    - 특정 값들을 false로 설정해 노드 역할 구분지어 클러스터 구성 가능
  - `node.master: true`
    - 모든 클러스터는 1개의 마스터 노드가 선출
    - false로 지정하면, 이건 마스터 노드 후보에서 제외됨
  - `node.data: true`
    - 노드가 데이터를 저장하도록 한다. false라면 저장 X
  - `node.ingest: true`
    - 데이터 색인시 전처리 작업인 ingest pipeline 작업의 수행을 할 수 있는지 여부 지정
  - `node.ml: true`
    - 노드가 머신러닝 작업을 수행할 수 있는지 여부 지정
  - 전용 마스터 노드 설정
    ```yml
    # config/elasticsearch.yml - 전용 마스터 노드 설정
    node.master: true
    node.data: false
    node.ingest: false
    node.ml: false
    ```


























