## 대규모 시스템 설계 기초 ch7. 분산 시스템을 위한 유일 ID 생성기 설계
*참고: https://github.com/shinhee-rebecca/system-design-interview-1/blob/main/7%EC%9E%A5/README.md*  

- **개요**
  - 분산 시스템이 아니라면 DB auto_incr 면 될텐데, 분산은 안 됨

- **UUID**
  - 128 비트 수로, UUID값은 충돌이 거의 없음. 
  - 각 서버가 알아서 만들기에 규모 확장도 쉬움
  - 다만, 시간 정렬이 어려움. 숫자만 쓰이지도 않음

- **티켓 서버**
  - 단일 ID를 중앙 집중형에서 만드는 방식
  - SPOF

- **트위터 스노우플레이크**
  - *참고: https://github.com/shinhee-rebecca/system-design-interview-1/blob/main/7%EC%9E%A5/README.md#%ED%8A%B8%EC%9C%84%ED%84%B0-%EC%8A%A4%EB%85%B8%EC%9A%B0%ED%94%8C%EB%A0%88%EC%9D%B4%ED%81%AC-%EC%A0%91%EA%B7%BC%EB%B2%95*
