### React

#### 1. 리액트란?
- **리액트는 라이브러리!**
  - 리액트는 전적으로 UI 렌더링하는데에 관여
  - 여러 라이브러리 기능 중 채택해서 사용
    - 화면 라우팅은 react-router-dom
    - 상태관리는 redux, mobx
    - 빌드는 webpack, npm
    - 테스팅은 Eslint, Mocha

- **컴포넌트**
  - 클래스형 컴포넌트
    - 클래식한 방법
    ```js
    class App extends Component {
        render() {
            return <h1>안녕!</h1>;
        }
    }
    ```
  - 함수형 컴포넌트
    - React-Hooks 발표된 이후 요즘은 이걸 더 많이 써
    ```js
    function App() {
        return <h1>안녕!</h1>;
    }
    ```

- **브라우저가 그려지는 원리**
  - 스텝 프로세스
    1. HTML 파싱 -> DOM 트리 생성
    2. CSS 파싱 -> CSSOM 트리 생성
    3. RenderTree(DOM + CSSOM) 만들어짐
    4. RenderTree 그리기
  - DOM이 인터랙션에 의해 변화하면 모든 스타일의 요소들이 다시 그려짐
    - 맨날 DOM 바뀔수도!

- **VirtualDOM**
  - 실제 DOM을 메모리에 복사해두고 (snapshot)
  - 바뀐 부분만 실제 DOM 바꿔치기 해주는 기법!

- **React가 그리는 VirtualDOM**
  1. JSX 렌더링 -> VirtualDOM 업데이트
  2. VirtualDOM 스냅샷과 비교
  3. VirtualDOM 바뀐 부분 RealDOM에서 갈아 끼우기

- **Webpack**
  - 자바스크립트 코드 압축 & 최적화 -> 네트워크 로딩 비용 감소
  - 모듈 단위 개발로 유지보수 up
  - 모듈화로 개발 --- webpack ---> js 압축/최적화본 뚝딱 등장

- **Babel**
  - 구형 브라우저에서 돌아갈 수 있도록 js 문법 포팅

- **npx**
  - npx create-react-app 으로 리액트 설치하는데
  - npx: 노드 패키지 실행을 도와주는 도구... npm 레지스트리에 있는 패키지 가져와서 설치

- **JSX**
  - JSX: 자바스크립트 확장 문법
    - UI가 보이는 모습을 이걸로 써주세요!
  - 원래 리액트에서 화면 그리려면...
    - `ReactDOM.render(React.createElement('h1', {}, 'hello'), document.getElementById('root'))`
  - JSX를 통해 html 태그 마냥 쓱싹 마크업하고 이를 리액트가 바꿔주도록 쓱 던져주자
    - 대신 필수적으로 부모요소 하나로 감사줘야해! `<div></div>`

#### 2. 리액트 기초
- **map()**
  - 리스트 하나하나 어떻게 해주세요~ 는 map()으로 처리합시다

- **JSX key**
  - 리액트에서 리스트 요소 나열시 Key를 꼭 넣어주세요
  - 변경/추가/제거시 항목 식별에 도움을 줍니다
  - 가상돔에서 갈아 끼워서 실제돔 만들자나요? 이때 Key를 기반으로 인식합니다
  - unique한 값으로 넣어줘야 불필요한 렌더링 최소화할 수 있어요

- **filter()**
  - 새로운 리스트 만들어 줄 수 있도록 조건을 filter()에 넣어서 휘뚜루 마뚜루
  - 함수형 프로그래밍 처럼 휘뚜루 마뚜루

- **React State**
  - 데이터가 변했을 때 렌더링 다시해주려면 **React State** 사용해주세요
    - state는 변경되면 리렌더링이 수행됨
    - state는 컴포넌트가 관리
  ```js
  state = {
      data: [
          {
              id: 1,
              title: "title1"
          },
          {
            id: 2,
            title: "title2"
          },
      ]
  }
  this.setState( {data: newData} )
  ```

- **Spread Operator**
  - 배열
  ```js
  const a1 = [1, 2, 3]
  const a2 = [4, 5, 6]
  const a3 = [7, 8, 9]
  const total = [...a1, ...a2, ...a3]
  
  console.log(total); // [1, 2, 3, 4, 5, 6, 7, 8, 9]
  ```
  - 객체
  ```js
  const obj1 = {
    a: 'A',
    b: 'B'
  }
  const obj2 = {
    c: 'C',
    d: 'D'
  }
  const total = { ...obj1, ...obj2 }
  
  console.log(total) 
  /*
  * {
  *   a: 'A',
  *   b: 'B',
  *   c: 'C',
  *   d: 'D'
  * }
  * */
  ```

- **React Hooks**
  - class 없이 state를 사용할 수 있는 새로운 기능
    - React Hooks 이전까지는 리액트의 생명주기를 Functional Component에서 쓰지 못했음
      - 생명주기
        - Mounting: componentDidMount()
        - Updating: componentDidUpdate()
        - Unmounting: componentWillUnmount()
    - 함수형 컴포넌트에서도 생명주기를 사용할 수 있게되었다!
      - useEffect만 있으면 생명주기를 위에 component~뭐시꺵이 다 사용할 수 있어!
  - 커스텀 훅을 만들어 코드 중복을 방지할 수도 있음

- **State & Props**
  - State
    - 해당 컴포넌트 내에서 데이터를 조작
    - 변경 가능
    - 변하면 re-render
  - Props
    - 부모 컴포넌트로 부터 받은 데이터
    - 읽기 전용
    - 부모 컴포넌트에서 setter 역시 전달받아 이를 호출하는 방식

- **구조 분해 할당**
  - 객체
  ```js
  let person = {
    name: 'Joel',
    age: 27,
    phone: "01012341234",
    address: {
      code: "123",
      street: "st"
    }
  }
  
  let {address: {code, street}} = person
  ```
  - 배열
  ```js
  const numbers = [1, 2, 3, 4, 5, 6]
  
  const [,,three, five] = numbers
  ```

- **JS 자료구조 불변성**
  - 원시타입: Boolean, String, Number, null, undefined, Symbol
  - 참조타입: Object, Array
    - 깊은 복사로 처리하자!
    - 새로운 배열을 반환하도록!
    - 원본데이터 변경하는 메서드: splice, push

- **React.memo**
  - 렌더링 최적화
  - 렌더링 안해도 될 컴포넌트는 스킵할 수 있도록!

- **useCallback**
  - 컴포넌트 재렌더링 되면 다시 함수를 만드는게 일반적...
  - 근데 그렇게 하지 말고 우리 useCallback 쓰면 최초 렌더링 시에만 함수가 생성될 수 있어

#### 3. 리액트 심화
