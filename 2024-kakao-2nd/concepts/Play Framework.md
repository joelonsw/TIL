## Play Framework 공식문서
*참고: https://www.playframework.com/documentation/2.8.x/Home*

#### Configuration API
- Typesafe config library를 사용하나, `Configuration` 이라는 스칼라 래퍼를 사용
  - `application.conf` 파일에 설정된 값들을 가져올 수 있음 
  - https://www.playframework.com/documentation/2.8.x/ConfigFile

#### Actions, Controllers and Results
- **Action**
  - `play.api.mvc.Action` == `(play.api.mvc.Request => play.api.mvc.Result)`
- **Controller**
  - Play에서 컨트롤러는 그저 Action 생성기

#### HTTP routing
- 들어오는 HTTP 요청을 Action으로 변경시켜주는 역할
- DI
  - 플레이의 기본 라우터 `@Inject` 어노테이션이 붙은 컨트롤러 클래스 인스턴스를 받음

#### Dependency Injection
*참고: https://www.playframework.com/documentation/2.8.x/ScalaDependencyInjection*  
- **개요**
  - Dependency Graph가 생성되고, 연결되고, 검증되고
  - Guice 사용해 구현

- **왜 쓰는가?**
  1. 쉽게 연결하여 같은 컴포넌트를 가진 다른 로직을 구현할 수 있음
  2. 전역 static 상태를 방지함.

- **어떻게 동작하는가**
  - Guice와 타 런타임 DI 프레임워크
  - GuiceApplicationLoader 사용

- **Component Lifecycle**
  - Singleton으로 마킹해두지 않는 이상, 새로운 인스턴스가 컴포넌트 필요시마다 생성됨
  - 인스턴스는 필요할때 lazy creation
    - Eager binding으로 생성도 가능
  - Components는 아무데서도 참조 안되면 GC의 대상이 될 것 (프레임워크에선 아무것도 안해줌)
    - ApplicationLifecycle을 제공해주는데, 해당 것으로 어플리케이션 스탑시 셧다운 할 것 지정가능

- **Stopping/Cleaning up**
  - Play 어플리케이션 사라질때 메모리에서도 사라지게! (GC에서 없애주세요오)
    ```scala
    import scala.concurrent.Future
    import javax.inject._
    import play.api.inject.ApplicationLifecycle
    
    @Singleton
    class MessageQueueConnection @Inject() (lifecycle: ApplicationLifecycle) {
        val connection = connectToMessageQueue()
        lifecycle.addStopHook { () =>
            Future.successful(connection.stop())
        }
    
        // ...
    }
    ```

#### Server Backends
*참고: https://www.playframework.com/documentation/2.8.x/Server*
*참고: https://www.playframework.com/documentation/2.8.x/AkkaHttpServer*
*참고: https://www.playframework.com/documentation/2.8.x/NettyServer*
- **개요**
  - 2개의 configurable server backend를 구성해서 줌
  - 로우 레벨의 HTTP 처리를 담당
  - Akka HTTP (2.6.x 이상)
  - Netty (2.6.x 미만)

- **Akka HTTP Server**
  - Akka Streams를 사용해서 구현
  - Play의 서버 백엔드는 [low level server API](https://doc.akka.io/docs/akka-http/current/server-side/low-level-api.html?language=scala) 사용하여 `HttpRequest` / `HttpResponse`를 다룸
  - Play의 서버는 Akka의 `HttpRequest`를 Play HTTP 요청으로 변경함
  - Play 처럼 Akka HTTP는 넌블러킹
    - 작은 갯수의 쓰레드로 많은 처리 가능
  - JDBC, HTTPURLConnection 등의 블락킹 연산이 문제
    - 해당 블럭킹 연산을 처리할 때는 메인 렌더링 쓰레드랑 무관한 친구를 사용해주세요
    - `Future`, `CompletionStage`, `CustomExecutionContext`로 커스텀 쓰레드 풀을 써보세용
