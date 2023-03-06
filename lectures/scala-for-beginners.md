# Scala 2 for Beginners
*참고: https://rockthejvm.com/courses/1462300*

## The Absolute Basic
### Expressions
- **개요**
  - Everything in scala is an Expression
    - IF는 Expression
    - Code Block도 Expression

- **Expressions vs Instructions**
  - Instruction: 실행되는 것 (Java) - do sth
  - Expressions: 평가되는 것 (Scala) - give me the value of sth

- **Side Effect**
  - 함수의 리턴값이 아닌 값에 대한 상태를 변화시키는 것을 의미함
    - 변수 조작, 파일/DB 읽기, 콘솔에 출력하기 등등을 의미함 (주로 Unit 반환)
  - 함수형 프로그래밍에서 프로그램이 어떻게 돌아가는지 추론을 어렵게 만들기에 권장되지 않음
  - 함수형 프로그램에서는 함수의 행위가 오로지 input에 대해서만 영향을 받아야함
  - 사이드 이펙트가 발생해야하는 경우가 있음 ex) 데이터베이스에 읽기/쓰기
    - 굉장히 작은, 잘 정제된 코드 부분에서 접근하도록 해야하며, 프로그램 전체에 영향을 미치지 않도록 해야함
    - monad를 사용하여 많은 라이브러리들이 이를 캡슐화하도록 지원하고 있음
    - purely functional 하도록 유도

### Functions
- 함수 실행은 Expression 평가와 같다
- 파라미터가 없다면 그냥 함수 이름만 써서 실행시킬 수 있음
- **반복문이 필요하다면, 재귀함수를 쓰세요!**

### Type Inference
- 컴파일러는 우리가 빠뜨린 자료형의 타입을 알아서 써줘
- 컴파일러는 우리가 빠뜨린 함수의 반환 타입을 알아서 써줘
- 대신 재귀함수를 쓸 때는 함수의 반환 타입을 알려주세요 => 모를 수 있거든요

### Recursion
- 반복문이 필요하다면 꼬리 재귀(tailrec)을 사용하세요!!
- **tailrec**
  - 재귀를 써도 스택 오버플로우가 안 터지는 방법
  - 꼬리 재귀를 쓰면 새로운 스택 위에 쌓지 않아
    - don't need to save intermediate result
    - evaluated stack frame => current stack frame (No need for extra stack frame)
  - 꼬리 재귀가 되려면 재귀 함수를 마지막 expression으로 사용하세요!!!!
  ````scala
  def factorial(n: Int): Int = {
    def factHelper(x: Int, accumulator: Int): Int =
      if (x <= 1) accumulator
      else factHelper(x - 1, x * accumulator)
    
    factHelper(n, 1)
  }
  ````

### Call By Name & Call By Value
- **Call By Value**
  - 파라미터로 넘어가는 "값" 그 자체!
  - 그 값을 아무리 호출해도 넘겨받은 값을 사용하게 됨
  - 파라미터로 넘길 때 값을 평가해서 "값"을 줌

- **Call By Name**
  - 파라미터로 넘어가는 "Expression"
  - 해당 "Expression"을 호출할 때마다 평가된다!
  - 파라미터로 넘길 때 호출할 "Expression"을 넘겨줌
    - 따라서 호출이 되어야 평가를 하고 값을 반환함

```scala
def calledByValue(x: Long): Unit = {
  println("by value: " + x)
  println("by value: " + x)
}

def calledByName(x: => Long): Unit = {
  println("by name: " + x)
  println("by name: " + x)
}

calledByValue(System.nanoTime())
calledByName(System.nanoTime())

/*
* by value: 12345
* by value: 12345
* by name: 12378
* by name: 12401
* */
```

### Default and Named Arguments
- 파라미터에 이름 붙이고, default value를 줄 수 있음
- 함수 호출시 `파리미터 이름 = 값` 형식으로 쓰자!

### String Operations and Interpolations
- **S-Interpolations**
  ```scala
  val name = "David"
  val age = 12
  val greeting = s"Hello, my name is $name and I am $age years old"
  val anotherGreeting = s"Hello, my name is $name and I will be turning ${age + 1} years old"
  println(anotherGreeting)
  ```

- **F-Interpolations**
  ```scala
  val speed = 1.2f
  val myth = f"Eat with $speed%2.2f burgers with minute"
  println(myth)
  ```

- **Raw-Interpolations**
```scala
println(raw"This is a \n newline")
/*
* This is a \n newline
* */

val escaped = "This is a \n newline"
println(raw"$escaped")
/*
* This is a
*  newline
* */
```
