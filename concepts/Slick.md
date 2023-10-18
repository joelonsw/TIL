### Slick
*참고: https://scala-slick.org/*

#### 개요
- **Reactive Functional Relational Mapping for Scala**
- 내세우는 키워드 : **스칼라**, **타입 안정성**, **합성 가능함**
- 슬릭은 스칼라 기반의 강타입 + 합성에 용이한 advanced, comprehensive 데이터베이스 접근 라이브러리
- 데이터베이스를 자연스럽게 쓸 수 있는 강점을 제공
- 스칼라 컬렉션을 통해 관계형 데이터베이스를 다루는 것을 지원
- 스칼라를 통해 컴파일 타임에 안전하고 합성에 용이한 쿼리를 만들어 낼 수 있다. 

#### Intro
- Slick : Scala Language-Integrated Connection Kit
- 스칼라 기반의 FRM 라이브러리
- 거의 스칼라 컬렉션을 쓰는 것 마냥 사용하되, 데이터베이스의 모든 기능을 쓸 수 있도록 지원함
- SQL을 직접 쓰는것도 가능함
- DB 액션은 비동기적으로 처리됨
- Play, Akka와 궁합이 좋음
- 쌩 쿼리에 비해 스칼라 코드를 쓰면 컴파일 타임에 타입 안정성을 확보할 수 있으며, 합성에 용이한 장점이 있음

#### FRM (Functional Relational Mapping)
- 함수형 프로그래머들은 객체지향 <-> DB간 미스매치로 인해 고생했다
- 슬릭의 FRM은 스칼라로 매핑이 완전하도록 지원하고, 느슨한 결합, 적은 설정, 관계형 데이터 베이스의 복잡성을 추상화시켜 없앤 장점을 제공한다.
- 관계형 모델을 함수형 패러다임으로 엮어 내려고 노력했다. 
- Slick은 관계형 데이터베이스를 직접 통합하여 거의 인메모리 스칼라 컬렉션 마냥 쓸 수 있도록 지원한다. 
    ```scala
    class Coffees(tag: Tag) extends Table[(String, Double)](tag, "COFFEES") {
        def name = column[String]("COF_NAME", O.PrimaryKey)
        def price = column[Double]("PRICE")
        def * = (name, price)
    }
    
    val coffees = TableQuery[Coffees]
    
    coffees.map(_.name)
    coffees.filter(_.price < 10)
    ```
- 슬릭의 FRM 접근은 다음의 장점을 제공한다
  - 미리 최적화 + 효율성
  - 타입 안정성 : 컴파일러가 에러 찾아줌
  - 합성 가능한 쿼리 : 쿼리 골라와서 컬렉션 마냥 map() 합성도 가능

#### 제공 기능
- 스칼라 컬렉션 API에서 영감을 받은 쿼리 API
- 슬릭을 통해 데이터베이스의 스키마
- 비동기 API를 통해 Future를 활용할 수 있어
  - Reactive Stream 인터페이스 활용 가능
  - Akka, FS2, ZIO와 함께 쓸 수 있음
- 합성을 많은 단계에서 할 수 있음
- advanced한 쿼리 컴파일러를 통해 SQL을 생성할 수 있음