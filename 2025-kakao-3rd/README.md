# 2025년 학습 기록 (Today I Learned)

지난 1년간 공부한 내용들을 정리한 Today I Learned (TIL) 저장소입니다. 월별 학습 기록, 특정 개념, 책 스터디로 나누어 관리하고 있습니다.

## 📚 학습 카테고리

- [월별 TIL (Monthly TILs)](#월별-til)
- [개념 정리 (Concepts)](#-개념-정리)
- [책 스터디 (Book Studies)](#-책-스터디)

---

## 월별 TIL

### (2025년 1월)
- **[2025-01-02.md](./2025-01/2025-01-02.md)**: Slick 2.x에서 3.x으로의 트랜잭션 마이그레이션, DBIOAction 및 `transactionally` 개선점 학습.
- **[2025-01-03.md](./2025-01/2025-01-03.md)**: Redis의 다양한 구성(Standalone, Master-Slave, Cluster), Pub/Sub 모델 및 Scala 라이브러리 비호환성 문제 학습.
- **[2025-01-05.md](./2025-01/2025-01-05.md)**: Play Framework의 요청-응답 주기, NIO 논블로킹 서버, Netty EventLoop, Play SBT 플러그인 역할 학습.
- **[2025-01-16.md](./2025-01/2025-01-16.md)**: Redis 성능, 메모리, 활동, 지속성, 오류 관련 모니터링 지표 학습.

### (2025년 2월)
- **[2025-02-17.md](./2025-02/2025-02-17.md)**: `LocalDateTime`과 `Date`의 차이, Play Framework 버전업에 따른 Akka ActorSystem DI 방식 변경 학습.
- **[2025-02-18.md](./2025-02/2025-02-18.md)**: Akka SupervisorStrategy 및 ActorContext의 역할과 기능 학습.
- **[2025-02-21.md](./2025-02/2025-02-21.md)**: Scala `Future`의 `andThen` 동작 방식과 Play Framework에서의 비동기 예외 처리 학습.
- **[2025-02-22.md](./2025-02/2025-02-22.md)**: 싱글코어 CPU에서의 병렬 처리 가능성 및 이벤트 루프 아키텍처 학습.
- **[2025-02-26.md](./2025-02/2025-02-26.md)**: 함수형 프로그래밍의 모나드 개념과 Slick의 DBIO 모나드 학습.

### (2025년 3월)
- **[2025-03-06.md](./2025-03/2025-03-06.md)**: Scala의 경로 종속 타입(Path-dependent type)으로서의 내부 클래스 특징 학습.
- **[2025-03-07.md](./2025-03/2025-03-07.md)**: Play Framework에서 비동기 처리 시 `Future`와 ExecutionContext의 동작 방식 및 DB 커넥션 풀의 `maxLifetime` 문제 해결.
- **[2025-03-14.md](./2025-03/2025-03-14.md)**: JVM 기반 APM 도구인 Kamon의 개념, 리포터, Play/Akka 연동 및 다양한 모듈 학습.

### (2025년 4월)
- **[2025-04-11.md](./2025-04/2025-04-11.md)**: GitOps 기반 Kubernetes 배포 도구인 ArgoCD의 개념, 장점, 활용 사례 학습.
- **[2025-04-15.md](./2025-04/2025-04-15.md)**: React에서 발생하는 Stale Closure 문제의 원인과 `useCallback` 의존성 배열을 통한 해결 방법 학습.
- **[2025-04-18.md](./2025-04/2025-04-18.md)**: ELK 스택에서 Filebeat와 Logstash를 사용한 로그 수집, 필터링, 인덱싱 파이프라인 구성 학습.
- **[2025-04-19.md](./2025-04/2025-04-19.md)**: RabbitMQ의 메시지 손실 방지를 위한 DLX/DLQ 구성 및 내구성(Durability) 설정 학습.
- **[2025-04-29.md](./2025-04/2025-04-29.md)**: Elasticsearch의 `refresh` 정책과 `netstat`, `curl`, `netcat` 등 네트워크 진단 도구 사용법 학습.

### (2025년 5월)
- **[2025-05-02.md](./2025-05/2025-05-02.md)**: Elasticsearch에서 `_update_by_query`와 `_reindex` API를 사용한 데이터 필드 추가 및 업데이트 방법 학습.
- **[2025-05-10.md](./2025-05/2025-05-10.md)**: Kubernetes 클러스터의 `ifconfig` 출력을 통해 `cni0`, `flannel.1`, `veth` 등 네트워크 인터페이스 구조 학습.
- **[2025-05-12.md](./2025-05/2025-05-12.md)**: MySQL 8.0 이상에서 `REGEXP`를 사용한 정규표현식 검색 쿼리 작성법 학습.
- **[2025-05-16.md](./2025-05/2025-05-16.md)**: 데이터베이스 반정규화의 개념, RabbitMQ `prefetch_count`의 역할 및 성능 최적화, consistent-hash-exchange, Redisson 분산락 학습.
- **[2025-05-19.md](./2025-05/2025-05-19.md)**: Redis 분산락 구현체인 Lettuce와 Redisson(RedLock)의 동작 방식 및 장단점 비교 학습.
- **[2025-05-23.md](./2025-05/2025-05-23.md)**: RabbitMQ의 `prefetch_count`, Connection과 Channel의 관계, Consumer의 ACK 전략 학습.
- **[2025-05-26.md](./2025-05/2025-05-26.md)**: RabbitMQ Consume 시 전달되는 메시지 메타데이터 객체 `Envelope`의 주요 정보 학습.
- **[2025-05-27.md](./2025-05/2025-05-27.md)**: Akka Actor 설정 파일(`akka.conf`)을 통한 라우터, 디스패처, 스레드 풀 설정 및 DI 바인딩 방법 학습.
- **[2025-05-29.md](./2025-05/2025-05-29.md)**: RabbitMQ의 Connection, Channel, Consumer의 관계 및 멀티 채널/단일 채널 구성 비교, 클러스터링과 미러링 개념 학습.

### (2025년 6월)
- **[2025-06-17.md](./2025-06/2025-06-17.md)**: Kubernetes `StorageClass`를 통한 동적/수동 PV 프로비저닝 방법 학습.
- **[2025-06-19.md](./2025-06/2025-06-19.md)**: Kubernetes `IngressClass`의 역할과 여러 Ingress Controller를 관리하는 방법 학습.
- **[2025-06-20.md](./2025-06/2025-06-20.md)**: Redis의 `set`, `setnx`, `setnxex` 명령어 차이점 및 Redisson 분산락과의 안정성 비교, 안드로이드 인텐트 URL 스킴 학습.
- **[2025-06-22.md](./2025-06/2025-06-22.md)**: Kubernetes 환경에서 `openssl`을 이용한 CSR 생성, 서명, `kubeconfig` 등록까지의 사용자 인증서 관리 절차 학습.
- **[2025-06-25.md](./2025-06/2025-06-25.md)**: RabbitMQ 3.x에서 4.x로의 변경점, 특히 Quorum Queue의 도입과 Classic Queue 미러링 제거에 대해 학습.
- **[2025-06-26.md](./2025-06/2026-06-26.md)**: Kubernetes `StatefulSet`의 특징(고유 식별자, 순차적 배포)과 고정 IP 할당 방법 학습.
- **[2025-06-27.md](./2025-06/2025-06-27.md)**: Kubernetes `NetworkPolicy`를 사용한 Ingress/Egress 트래픽 제어 및 Pod 격리 방법 학습.

### (2025년 7월)
- **[2025-07-05.md](./2025-07/2025-07-05.md)**: 클라이언트 측 세션, 서버 측 세션, JWT의 특징 비교 및 Play Framework에서의 세션 처리 방식 학습.
- **[2025-07-08.md](./2025-07/2025-07-08.md)**: Redisson `RedissonMultiLock`의 동작 원리, 오버헤드, 데드락 발생 가능성 분석.
- **[2025-07-16.md](./2025-07/2025-07-16.md)**: Kubernetes `Headless Service`의 개념과 `StatefulSet`과의 연동을 통한 파드 직접 접근 방법 학습.
- **[2025-07-18.md](./2025-07/2025-07-18.md)**: Kubernetes `Job`을 이용한 배치 작업 실행 및 `DaemonSet`과 `StaticPod`의 차이점 학습.
- **[2025-07-19.md](./2025-07/2025-07-19.md)**: `kubectl -o` 출력 옵션(yaml, jsonpath 등) 및 Kubernetes RBAC의 핵심 구성요소(Role, RoleBinding, ClusterRole) 학습.
- **[2025-07-20.md](./2025-07/2025-07-20.md)**: Kubernetes `nodeAffinity`와 `podAffinity`를 이용한 스케줄링 제어 및 `rollout restart` 명령어 학습.
- **[2025-07-24.md](./2025-07/2025-07-24.md)**: RabbitMQ 지연 큐(Delayed MQ) 구현 방법 비교 및 Akka Actor와 MQ의 동시성 처리 방식 비교, VectorDB와 Elasticsearch의 차이점 학습.
- **[2025-07-31.md](./2025-07/2025-07-31.md)**: RabbitMQ 메시지 발행 시 병렬 처리 성능 문제 원인(공유 ExecutionContext, 단일 채널) 및 해결(채널 풀링, `queueDeclarePassive` 최적화) 과정 학습.

### (2025년 8월)
- **[2025-08-12.md](./2025-08/2025-08-12.md)**: 헥사고날 아키텍처(포트와 어댑터)의 개념, 필요성, 장점 학습.
- **[2025-08-18.md](./2025-08/2025-08-18.md)**: Play Framework(`sbt dist`)와 Spring Boot(fat Jar)의 배포 프로세스 비교 및 RabbitMQ 클라이언트의 JVM Hang 문제 원인 학습.

### (2025년 9월)
- **[2025-09-12.md](./2025-09/2025-09-12.md)**: 디자인 패턴 중 하나인 퍼사드(Facade) 패턴의 개념과 Akka Actor에서 `sender()`를 안전하게 참조하기 위한 `pipeTo` 패턴 학습.
- **[2025-09-30.md](./2025-09/2025-09-30.md)**: Spring Data JPA의 인터페이스 기반 및 클래스 기반 프로젝션(Projections)을 사용한 쿼리 결과 매핑 방법 학습.

### (2025년 10월)
- **[2025-10-09.md](./2025-10/2025-10-09.md)**: Elasticsearch 클러스터의 구조(노드, 인덱스, 샤드)와 역할(마스터, 데이터) 분리 학습.
- **[2025-10-28.md](./2025-10/2025-10-28.md)**: Scala에서 JVM의 타입 이레이저 문제를 해결하는 `TypeTag`와 `ClassTag`의 역할과 용도 학습.

### (2025년 11월)
- **[2025-11-03.md](./2025-11/2025-11-03.md)**: Akka Actor에서 `pipeTo` 패턴을 사용한 안전한 비동기 재처리 및 `akka.pattern.retry` 유틸리티 함수 학습.
- **[2025-11-12.md](./2025-11/2025-11-12.md)**: 유니코드의 기본 개념(코드 포인트, 인코딩)과 MySQL에서의 `utf8mb4` 인코딩 및 `collation` 설정 학습.
- **[2025-11-26.md](./2025-11/2025-11-26.md)**: HTTP 3xx 리다이렉션 상태 코드(301, 308, 302, 307, 303)의 차이점 학습.
- **[2025-11-27.md](./2025-11/2025-11-27.md)**: RBAC(역할 기반 접근 제어)의 개념, Vault 시크릿 관리를 위한 VSO와 ESO 비교, Helm과 Kustomize 실무 전략 학습.

### (2025년 12월)
- **[2025-12-22.md](./2025-12/2025-12-22.md)**: Kubernetes 환경에서 Filebeat를 `DaemonSet`과 `Sidecar` 방식으로 배포할 때의 장단점 비교.
- **[2025-12-24.md](./2025-12/2025-12-24.md)**: Kubernetes Deployment에서 Filebeat를 사이드카 컨테이너로 설정하는 YAML 예제 학습.

---

## 💡 개념 정리

- **[AI.md](./concepts/AI.md)**: Anthropic Claude API 사용법, 프롬프트 엔지니어링 및 평가, Tool 사용법.
- **[CKA.md](./concepts/CKA.md)**: CKA(Certified Kubernetes Administrator) 시험 준비를 위한 핵심 요약, 모의고사 풀이 및 주요 개념(CNI, Helm, Kustomize, Gateway API, RBAC, 스토리지, 트러블슈팅 등) 정리.
- **[Kubernetes.md](./concepts/Kubernetes.md)**: 쿠버네티스 아키텍처, 핵심 리소스(Pod, Deployment, Service, Ingress), 스케줄링, 보안(CSR, RBAC, Admission Controller), 네트워크, 스토리지(PV, PVC, StorageClass), 고가용성, Helm, Kustomize 등 전반적인 개념 정리.
- **[Multi Module.md](./concepts/Multi%20Module.md)**: SBT를 사용한 Scala(Play Framework) 멀티 모듈 프로젝트 구성 방법.

---

## 📖 책 스터디

### Kotlin In Action
- **[Chapter 1](./book/Kotlin%20In%20Action/KotlinInAction-ch1.md)**: 코틀린의 주요 특성, 철학, 사용 분야.
- **[Chapter 2](./book/Kotlin%20In%20Action/KotlinInAction-ch2.md)**: 코틀린 기본 요소(함수, 변수), 클래스와 프로퍼티, `enum`과 `when`, 루프, 예외 처리.
- **[Chapter 3](./book/Kotlin%20In%20Action/KotlinInAction-ch3.md)**: 컬렉션, 확장 함수와 프로퍼티, 중위 함수, 문자열 및 정규식 처리.

### 대규모 시스템 설계 기초
- **[Chapter 1](./book/대규모%20시스템%20설계%20기초/대규모시스템설계기초-ch1.md)**: 사용자 수에 따른 시스템 규모 확장, 데이터베이스 다중화, 캐시, CDN, 무상태 아키텍처.
- **[Chapter 2](./book/대규모%20시스템%20설계%20기초/대규모시스템설계기초-ch2.md)**: QPS, 저장소 요구량 등 대략적인 규모 추정 방법.
- **[Chapter 4](./book/대규모%20시스템%20설계%20기초/대규모시스템설계기초-ch4.md)**: 처리율 제한 장치의 필요성 및 다양한 알고리즘(토큰 버킷, 누출 버킷 등).
- **[Chapter 5](./book/대규모%20시스템%20설계%20기초/대규모시스템설계기초-ch5.md)**: 안정 해시(Consistent Hashing)의 개념과 가상 노드를 통한 데이터 분포 균등화.
- **[Chapter 6](./book/대규모%20시스템%20설계%20기초/대규모시스템설계기초-ch6.md)**: 키-값 저장소 설계, CAP 정리, Quorum 프로토콜, 가십 프로토콜.
- **[Chapter 7](./book/대규모%20시스템%20설계%20기초/대규모시스템설계기초-ch7.md)**: 분산 시스템에서 유일 ID를 생성하는 방법(UUID, 티켓 서버, 스노우플레이크).
- **[Chapter 8](./book/대규모%20시스템%20설계%20기초/대규모시스템설계기초-ch8.md)**: URL 단축기의 동작 원리, 해시 충돌, Base-62 변환.
- **[Chapter 9](./book/대규모%20시스템%20설계%20기초/대규모시스템설계기초-ch9.md)**: 웹 크롤러의 기본 구조, BFS/DFS, 신선도 유지, 성능 최적화.
- **[Chapter 10](./book/대규모%20시스템%20설계%20기초/대규모시스템설계기초-ch10.md)**: 알림 시스템 설계, 안정성(재시도, 중복 방지), 템플릿, 전송률 제한.
- **[Chapter 11](./book/대규모%20시스템%20설계%20기초/대규모시스템설계기초-ch11.md)**: 뉴스 피드 시스템 설계, 팬아웃(Push/Pull) 모델 비교.
- **[Chapter 12](./book/대규모%20시스템%20설계%20기초/대규모시스템설계기초-ch12.md)**: 채팅 시스템 설계, 웹소켓, 메시지 흐름, 접속 상태 관리.
- **[Chapter 13](./book/대규모%20시스템%20설계%20기초/대규모시스템설계기초-ch13.md)**: 검색어 자동 완성 시스템 설계, 트라이(Trie) 자료구조 활용.
- **[Chapter 14](./book/대규모%20시스템%20설계%20기초/대규모시스템설계기초-ch14.md)**: 유튜브와 같은 대규모 비디오 스트리밍 시스템 설계, 트랜스코딩, DAG 파이프라인, CDN 최적화.
