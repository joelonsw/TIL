## QueryDsl

### Why QueryDsl?
- 장점
  1. 컴파일 타임에 에러를 잡아낼 수 있음!
  2. 파라미터 바인딩을 자바 코드로 할 수 있음!

### Q-Type
- gradle build를 통해 build 디렉토리 하위에 엔티티에 대해 QType 인스턴스를 만들어 둔다
- QMember qMember = QMember.member => 이렇게 기본 인스턴스를 사용할 수 있음

### Projection
- 결과를 DTO 반환할 때 사용함
  - 프로퍼티 접근 (Projections.bean)
  - 필드 직접 접근 (Projections.fields)
  - 생성자 사용 (Projections.constructor)
- `@QueryProjection`
  - 컴파일러로 타입 체크하여 QType으로 컴파일한(빌드된) 객체에 대해 new 연산자로 뚝

### Tips
- JPAQueryFactory를 필드로 가지면 동시성 문제는? 
  - 동시성 문제는 JPAQueryFactory를 생성 시 제공되는 EntityManager에 달림
  - 여러 쓰레드에서 동시에 같은 EntityManager에 접근해도, 트랜잭션 마다 별도의 Persistence Context를 제공하기에 동시성 문제는 걱정 X

- List<Tuple\>을 통한 결과 조회
  - Jpql에서 제공하는 모든 집합 함수 제공
  - 어떤 필드 추출할지 select 문에서 고르면 튜플에 저장됨
  - QueryDsl에서 제공하는 클래스이니, repository에서만 사용하는 것 추천

- from 절의 서브쿼리 한계
  - JPA/JPQL 서브쿼리의 한계점으로 from 절에서 서브쿼리는 지원 X

- 수정/삭제 벌크 연산
  - 쿼리 한번으로 많은 데이터를 수정함
  - 영속성 컨텍스트와 무관하게 쿼리가 나감.
  - 조회 로직에서는 영속성 컨텍스트가 항상 우선권을 가짐!
