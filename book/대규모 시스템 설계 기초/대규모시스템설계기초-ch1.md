## 대규모 시스템 설계 기초 ch1. 사용자 수에 따른 규모 확장성
- **서버의 확장에서 고려할 점**
  - NoSQL 알맞은 걸 잘 써보자
    - 용도
      - 낮은 지연시간 필요
      - 데이터가 비정형
      - 데이터 직렬/역직렬화만 필요
      - 많은 데이터 저장 필요
    - 종류
      1. K-V store
      2. graph store
      3. column store
      4. document store
  - 수직적 vs 수평적 규모 확장
    - 수직적은 확장에 한계가 있고, failover에 취약
  - DB 다중화를 할 때엔, 지역적으로 떨어진 곳에 배치하고, 장애 상황시 데이터 싱크 맞출 수 있도록 하자
  - 캐시 전략
    - 어떤 상황에 바람직? (갱신 << 참조)
    - TTL 정책은 어떻게? 
    - SPOF가 되진 않을지 고려
  - CDN 사용시 ?v=2 를 붙여 갱신이 필요하면 진행
  - Stateless한 백엔드를 만들어야 확장성이 좋음

- **데이터 센터**
  - geo-routing: 지리적 라우팅으로 사용자 위치에 따라 도메인을 어떤 IP로 반환할지 결정
  - 여러 리전에 데이터센터가 분포해있다면, 데이터를 여러 데이터 센터에 걸쳐 다중화를 해둘 수 있게 하자. 
  - 자동화된 배포 도구는 모든 데이터 센터에 설치하자

- **MQ, 로그/메트릭/자동화**
  - MQ로 시스템 컴포넌트를 분리하여 각기 독립적으로 확장될 수 있도록 하자
    - loosely coupled

- **DB 규모 확장**
  - 수직적 확장은 계속 한계가 나옴
    - CPU/RAM 무한 증설 불가
    - SPOF 위험성 증가
    - 비용의 증대
  - 수평적 확장
    - 샤드를 도입하자. 
    - 샤드의 문제)
      - 데이터 재 샤딩이 필요할 수 있음. 안정 해시 기법을 통해서 해결할 수 있다고 함
      - 유명인사 문제: 쪼갰는데 쪼갠 효과가 없는 경우. (알림톡은 허파 id)
        - 그냥 무지성 id modulo 가 더 안좋을 수 있음

### 스터디
- NoSQL이 수평적으로 확장이 좋다고 하던데... (ex. ElasticSearch?)
- 원형 다중화: Master 업데이트 -> binlog -> Slave -> binlog
  - Active-Active 동기화 고급 복제 방식
  - 장점) 모든 binlog 확장 용이
  - 각 클러스터가 동시에 데이터 변경이 가능하며, 장애 복구와 부하 분산에 매우 유용. 
  - 다만, 복제 충돌 관리와 세심한 설정이 필수
- Scaling Memcache at Facebook
- 캐시 Overprovision : 적당한 메모리 크기를 갖기
- 동적 컨텐츠 캐시 캐싱도 가능
  - 9시 00분 00초에 딱 엄청 몰리는 시점에 짧은 TTL로 진행하기
- 로드밸런서 고장나면 어떻게하지? 
  - 다중화-이중화 해두자
  - Hot Standby Router Protocol: http://www.ktword.co.kr/test/view/view.php?no=2812
- 이중화를 해두어서 페일오버 처리해도 다른쪽이 다 그걸 받아낼 만큼 인프라 구축을 할 수 있는가? 비용은 감당할 수 있는가?
- 로컬 캐시/서버 캐시의 TTL이 다른 경우 어떻게 하는가?
  - DB에서 트래픽이 집중되어 부하의 원인이 될 수 있음
  - *https://techblog.lycorp.co.jp/ko/req-saver-for-thundering-herd-problem-in-cache*
  - 캐시 없을 때, 맨 처음 부하가 너무 심할거같은데? -> 분산락해서 배포 충격 막자
  - 분산락을 걸어둬서 캐시 Set하는거 한쪽에서만
  - 어플리케이션 warm up 로딩할 때 뚝딱 cache에 적재
- DBMS 자체에서 샤딩 제공해준다. 
- https://www.notion.com/ko/blog/sharding-postgres-at-notion
