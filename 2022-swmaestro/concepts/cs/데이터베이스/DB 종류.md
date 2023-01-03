### DB 종류

## RDBMS
- MySQL, PostgreSQL
- 행과 열을 가진 표 형식 데이터를 저장하는 형태
- **MySQL**
  - MyISAM 인덱스 압축 기술
  - B트리 기반의 인덱스
  - 스레드 기반의 메모리 할당 시스템
  - 매우 빠른 조인
  - 최대 64개의 인덱스
  - 대용량 데이터베이스를 위한 설계
    - 롤백, 커밋, 이중 암호 지원 보안 

- **MySQL 구조**
  - MySQL Connectors(Application)
  - MySQL Shell
  - MySQL Server Process(mysqld)
    - NoSQL
    - SQL Interface
    - Parser
    - Optimizer
    - Caches & Buffers
    - Storage Engines (https://jobc.tistory.com/196)
      - InnoDB
        - 디폴트
        - 트랜잭션 지원
        - row-level locking => multi-thread에 유리
        - PK 기반으로 "clustered index"에 저장 => PK 기반의 쿼리 비용 절감
      - MyISAM
        - 테이블 레벨 락킹(1개 row 읽더라도 테이블 전체 락 걸어) => multi-thread에 불리
        - 기능적으로 단순해, 단순 조회의 경우 InnoDB보다 속도 빠름
        - MyISAM이 InnoDB보다 빠르지만, Order By등 정렬의 구문이 들어가면 InnoDB보다 느림
        - Full text Searching 지원
      - NDB Cluster
      - Memory
    - File System
    - Files & Logs

## NoSQL
- **Redis**
  - 인메모리 데이터베이스이자 키-값 모델 기반의 DB