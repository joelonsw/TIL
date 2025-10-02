## Kotlin In Action - ch3. 함수 정의와 호출
### 3.1 코틀린에서 컬렉션 만들기
- **선언 방법 및 생성 Java Collection**
  - 불변)
    - `listOf`: `java.util.Arrays.ArrayList` (크기 변경 불가)
    - `setOf`: `java.util.LinkedHashSet` (RO)
    - `mapOf`: `java.util.LinkedHashMap` (RO)
  - 가변)
    - `mutableListOf`: `java.util.ArrayList`
    - `mutableSetOf`: `java.util` (RW)
    - `mutableMapOf`: `java.util` (RW)

### 3.2 함수를 호출하기 쉽게 만들기
- **편의 기능**
  - toString을 기본으로 제공
  - 인자를 이름 붙여서 제공할 수 있음 (스칼라와 같이)
  - 코틀린에서는 함수 선언에서 파라미터 기본값을 지정할 수 있어 오버로드 중 상당수 피할 수 있음
  - 함수 디폴트 파라미터는 함수 호출하는 쪽이 아닌, 함수 선언 쪽에 인코딩
    - 함수를 호출하는 코드 중 값을 지정하지 않은 모든 인자는 자동으로 바뀐 기본값 적용
  - 스칼라와 같이 코틀린에서도 하나의 파일에 여러 클래스, 인터페이스 정의 가능

### 3.3 메서드를 다른 클래스에 추가: 확장 함수와 확장 프로퍼티
- **확장 함수**
  - 클래스의 멤버 메서드인 것 처럼 호출할 수 있지만, 그 클래스 밖에 선언된 함수
  - 하지만, 캡슐화를 깬 private/protected 멤버 사용은 못함
  - 내부적으로 수신 객체를 첫번째 인자로 받는 정적 메서드
  - `char c = StringUtilKt.lastChar("Java")`

- **확장 프로퍼티**
  - 클래스의 멤버 변수인것 처럼 호출하지만, 그 클래스 밖에 선언됨
  - `get()`이 필수. Backing Field (프로퍼티의 값을 실제로 저장하는 보이지 않는 변수) 가 없기 때문
  - 이미 컴파일된 String 클래스에 특정한 저장공간을 추가할 수 없어.
  - 따라서 `get()`을 통해 이 값을 요청하면, 이 로직을 실행하여 계산해라 지시

- **예시**
    ```kotlin
    fun String.lastChar(): Char = this[this.length - 1]
    fun String.lastChar: Char
        get() = this[this.length - 1]
          
    // 에러 -> 애초에 저장할 공간이 없구나. String 객체 자체에 해당 값을. 그냥 참조같이 가져와서 쓰는 방법 뿐
    fun String.lastChar = this[this.length - 1]
        
    fun main {
        val name = "Kotlin"
        println(name.lastChar()) // n
        println(name.lastChar) // n
    }
    ```

### 3.4 컬렉션 처리: 가변 길이 인자, 중위 함수 호출, 라이브러리 지원
- **중위 함수**
  - infix 예약어를 통해 함수를 선언하면 중위 호출에 사용할 수 있음
  - `infix fun Any.to(other: Any) = Pair(this, other)`

- **구조 분해할당**
  - `for((index, element) in collection.withIndex())`

### 3.5 문자열과 정규식 다루기
- **문자열 나누기**
  - regex를 통해 나눌 수 있고, 문자 자체를 줘서 이를 기반으로 나눌 수 있음
  - ` 3개를 가지고 멀티라인 String 표현 가능

### 3.6 코드 깔끔하게 다듬기: 로컬 함수와 확장
- **로컬 함수**
  - 함수 내부에 함수를 선언할 수 있음 (스칼라 처럼)
  - 한단계 정도만 내포해주세요