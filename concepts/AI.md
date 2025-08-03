# AI

## Claude with the Anthropic API
*참고: https://anthropic.skilljar.com/claude-with-the-anthropic-api/*
### Accessing Claude with the API
- **Accessing the API**
  1. Request to Server
     - Client에서 직접 API 호출하지 말고, 서버 통해서 호출하세요
  2. Request to Anthropic API
     - 앤트로픽 SDK 등을 활용해서 요청하세요
       - API Key, Model, Message, Max Token 파라미터로 전달
  3. Model Processing
     - Text Generation Process
       - Tokenization
       - Embedding: list of numbers
       - Contextualization: Embedding 기반으로 확률 계산
       - Generation: 높은 확률로 그 다음 단어 뭐가 나올지 Output Layer
  4. Response to Server
     - Message, Usage, Stop Reason을 반환

- **API context**
  - context를 유지하기 위해서는 코드에서 수동으로 메시지를 저장해야한다. follow-up question 하기 위해서는 준 메시지 다 필요해

- **System Prompt**
  - Style/Tone을 조정하여 클로드의 답변 조정
  - ex) 수학 튜터 역할을 맡기고 싶다면
    - you are a patient math tutor. Do not directly answer a student's questions. Guide them to a solution step by step.

- **Temperature**
  - Each token being selected -> 그 다음 단어 선택될 확률
  - temperature (0~1 사이 값) 으로 어떤 토큰을 선택할지 조절할 수 있음
    - 확률의 분포를 조정한다
    - `0`: 가장 높은 확률의 token이 선택될 확률이 100%로 올라감 (deterministic)
    - `1`: 확률의 분포가 고만고만해짐
  - ![](../images/2025-08-03-temperature.png)

- **Model Output 조정**
  - assistant 메시지에 특정한 문장을 넣어, 마치 모델이 이미 해당 답변을 제공한것 처럼 조작해 모델의 답변 선호도를 조절할 수 있음
  - `stop_sequence`를 통해서 특정 문자열이 나오면 멈추도록 제어 가능

- **Structured data**
  - 딱 구조화된 응답을 받고 싶다면, 위의 assistant + stop_sequence를 응용할 수 있음
  - `add_assistant_message(messages, "```json")`
    - 클로드가 생각하기에 어머! 나 벌써 json 마크다운 응답 시작했구나? 그냥 json부터 뱉어야지
  - `chat(stop_sequences=["```"])`
    - 마크다운 끝낼때 나오는 사인 나오면 응답 중지!
  - 이렇게 많은 형식을 구조화하여 출력 가능

### Prompt Evaluation
- **개요**
  - Prompt Engineering: improve prompt
  - Prompt Evaluation: Getting objective metric that prompt is effective
  - 측정 가능한 것이 뭔지 먼저 알고 (Evaluation), 최적화 (Engineering) 로 나아가자
    - Evaluation Pipeline을 태워서 해당 프롬프트를 점수화하고, 반복하자

- **Evaluation Workflow**
  - 다양한 방식이 있음. 많은 오픈소스 워크 플로우가 있음
  - workflow가 어떻게 동작하는지 알고, 대단한 규모가 필요한 일은 아님
  - 방식
    1. Draft a Prompt
    2. Create an Eval Dataset
    3. Feed Through Claude
    4. Feed Through a Grader
    5. Change Prompt and Repeat
  - ![](../images/2025-08-03-Evaluation.png)

- **Evaluation Criteria**
  - Format: 어떤 형식만을 반환해야할지 검증
  - Valid Syntax: Python/JSON/Regex가 문법이 맞는지?
    - Code로 직접 검증 가능
  - Task Following: 정확한 요구사항을 맞춘 결과물인지?
    - Model API 호출하여 자체 검증을 하는것이 빠름
