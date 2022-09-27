## Reactor
- *참고: https://tech.kakao.com/2018/05/29/reactor-programming/*

### Mono & Flux
- **Mono**
  - 0-1개의 결과만을 처리하는 Reactor의 객체

- **Flux**
  - 0-N개의 결과를 처리하는 Reactor의 객체

- **특징**
  - Reactive Stream의 Publisher 인터페이스를 구현
  - Reactor에서 제공하는 풍부한 연산자들의 조합을 통해 스트림 표현 가능
    - Flux --(reduce)--> Mono
    - Mono --(flatMapMany)--> Flux

### 내가 쓰고 있는 Reactor 메서드
- **block()**
    ```java
    Mono<TokenHistoriesResponse> request =
            kasWebClient.getForObject(url, TokenHistoriesResponse.class);
    return request.block();
    ```

- **subscribe()**
    ```java
    for (String contractAddress : contractAddresses) {
        Mono<TokensResponse> tokensResponseMono =
                findTokensOwnedByUser(contractAddress, userKlaytnAddress);
        tokensResponseMono.subscribe(
                tokensResponse -> {
                    tokensResponses.put(contractAddress, tokensResponse);
                    countDownLatch.countDown();
                });
    }
    ```
  

