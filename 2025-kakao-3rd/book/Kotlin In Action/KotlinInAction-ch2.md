## Kotlin In Action - ch2. 코틀린 기초
### 2.1 기본 요소: 함수와 변수
- **특성**
  - 최상위에 있는 main함수를 어플리케이션의 진입점 지정 가능. main에 인자가 없어도 됨
  - 더 간결한 구문을 사용할 수 있는 wrapper 제공. ex) println

- **식(Expression) vs 문(Statement)**
  - 식: 값을 만들어내며 다른 식의 하위 요소로 계산에 참여할 수 있음
  - 문: 자신을 둘러싸고 있는 가장 안쪽 블록의 최상위 요소로 존재. 아무런 값을 만들지 않음
  - kotlin에서는 for, while, do/while을 제외한 대부분의 제어 구조가 "식" 이다. 스칼라와 유사. 다음이 가능
    ```kotlin
    val x = if (myBoolean) 3 else 5
    val direction = when (inputString) {
      "u" -> UP
      "d" -> DOWN
      else -> UNKNOWN
    }
    val number = try {
        inputString.toInt()
    } catch (nfe: NumberFormatException) {
        -1
    }
    ```
  - kotlin에서는 대입은 항상 문(값을 반환하지 않는다는 뜻). 따라서 이런 코드는 성립하지 않음
    - `val alsoNumber = i = getNumber()`

- **블록 본문 함수 vs 식 본문 함수**
  - 블록 본문 함수
    ```kotlin
    fun max(a: Int, b: Int): Int {
        return if (a > b) a else b
    }
    ```
  - 식 본문 함수: 굳이 사용자가 반환 타입을 적지 않아도 컴파일러가 분석해서 식의 결과 타입을 함수 반환 타입으로 정함 (타입 추론)
    ```kotlin
    fun max(a: Int, b: Int): Int = if (a > b) a else b
    ```

- **val**
  - val 키워드를 통해 선언하자. 반드시 필요한 변경에만 var : 그래야 함수형 장점 살림
  - 참조가 가리키는 객체 내부의 값은 변경될 수 있음 (java final)
  - var도 타입은 못바꿈

- **문자열 템플릿**
  - `${variableName} ${object.callMethod()}` string interpolation 스칼라와 유사

### 2.2 행동과 데이터 캡슐화: 클래스와 프로퍼티
- **프로퍼티**
  ```kotlin
  class Person(
      val name: String,       // RO 프로퍼티, 공개 getter 만듦
      var isStudent: Boolean  // RW 프로퍼티, 공개 getter/setter 만듦
  )
  ```
  
- **디렉터리와 패키지**
  - 스칼라가 하나의 파일 안에 class/object 등을 넣듯, 코틀린도 package 파일에 클래스, 함수, 프로퍼티 선언 가능
  - 같은 패키지에 속해 있다면 다른 파일에서 정의한 선언이여도 직접 사용 가능.
    - import를 통해 불러오면 됨

### 2.3 선택 표현과 처리: enum과 when
- **enum & when**
  - 코틀린에서는 enum이 soft keyword. `enum class`라고 지칭해야 특별한 의미. 다른 곳에서는 일반적인 이름으로 사용 가능
  - when으로 Enum을 다루기 좋음 (scala의 case match)
  - when의 대상을 when 식의 본문으로 영역에 제한 시킨 변수로 할당 가능
    ```kotlin
    fun getWarmFromSensor() = 
      when (val color = measureColor()) {
          RED, ORANGE -> "good (red = ${color.name})"
          GRREN -> "neutral (green = ${color.g})"
      }
    ```

- **스마트 캐스트: 타입 검사 + 타입 캐스트 조합**
  - 어떤 변수의 타입을 확인한 다음 그 타입에 속한 멤버에 접근하기 위해 명시적으로 변수 타입 변환하지 않아도 됨
  - 컴파일러가 타입을 대신 변환해줌 (스마트 캐스트)
  - 중위 표현식을 이렇게 멋진 코드로 표현 가능 (SUM, NUM)
    ```kotlin
    fun eval(e: Expr) : Int =
        when (e) {
            is Num -> e.value
            is Sum -> eval(e.right) + eval(e.left)
            else -> throw IllegalArgumentException()
        }
    ```

### 2.4 대상 이터레이션: while과 for 루프
- **루프**
  - (for int i=0; i<10; i++) 이런 거 없음
  - 1..10 으로 표현
  - `for (i in 1..100)`
  - `for (i in 100 downTo 1 step 2)`
  - `for (x in 0 ..< size)` : 마지막 원소 제외
  - `for ((index, element) in list.withIndex())`: 인덱스와 함께 컬렉션 순회

### 2.5 코틀린에서 예외 던지고 잡아내기
- **예외**
  - new 키워드 코틀린에서 없어
  - 자바와 달리 코틀린의 throw는 식이므로 다른 식에 포함될 수 있음
    - 평가 결과만드는 코드 조각. 타 식의 일부이자, 변수로 할당도 가능
  - 최신 JVM 언어와 같이 코틀린은 체크 예외와 언체크 예외를 구별하지 않음
    - 스칼라 역시 체크/언체크 예외를 구분하지 않음 (메서드 시그니처 없다는 것)
      - Try, Either를 통한 타입으로 오류를 표현하는 방식을 사용
    - 자바 lombok에서는 `@SneakyThrows`로 불편함을 개선
      - 컴파일러 속여 체크 예외를 언체크 예외처럼 던짐

- **try**
  - 내부에 여러 문장이 있으면 마지막 식이 전체 결과 값
