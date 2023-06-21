### Akka

## 액터 모델
*참고: https://blog.rajephon.dev/2018/11/25/akka-00/*
*참고: https://velog.io/@wansook0316/Actor-Model*
- **개요**
  - 멀티 코어 프로세서로 발전하는 컴퓨터... 물리적 환경에 맞춰 최대한 성능을 낼 수 있는 코드를 짜자!
  - 멀티 쓰레드 프로그래밍은 많은 문제에 봉착
    1. 공유 리소스 접근: heap 영역 race condition
    2. Lock 처리 통한 임계 영역 처리: 어려워! 힘들어!
    
- **Lock의 문제**
  1. Concurrency 제한: Thread 일시 정지 & 복원 => OS에서 비싼 작업
  2. Block된 Thread에서 유의미한 작업 X
  3. Deadlock 유발 가능

- **액터 모델**
  - ![](../images/2023-06-20-Actor-model.png)
  - 모든 것은 액터다 (Everything is an actor)
  - 액터 모델은 본질적으로 동시성을 제공
  - 액터는 비동기적으로 메시지를 처리할 수 있는 Computational Entity...
    - 다른 액터에게 유한한 갯수의 메시지를 보낼 수 있음
    - 유한한 갯수의 새로운 액터를 만들 수 있음
    - 다른 액터가 받을 메시지에 수반될 행동을 지정할 수 있음
  - 액터가 차지하는 메모리 공간은 독립적
    - 다른 쓰레드나 액터가 접근할 수 없음!
    - 메모리 공유 없이 "메시지 전달"만을 사용하기에 공유 메모리의 교착 상태 등 뇌절 상황 미연에 방지

- **액터 모델의 목표**
  1. lock에 의존하지 않고 캡슐화를 통해 동기화 문제를 해결
  2. Cooperative Entity 모델 사용: 전체 앱이 서로에게 시그널을 보내고 값을 변경하면서 동작
  3. 우리가 당연하게 생각하는 방식(사람이 서로 말하듯) 으로 처리

- **액터 모델의 기본 구조**
  - [액터 구조]
    - Mailbox: Queue
    - Message
    - Behavior: Message에 따른 행동 결정 및 실행
      - 본인의 상태 변경
      - Child Actor 생성/제거
      - 타 Actor에게 메시지 전송
    - State: Actor의 실행 상태(init, ready, closed) - 자신만 변경 가능
  - [메시지 전달 방식]
    - Lock, Blocking X
    - 특정 메서드 호출이 아닌, 특정 액터에게 메시지 전달!
    - 메시지 전달 != Thread 실행
    - 각 액터는 독립적으로 받은 메시지 수행

- **액터 모델의 효용**
  1. Lock이 필요 없음 => Actor는 독립적으로 queue를 가짐
  2. Actor의 상태값은 해당 객체가 가진 Queue로 부터 넘어오는 동작으로만 처리됨 => 동시성 문제 해결 

## Akka의 동작 방식
- **질문 사항**
  - 어떻게 메시지의 순서를 보장할 수 있는가?
  - Race Condition을 일으키지는 않는가?
  - "Async"로 액터가 동작한다는게 무슨뜻인가?
  - 어떻게 아카 액터가 동작하는 건가?

- **Akka의 동작 방식**
  - Akka는 액터들끼리 공유하는 __쓰레드 풀__ 있어요
    - 액터는 사실 그저 데이터 구조일 뿐이에요!
      - 메시지 큐와 메시지 핸들러가 있고
      - 메시지 큐에서 그냥 하나씩 꺼내서 처리하는 데이터구조!
  - Akka는 액터 실행의 순서를 스케줄링해요
    - 쓰레드 풀에 있는 여러 쓰레드가, 엄청 많은 액터의 일처리를 번갈아가면서 수행하죠
  - [메세지 -> 액터]
    - 메시지가 액터의 메시지큐에 enqueue 됩니다
    - 이는 Thread-safe 하도록 Akka에서 프로세싱 해주고요
  - [액터의 메시지 처리]
    - 쓰레드가 가만히 있던 액터를 처리해줄게~ 라고 다갸ㅏ오면
    - 메시지큐에 있는 메시지 deque
    - 쓰레드가 해당 메시지에 대해 액터의 메시지 핸들러를 실행시키고
    - 쓰레드가 이후에 액터 나중에 또 올게~ 하고 unscheduled
  - [액터는 다음을 보장해요]
    1. 하나의 쓰레드만이 특정 시점에 하나의 액터에 접근하여 필요한 처리를 진행한다
       - 액터는 싱글쓰레드 => 락 필요없음
    2. 메시지 큐를 통해서
       - 메시지는 딱 한번만 메시지큐에 등록되고
       - 메시지의 순서는 메시지큐 덕에 보존된다

## Akka Actor 쓰는 법
- **관심사의 분리**
  - 으레 많은 프레임워크가 그렇듯, 개발자는 비즈니스 로직에만 집중할 수 있도록 도와주고 있다.
  - 액터의 메시지 큐(Mailbox 인 듯)는 akka가 매니징 해주는 듯 하고,
    - typesafe.akka:akka-actor/Dispatch 등을 보면 좀 있는 듯 하다
  - 우리는 Actor를 상속한 객체를 만들고, receive 메서드를 오버라이딩 해주어 메시지 핸들러를 구축해주자!

- **예시**
  ```scala
  class WordCountActor extends Actor {
      private var totalWords = 0
  
      // 요게 메시지 핸들러! PartialFunction으로 구현하자 :)
      override def receive: PartialFunction[Any, Unit] = {
          case message: String => {
              println(s"[WordCountActor] $message")
              totalWords += message.split(" ").length
          }
          case _ => println("[WordCountActor] I don't understand!!")
      }
  }
  ```
  
- **context.become()**
  - 액터는 상태를 가질 수도 있다
  - 싱글 쓰레드고, 한번에 메시지 하나만 처리하니까 상태 있어도 됨, 다만 상태를 가지지 않도록 하는 것이 추천됨
  - 메시지 핸들러를 잘~ 쓰면 상태를 사용하지 않도록 리팩터링 할 수 있음
  - 약간 재귀함수 감성으로다가...
    ```scala
    object Counter {
        case object Increment
  
        case object Decrement
  
        case object Print
    }
  
    class Counter extends Actor {
  
        import Counter._
  
        override def receive: Receive = countReceive(0)
  
        def countReceive(count: Int): Receive = {
            case Increment =>
                println(s"[currentCount] incrementing")
                context.become(countReceive(count + 1))
            case Decrement =>
                println(s"[currentCount] decrementing")
                context.become(countReceive(count - 1))
            case Print =>
                println(s"[currentCount] $count")
        }
    }
    ```

- **Child Actors**
  - `context.actorOf(Props[], "name")` 의 문법으로 액터 안에서 또 다른 액터를 만들 수 있다!
  - 여러개의 child actor들을 관리할 때, 그냥 부모의 상태로 물고 있는 것도 방법이지만, 위의 `context.become()` 등의 트릭으로 휘뚜루 마뚜루 코딩도 가능
  ```scala
  class ParentActor extends Actor {
    override def  receive: Receive = ??? // 초기화 로직
  
    // 이런식으로 매개변수로 상태를 물고있고
    def withChildren(childrens: Seq[ActorRef], currentChildIdx: Int, currentTaskId: Int, requestMap: Map[Int, ActorRef]): Request = {
  
      // context.become을 활용해 전환해주면 더 "비동기적인 스칼라틱한 코드" (가독성이 좋은진 모르겠음)
      context.become(withChildren(/*~~~*/))
    }
  }
  ```

- **Logging**
  1. 명시적으로 logging 선언
     - `val logger = akka.event.Logging(context.system, this)`
  2. trait 상속
     - `with ActorLogging`