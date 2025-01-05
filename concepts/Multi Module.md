## Multi Module

### 멀티모듈 분리 기준
- **필요한 이유**
  - 코드 재사용성, 빌드 효율성, 팀 협업을 위함
  - 프로젝트 규모/조직/도메인에 따라 분리할 것

- **모듈 분리 기준**
  1. 도메인 기준: DDD 적용 시
  2. 계층(레이어) 또는 공통 로직 기준
     - 공통 로직: common/core/shared 와 같은 이름으로 공통 라이브러리로 분리
     - 서비스 레이어/레포 레이어 등 계층 구조 명확하다면 계층변로 분리하기도 함
  3. 기술 스택별 구분

- **언제 쓸 것인가?**
  1. 프로젝트 규모 커지고, 빌드/배포/협업 복잡한 경우
  2. 특정 부분의 재사용성/독립성 필요
     - auth, logging, messaging 등 공통 관심사 별도 모듈로 추출

- **주의**
  1. 과도하게 분리하지 말 것
  2. 의존 방향은 명확할 것 (순환 의존 X)
  3. 버전 충돌 관리할 것

### SBT로 멀티모듈을 구성하는 법
1. 기본구조
   ```
   root/
   ├── project/
   │    ├── build.properties
   │    └── plugins.sbt
   ├── build.sbt                    // 전체(루트) 프로젝트의 설정
   ├── moduleA/
   │    ├── project/
   │    │    ├── build.properties
   │    │    └── plugins.sbt
   │    └── build.sbt               // 서브 프로젝트 A
   ├── moduleB/
   │    ├── project/
   │    │    ├── build.properties
   │    │    └── plugins.sbt
   │    └── build.sbt               // 서브 프로젝트 B
   └── moduleC/
       ├── project/
       │    ├── build.properties
       │    └── plugins.sbt
       └── build.sbt               // 서브 프로젝트 C
   ```
    - root: 멀티모듈을 통합하는 상위 관점의 빌드 스크립트
    - project: SBT 프로젝트
    - moduleX: 별도의 `build.sbt`를 가진 서브 프로젝트들

2. root `build.sbt` 구성
- 각 서브 프로젝트를 `lazy val`로 정의
- `aggregate`, `dependsOn`을 통한 관계 설정
   ```sbt
   lazy val moduleA = (project in file("moduleA"))
           .settings(
              name := "moduleA",
              scalaVersion := "2.13.8"
              // 그 외 설정
           )
   
   lazy val moduleB = (project in file("moduleA"))
           .settings(
              name := "moduleB",
              scalaVersion := "2.13.8"
              // 그 외 설정
           )
           .dependsOn(moduleA) // moduleA 사용해야 하는 경우
   
   lazy val root = (project in file("."))
           .aggregate(moduleA, moduleB)
           .settings(
              name := "rootProject",
              scalaVersion := "2.13.8"
              // 그 외 설정
           )
   ```

3. Play로 멀티모듈 나누기
- **폴더 구조**
   ```
   root/
    ├── project/
    │    ├── build.properties
    │    └── plugins.sbt
    ├── build.sbt                    // 루트 및 서브 프로젝트 선언
    ├── app1/
    │    ├── app/                    // Play Controller, Model, View 등
    │    └── build.sbt               // Play 모듈1
    ├── app2/
    │    ├── app/
    │    └── build.sbt               // Play 모듈2
    └── common/
         ├── src/main/scala/
         └── build.sbt               // 공통 로직 모듈
   ```

- **`build.sbt`**
   - 일반적으로 `play-sbt-plugin`을 사용
     - play 어플리케이션을 빌드/실행할 수 있도록 여러 설정과 작업을 제함
   ```sbt
   import sbt._
   import Keys._
   import play.sbt.PlayScala
   
   lazy val common = (project in file("common"))
           .settings(
              name := "common",
              scalaVersion := "2.13.8",
              libraryDependencies ++= Seq(
                 // 공통 라이브러리
              )
           )
   
   lazy val app1 = (project in file("app1"))
           .enablePlugins(PlayScala)   // Play 플러그인 적용
           .dependsOn(common)          // common 모듈 의존
           .settings(
              name := "app1",
              scalaVersion := "2.13.8",
              libraryDependencies ++= Seq(
                 // 필요한 Play 관련 라이브러리
              )
           )
   
   lazy val app2 = (project in file("app2"))
           .enablePlugins(PlayScala)
           .dependsOn(common)
           .settings(
              name := "app2",
              scalaVersion := "2.13.8"
           )
   
   lazy val root = (project in file("."))
           .aggregate(common, app1, app2)    // 지정된 모든 서브 프로젝트 대상 컴파일/테스트 동작
           .settings(
              name := "rootProject",
              scalaVersion := "2.13.8"
           )
   ```
