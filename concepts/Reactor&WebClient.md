## Reactor & WebClient
- *참고: https://tech.kakao.com/2018/05/29/reactor-programming/*
- *참고: https://happycloud-lee.tistory.com/220*
- *참고: https://alwayspr.tistory.com/44*

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

## WebClient
- **왜 필요한가?**
  - 요청자와 제공자 사이의 통신을 좀 더 효율적인 Non-Blocking 방식으로 하기 위함

- **어떻게 동작하는가? [RestTemplate]**
  - ![](../images/2022-09-27-resttemplate.png)
  - Multi-Thread 와 Blocking 방식 사용
  - Thread-Pool은 요청자 어플리케이션 구동시 미리 만들어 둠
    - Request는 Queue에 쌓이고 가용한 쓰레드가 있으면 그 쓰레드에 할당되어 치리됨
    - 각 쓰레드는 블로킹 방식으로 처리되어 응답 올 때 까지 해당 쓰레드 다른 요청에 할당 x
  - 요청을 처리할 쓰레드가 없다면 Queue에서 대기
    - 여기에서 병목이 발생하면 서비스가 매우 느려짐

- **어떻게 동작하는가 [WebClient]**
  - ![](../images/2022-09-27%20WebClient.jpeg)
  - Single-Thread와 Non-Blocking 방식 사용
    - Core 당 1개의 Thread 이용
  - 각 요청은 Event Loop내에 Job으로 등록
    - Event Loop는 각 Job을 제공자에게 요청한 후, 결과 기다리지 않고 다른 Job 처리
    - 제공자로 부터 callback 응답이 오면, 그 결과를 요청자에게 제공

- **VS RestTemplate**
  - 1000명까지는 비슷하지만, 그 이후에는 WebClient가 압

## 프로젝트 로그 분석
- **테스트 대상 메서드 sendMyToken()**
  - 단일 HTTP 요청
  ```java
  @Test
  void sendToken() throws InterruptedException {
      TransactionResponse transactionResponse =
              kasService.sendMyToken(NEW_CONTRACT_ADDRESS, "0x2", JOEL_KAIKAS);
      System.out.println("transactionResponse.getStatus() = " + transactionResponse.getStatus());
      System.out.println(
              "transactionResponse.getTransactionHash() = "
                      + transactionResponse.getTransactionHash());
  
      Thread.sleep(2000);
  }
  ```

- **로그 sendMyToken()**
```
16:10:52.262 [DEBUG] [Test worker] [o.s.t.c.c.DefaultCacheAwareContextLoaderDelegate] - Retrieved ApplicationContext [34644587] from cache with key [[WebMergedContextConfiguration@5649ec46 testClass = KasServiceTestWithTestnet, locations = '{}', classes = '{class com.backend.connectable.ConnectableApplication}', contextInitializerClasses = '[]', activeProfiles = '{}', propertySourceLocations = '{}', propertySourceProperties = '{org.springframework.boot.test.context.SpringBootTestContextBootstrapper=true}', contextCustomizers = set[org.springframework.boot.test.autoconfigure.actuate.metrics.MetricsExportContextCustomizerFactory$DisableMetricExportContextCustomizer@1ddae9b5, org.springframework.boot.test.autoconfigure.properties.PropertyMappingContextCustomizer@0, org.springframework.boot.test.autoconfigure.web.servlet.WebDriverContextCustomizerFactory$Customizer@f74e835, org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@21d8bcbe, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@24fb6a80, org.springframework.boot.test.mock.mockito.MockitoContextCustomizer@0, org.springframework.boot.test.web.client.TestRestTemplateContextCustomizer@3efe7086, org.springframework.boot.test.web.reactive.server.WebTestClientContextCustomizer@24faea88, org.springframework.boot.test.context.SpringBootTestArgs@1, org.springframework.boot.test.context.SpringBootTestWebEnvironment@16b2bb0c], resourceBasePath = 'src/main/webapp', contextLoader = 'org.springframework.boot.test.context.SpringBootContextLoader', parent = [null]]]
16:10:52.262 [DEBUG] [Test worker] [o.springframework.test.context.cache] - Spring test ApplicationContext cache statistics: [DefaultContextCache@737fbdc2 size = 1, maxSize = 32, parentContextCount = 0, hitCount = 89, missCount = 1]
16:10:52.265 [TRACE] [Test worker] [o.s.w.r.f.client.ExchangeFunctions] - [7fafb60] HTTP POST https://kip17-api.klaytnapi.com/v2/contract/0xa875f3b7e62ea14cde486cfb6f4c3e5926dceedb/token/0x2, headers={masked}
16:10:52.265 [DEBUG] [reactor-http-nio-2] [r.n.r.PooledConnectionProvider] - [92e2fd67, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443] Channel acquired, now: 1 active connections, 0 inactive connections and 0 pending acquire requests.
16:10:52.265 [DEBUG] [reactor-http-nio-2] [r.n.http.client.HttpClientConnect] - [92e2fd67-8, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443] Handler is being applied: {uri=https://kip17-api.klaytnapi.com/v2/contract/0xa875f3b7e62ea14cde486cfb6f4c3e5926dceedb/token/0x2, method=POST}
16:10:52.265 [DEBUG] [reactor-http-nio-2] [r.n.r.DefaultPooledConnectionProvider] - [92e2fd67-8, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443] onStateChange(POST{uri=/v2/contract/0xa875f3b7e62ea14cde486cfb6f4c3e5926dceedb/token/0x2, connection=PooledConnection{channel=[id: 0x92e2fd67, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443]}}, [request_prepared])
16:10:52.268 [TRACE] [reactor-http-nio-2] [o.s.h.codec.json.Jackson2JsonEncoder] - [7fafb60] Encoding [com.backend.connectable.kas.service.token.dto.TokenSendRequest@6b291ff4]
16:10:52.271 [DEBUG] [reactor-http-nio-2] [r.n.r.DefaultPooledConnectionProvider] - [92e2fd67-8, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443] onStateChange(POST{uri=/v2/contract/0xa875f3b7e62ea14cde486cfb6f4c3e5926dceedb/token/0x2, connection=PooledConnection{channel=[id: 0x92e2fd67, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443]}}, [request_sent])
16:10:52.400 [DEBUG] [reactor-http-nio-2] [r.n.http.client.HttpClientOperations] - [92e2fd67-8, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443] Received response (auto-read:false) : [content-type=application/json; charset=utf-8, date=Tue, 27 Sep 2022 07:10:52 GMT, x-envoy-upstream-service-time=98, server=istio-envoy, content-length=109]
16:10:52.400 [DEBUG] [reactor-http-nio-2] [r.n.r.DefaultPooledConnectionProvider] - [92e2fd67-8, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443] onStateChange(POST{uri=/v2/contract/0xa875f3b7e62ea14cde486cfb6f4c3e5926dceedb/token/0x2, connection=PooledConnection{channel=[id: 0x92e2fd67, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443]}}, [response_received])
16:10:52.400 [TRACE] [reactor-http-nio-2] [o.s.w.r.f.client.ExchangeFunctions] - [7fafb60] [92e2fd67-8, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443] Response 200 OK, headers={masked}
16:10:52.401 [DEBUG] [reactor-http-nio-2] [reactor.netty.channel.FluxReceive] - [92e2fd67-8, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443] FluxReceive{pending=0, cancelled=false, inboundDone=false, inboundError=null}: subscribing inbound receiver
16:10:52.401 [DEBUG] [reactor-http-nio-2] [r.n.http.client.HttpClientOperations] - [92e2fd67-8, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443] Received last HTTP packet
16:10:52.401 [TRACE] [reactor-http-nio-2] [r.netty.channel.ChannelOperations] - [92e2fd67, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443] Disposing ChannelOperation from a channel

16:10:52.402 [TRACE] [reactor-http-nio-2] [o.s.h.codec.json.Jackson2JsonDecoder] - [7fafb60] [92e2fd67-8, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443] Decoded [com.backend.connectable.kas.service.common.dto.TransactionResponse@7943d672]
16:10:52.402 [DEBUG] [reactor-http-nio-2] [r.n.r.DefaultPooledConnectionProvider] - [92e2fd67, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443] onStateChange(POST{uri=/v2/contract/0xa875f3b7e62ea14cde486cfb6f4c3e5926dceedb/token/0x2, connection=PooledConnection{channel=[id: 0x92e2fd67, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443]}}, [response_completed])
16:10:52.402 [DEBUG] [reactor-http-nio-2] [r.n.r.DefaultPooledConnectionProvider] - [92e2fd67, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443] onStateChange(POST{uri=/v2/contract/0xa875f3b7e62ea14cde486cfb6f4c3e5926dceedb/token/0x2, connection=PooledConnection{channel=[id: 0x92e2fd67, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443]}}, [disconnecting])
16:10:52.402 [DEBUG] [reactor-http-nio-2] [r.n.r.DefaultPooledConnectionProvider] - [92e2fd67, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443] Releasing channel
16:10:52.402 [DEBUG] [reactor-http-nio-2] [r.n.r.PooledConnectionProvider] - [92e2fd67, L:/10.64.154.214:63793 - R:kip17-api.klaytnapi.com/13.125.50.215:443] Channel cleaned, now: 0 active connections, 1 inactive connections and 0 pending acquire requests.
transactionResponse.getStatus() = Submitted
transactionResponse.getTransactionHash() = 0x8e94cd81906268707e6072ed01f2259ac1679a6717b220ca5ddc4cc8a55cbeb2
```
- ExchangeFunctions을 통해 HTTP POST 요청할 정보 생성
- PooledConnectionProvider에서 [Channel acquired] 를 통해 연결할 정보를 생성하고, 현재 HTTP 연결 상황 보여줌
  - 1 active connections
  - 0 inactive connections
  - 0 pending acquire requests
- HttpClientConnect에 Handler being applied
  - 핸들러 정보 : `{uri=https://kip17-api.klaytnapi.com/v2/contract/0xa875f3b7e62ea14cde486cfb6f4c3e5926dceedb/token/0x2, method=POST}`
- DefaultPooledConnectionProvider에서 해당 요청에 대한 단계별 변경을 감지 [onStateChange]
  - request_prepared
  - request_sent
  - response_received
  - response_completed
  - disconnecting
  - Releasing channel
- PooledConnectionProvider에서 [Channel cleaned]
  - 0 active connections
  - 1 inactive connections
  - 0 pending acquire requests.

- **테스트 대상 메서드 findAllTokensOwnedByUser()**
  - 여러 HTTP 요청 with CountDownLatch

- **로그 findAllTokensOwnedByUser()**
```
16:39:42.219 [TRACE] [Test worker] [o.s.w.r.f.client.ExchangeFunctions] - [53506644] HTTP GET https://kip17-api.klaytnapi.com/v2/contract/0xb29566b9f7ff197c84b1df3fa203e0e230fa87c2/owner/0xEa06ee0577795e39A0465b46d509168ff6302973, headers={masked}
16:39:42.229 [DEBUG] [reactor-http-nio-4] [r.n.r.DefaultPooledConnectionProvider] - [ceaf5bfe, L:/10.64.154.214:64166 - R:kip17-api.klaytnapi.com/13.125.50.215:443] Registering pool release on close event for channel
16:39:42.230 [DEBUG] [reactor-http-nio-4] [r.n.r.PooledConnectionProvider] - [ceaf5bfe, L:/10.64.154.214:64166 - R:kip17-api.klaytnapi.com/13.125.50.215:443] Channel connected, now: 9 active connections, 0 inactive connections and 0 pending acquire requests.
16:39:42.235 [TRACE] [Test worker] [o.s.w.r.f.client.ExchangeFunctions] - [5cafef6f] HTTP GET https://kip17-api.klaytnapi.com/v2/contract/0x520a316aba944eefc243c8fceeef5a4be06fe378/owner/0xEa06ee0577795e39A0465b46d509168ff6302973, headers={masked}
16:39:42.247 [DEBUG] [reactor-http-nio-3] [r.n.r.PooledConnectionProvider] - [1e9ce816] Created a new pooled channel, now: 9 active connections, 0 inactive connections and 0 pending acquire requests.
16:39:42.247 [DEBUG] [reactor-http-nio-3] [reactor.netty.tcp.SslProvider] - [1e9ce816] SSL enabled using engine sun.security.ssl.SSLEngineImpl@38f950c9 and SNI kip17-api.klaytnapi.com:443
16:39:42.247 [DEBUG] [reactor-http-nio-3] [r.netty.transport.TransportConfig] - [1e9ce816] Initialized pipeline DefaultChannelPipeline{(reactor.left.sslHandler = io.netty.handler.ssl.SslHandler), (reactor.left.sslReader = reactor.netty.tcp.SslProvider$SslReadHandler), (reactor.left.httpCodec = io.netty.handler.codec.http.HttpClientCodec), (reactor.left.httpDecompressor = io.netty.handler.codec.http.HttpContentDecompressor), (reactor.right.reactiveBridge = reactor.netty.channel.ChannelOperationsHandler)}
16:39:42.249 [TRACE] [Test worker] [o.s.w.r.f.client.ExchangeFunctions] - [5fcef70b] HTTP GET https://kip17-api.klaytnapi.com/v2/contract/0x6b319ab59f2c85c49dc9ec2d8280d55614980ea2/owner/0xEa06ee0577795e39A0465b46d509168ff6302973, headers={masked}
16:39:42.251 [DEBUG] [reactor-http-nio-1] [i.netty.resolver.dns.DnsQueryContext] - [id: 0x6cf98367] WRITE: UDP, [16838: /10.4.1.151:53], DefaultDnsQuestion(kip17-api.klaytnapi.com. IN A)
16:39:42.255 [DEBUG] [reactor-http-nio-6] [r.n.r.PooledConnectionProvider] - [3a76f4e0] Created a new pooled channel, now: 9 active connections, 0 inactive connections and 0 pending acquire requests.
16:39:42.255 [DEBUG] [reactor-http-nio-3] [r.n.r.PooledConnectionProvider] - [dcdbe426] Created a new pooled channel, now: 9 active connections, 0 inactive connections and 0 pending acquire requests.
16:39:42.256 [TRACE] [reactor-http-nio-2] [o.s.h.codec.json.Jackson2JsonDecoder] - [1eff0d64] [0a3d2492-51, L:/10.64.154.214:64162 - R:kip17-api.klaytnapi.com/13.125.28.148:443] Decoded [com.backend.connectable.kas.service.token.dto.TokensResponse@1baeab40]
16:39:42.257 [DEBUG] [reactor-http-nio-3] [reactor.netty.tcp.SslProvider] - [dcdbe426] SSL enabled using engine sun.security.ssl.SSLEngineImpl@1d40d18f and SNI kip17-api.klaytnapi.com:443
16:39:42.260 [DEBUG] [reactor-http-nio-2] [r.n.r.DefaultPooledConnectionProvider] - [0a3d2492, L:/10.64.154.214:64162 - R:kip17-api.klaytnapi.com/13.125.28.148:443] onStateChange(GET{uri=/v2/contract/0xa875f3b7e62ea14cde486cfb6f4c3e5926dceedb/owner/0xEa06ee0577795e39A0465b46d509168ff6302973, connection=PooledConnection{channel=[id: 0x0a3d2492, L:/10.64.154.214:64162 - R:kip17-api.klaytnapi.com/13.125.28.148:443]}}, [response_completed])
16:39:42.260 [DEBUG] [reactor-http-nio-2] [r.n.r.DefaultPooledConnectionProvider] - [0a3d2492, L:/10.64.154.214:64162 - R:kip17-api.klaytnapi.com/13.125.28.148:443] onStateChange(GET{uri=/v2/contract/0xa875f3b7e62ea14cde486cfb6f4c3e5926dceedb/owner/0xEa06ee0577795e39A0465b46d509168ff6302973, connection=PooledConnection{channel=[id: 0x0a3d2492, L:/10.64.154.214:64162 - R:kip17-api.klaytnapi.com/13.125.28.148:443]}}, [disconnecting])
16:39:42.260 [DEBUG] [reactor-http-nio-2] [r.n.r.DefaultPooledConnectionProvider] - [0a3d2492, L:/10.64.154.214:64162 - R:kip17-api.klaytnapi.com/13.125.28.148:443] Releasing channel
16:39:42.261 [DEBUG] [reactor-http-nio-6] [reactor.netty.tcp.SslProvider] - [3a76f4e0] SSL enabled using engine sun.security.ssl.SSLEngineImpl@5bec0d52 and SNI kip17-api.klaytnapi.com:443
16:39:42.267 [DEBUG] [reactor-http-nio-5] [r.n.r.PooledConnectionProvider] - [4911b8cf] Created a new pooled channel, now: 9 active connections, 0 inactive connections and 0 pending acquire requests.
16:39:42.267 [DEBUG] [reactor-http-nio-1] [r.n.r.PooledConnectionProvider] - [ffb5a955] Created a new pooled channel, now: 9 active connections, 0 inactive connections and 0 pending acquire requests.
16:39:42.268 [DEBUG] [reactor-http-nio-2] [r.n.r.PooledConnectionProvider] - [0a3d2492, L:/10.64.154.214:64162 - R:kip17-api.klaytnapi.com/13.125.28.148:443] Channel cleaned, now: 8 active connections, 1 inactive connections and 0 pending acquire requests.
16:39:42.268 [DEBUG] [reactor-http-nio-6] [r.netty.transport.TransportConfig] - [3a76f4e0] Initialized pipeline DefaultChannelPipeline{(reactor.left.sslHandler = io.netty.handler.ssl.SslHandler), (reactor.left.sslReader = reactor.netty.tcp.SslProvider$SslReadHandler), (reactor.left.httpCodec = io.netty.handler.codec.http.HttpClientCodec), (reactor.left.httpDecompressor = io.netty.handler.codec.http.HttpContentDecompressor), (reactor.right.reactiveBridge = reactor.netty.channel.ChannelOperationsHandler)}
16:39:42.269 [DEBUG] [reactor-http-nio-7] [r.n.r.PooledConnectionProvider] - [3b9c0a13] Created a new pooled channel, now: 8 active connections, 1 inactive connections and 0 pending acquire requests.
16:39:42.269 [TRACE] [Test worker] [o.s.w.r.f.client.ExchangeFunctions] - [7e06727f] HTTP GET https://kip17-api.klaytnapi.com/v2/contract/0xe13e1f3c1270b5f9f7a641ae0eadfc18582e0b93/owner/0xEa06ee0577795e39A0465b46d509168ff6302973, headers={masked}
16:39:42.270 [DEBUG] [reactor-http-nio-2] [r.n.r.PooledConnectionProvider] - [8e456b4c] Created a new pooled channel, now: 8 active connections, 1 inactive connections and 0 pending acquire requests.
16:39:42.271 [DEBUG] [reactor-http-nio-3] [r.netty.transport.TransportConfig] - [dcdbe426] Initialized pipeline DefaultChannelPipeline{(reactor.left.sslHandler = io.netty.handler.ssl.SslHandler), (reactor.left.sslReader = reactor.netty.tcp.SslProvider$SslReadHandler), (reactor.left.httpCodec = io.netty.handler.codec.http.HttpClientCodec), (reactor.left.httpDecompressor = io.netty.handler.codec.http.HttpContentDecompressor), (reactor.right.reactiveBridge = reactor.netty.channel.ChannelOperationsHandler)}
16:39:42.271 [DEBUG] [reactor-http-nio-1] [reactor.netty.tcp.SslProvider] - [ffb5a955] SSL enabled using engine sun.security.ssl.SSLEngineImpl@138d51de and SNI kip17-api.klaytnapi.com:443
16:39:42.271 [DEBUG] [reactor-http-nio-7] [reactor.netty.tcp.SslProvider] - [3b9c0a13] SSL enabled using engine sun.security.ssl.SSLEngineImpl@3cf6c160 and SNI kip17-api.klaytnapi.com:443
16:39:42.273 [DEBUG] [reactor-http-nio-6] [r.n.r.PooledConnectionProvider] - [190246bb] Created a new pooled channel, now: 8 active connections, 1 inactive connections and 0 pending acquire requests.
16:39:42.275 [DEBUG] [reactor-http-nio-5] [reactor.netty.tcp.SslProvider] - [4911b8cf] SSL enabled using engine sun.security.ssl.SSLEngineImpl@36166e66 and SNI kip17-api.klaytnapi.com:443
16:39:42.277 [TRACE] [Test worker] [o.s.w.r.f.client.ExchangeFunctions] - [2e3459bd] HTTP GET https://kip17-api.klaytnapi.com/v2/contract/0x0b794696d6e3f0ad4c884b0a74da61883f03e375/owner/0xEa06ee0577795e39A0465b46d509168ff6302973, headers={masked}
16:39:42.278 [DEBUG] [reactor-http-nio-3] [r.n.r.DefaultPooledConnectionProvider] - [4edbb9b2, L:/10.64.154.214:64176 - R:kip17-api.klaytnapi.com/54.180.209.250:443] Registering pool release on close event for channel
16:39:42.278 [DEBUG] [reactor-http-nio-3] [r.n.r.PooledConnectionProvider] - [4edbb9b2, L:/10.64.154.214:64176 - R:kip17-api.klaytnapi.com/54.180.209.250:443] Channel connected, now: 10 active connections, 0 inactive connections and 0 pending acquire requests.
16:39:42.281 [DEBUG] [reactor-http-nio-4] [r.n.r.PooledConnectionProvider] - [9e2fad53] Created a new pooled channel, now: 10 active connections, 0 inactive connections and 0 pending acquire requests.
16:39:42.283 [DEBUG] [reactor-http-nio-5] [r.netty.transport.TransportConfig] - [4911b8cf] Initialized pipeline DefaultChannelPipeline{(reactor.left.sslHandler = io.netty.handler.ssl.SslHandler), (reactor.left.sslReader = reactor.netty.tcp.SslProvider$SslReadHandler), (reactor.left.httpCodec = io.netty.handler.codec.http.HttpClientCodec), (reactor.left.httpDecompressor = io.netty.handler.codec.http.HttpContentDecompressor), (reactor.right.reactiveBridge = reactor.netty.channel.ChannelOperationsHandler)}
16:39:42.284 [DEBUG] [reactor-http-nio-4] [reactor.netty.tcp.SslProvider] - [9e2fad53] SSL enabled using engine sun.security.ssl.SSLEngineImpl@2431cb75 and SNI kip17-api.klaytnapi.com:443
16:39:42.284 [DEBUG] [reactor-http-nio-7] [r.netty.transport.TransportConfig] - [3b9c0a13] Initialized pipeline DefaultChannelPipeline{(reactor.left.sslHandler = io.netty.handler.ssl.SslHandler), (reactor.left.sslReader = reactor.netty.tcp.SslProvider$SslReadHandler), (reactor.left.httpCodec = io.netty.handler.codec.http.HttpClientCodec), (reactor.left.httpDecompressor = io.netty.handler.codec.http.HttpContentDecompressor), (reactor.right.reactiveBridge = reactor.netty.channel.ChannelOperationsHandler)}
16:39:42.285 [DEBUG] [reactor-http-nio-2] [reactor.netty.tcp.SslProvider] - [8e456b4c] SSL enabled using engine sun.security.ssl.SSLEngineImpl@64f95523 and SNI kip17-api.klaytnapi.com:443
16:39:42.285 [DEBUG] [reactor-http-nio-1] [r.netty.transport.TransportConfig] - [ffb5a955] Initialized pipeline DefaultChannelPipeline{(reactor.left.sslHandler = io.netty.handler.ssl.SslHandler), (reactor.left.sslReader = reactor.netty.tcp.SslProvider$SslReadHandler), (reactor.left.httpCodec = io.netty.handler.codec.http.HttpClientCodec), (reactor.left.httpDecompressor = io.netty.handler.codec.http.HttpContentDecompressor), (reactor.right.reactiveBridge = reactor.netty.channel.ChannelOperationsHandler)}
16:39:42.287 [DEBUG] [reactor-http-nio-1] [r.n.r.PooledConnectionProvider] - [02691056] Created a new pooled channel, now: 10 active connections, 0 inactive connections and 0 pending acquire requests.
16:39:42.288 [DEBUG] [reactor-http-nio-1] [reactor.netty.tcp.SslProvider] - [02691056] SSL enabled using engine sun.security.ssl.SSLEngineImpl@18176471 and SNI kip17-api.klaytnapi.com:443
16:39:42.288 [TRACE] [Test worker] [o.s.w.r.f.client.ExchangeFunctions] - [d431f83] HTTP GET https://kip17-api.klaytnapi.com/v2/contract/0x34fe68fa5988f04b2c35b6ade16dc6ad8be26c7b/owner/0xEa06ee0577795e39A0465b46d509168ff6302973, headers={masked}
16:39:42.289 [DEBUG] [reactor-http-nio-2] [r.netty.transport.TransportConfig] - [8e456b4c] Initialized pipeline DefaultChannelPipeline{(reactor.left.sslHandler = io.netty.handler.ssl.SslHandler), (reactor.left.sslReader = reactor.netty.tcp.SslProvider$SslReadHandler), (reactor.left.httpCodec = io.netty.handler.codec.http.HttpClientCodec), (reactor.left.httpDecompressor = io.netty.handler.codec.http.HttpContentDecompressor), (reactor.right.reactiveBridge = reactor.netty.channel.ChannelOperationsHandler)}
16:39:42.289 [DEBUG] [reactor-http-nio-6] [reactor.netty.tcp.SslProvider] - [190246bb] SSL enabled using engine sun.security.ssl.SSLEngineImpl@29a46cd7 and SNI kip17-api.klaytnapi.com:443
16:39:42.292 [DEBUG] [reactor-http-nio-2] [r.n.r.PooledConnectionProvider] - [bf4051be] Created a new pooled channel, now: 10 active connections, 0 inactive connections and 0 pending acquire requests.
16:39:42.292 [DEBUG] [reactor-http-nio-4] [r.netty.transport.TransportConfig] - [9e2fad53] Initialized pipeline DefaultChannelPipeline{(reactor.left.sslHandler = io.netty.handler.ssl.SslHandler), (reactor.left.sslReader = reactor.netty.tcp.SslProvider$SslReadHandler), (reactor.left.httpCodec = io.netty.handler.codec.http.HttpClientCodec), (reactor.left.httpDecompressor = io.netty.handler.codec.http.HttpContentDecompressor), (reactor.right.reactiveBridge = reactor.netty.channel.ChannelOperationsHandler)}
16:39:42.291 [DEBUG] [reactor-http-nio-5] [r.n.r.PooledConnectionProvider] - [67d95e91] Created a new pooled channel, now: 10 active connections, 0 inactive connections and 0 pending acquire requests.
16:39:42.294 [DEBUG] [reactor-http-nio-1] [r.netty.transport.TransportConfig] - [02691056] Initialized pipeline DefaultChannelPipeline{(reactor.left.sslHandler = io.netty.handler.ssl.SslHandler), (reactor.left.sslReader = reactor.netty.tcp.SslProvider$SslReadHandler), (reactor.left.httpCodec = io.netty.handler.codec.http.HttpClientCodec), (reactor.left.httpDecompressor = io.netty.handler.codec.http.HttpContentDecompressor), (reactor.right.reactiveBridge = reactor.netty.channel.ChannelOperationsHandler)}
16:39:42.295 [DEBUG] [reactor-http-nio-5] [reactor.netty.tcp.SslProvider] - [67d95e91] SSL enabled using engine sun.security.ssl.SSLEngineImpl@1d463c58 and SNI kip17-api.klaytnapi.com:443
16:39:42.295 [DEBUG] [reactor-http-nio-2] [reactor.netty.tcp.SslProvider] - [bf4051be] SSL enabled using engine sun.security.ssl.SSLEngineImpl@3b7bbfb and SNI kip17-api.klaytnapi.com:443
16:39:42.297 [DEBUG] [reactor-http-nio-6] [r.netty.transport.TransportConfig] - [190246bb] Initialized pipeline DefaultChannelPipeline{(reactor.left.sslHandler = io.netty.handler.ssl.SslHandler), (reactor.left.sslReader = reactor.netty.tcp.SslProvider$SslReadHandler), (reactor.left.httpCodec = io.netty.handler.codec.http.HttpClientCodec), (reactor.left.httpDecompressor = io.netty.handler.codec.http.HttpContentDecompressor), (reactor.right.reactiveBridge = reactor.netty.channel.ChannelOperationsHandler)}
16:39:42.302 [DEBUG] [reactor-http-nio-1] [r.n.r.PooledConnectionProvider] - [2ac83947] Created a new pooled channel, now: 11 active connections, 0 inactive connections and 0 pending acquire requests.
16:39:42.303 [DEBUG] [reactor-http-nio-5] [r.netty.transport.TransportConfig] - [67d95e91] Initialized pipeline DefaultChannelPipeline{(reactor.left.sslHandler = io.netty.handler.ssl.SslHandler), (reactor.left.sslReader = reactor.netty.tcp.SslProvider$SslReadHandler), (reactor.left.httpCodec = io.netty.handler.codec.http.HttpClientCodec), (reactor.left.httpDecompressor = io.netty.handler.codec.http.HttpContentDecompressor), (reactor.right.reactiveBridge = reactor.netty.channel.ChannelOperationsHandler)}
16:39:42.303 [DEBUG] [reactor-http-nio-6] [r.n.r.DefaultPooledConnectionProvider] - [b4b598e6, L:/10.64.154.214:64177 - R:kip17-api.klaytnapi.com/54.180.209.250:443] Registering pool release on close event for channel
16:39:42.303 [DEBUG] [reactor-http-nio-6] [r.n.r.PooledConnectionProvider] - [b4b598e6, L:/10.64.154.214:64177 - R:kip17-api.klaytnapi.com/54.180.209.250:443] Channel connected, now: 11 active connections, 0 inactive connections and 0 pending acquire requests.
16:39:42.304 [DEBUG] [reactor-http-nio-2] [r.netty.transport.TransportConfig] - [bf4051be] Initialized pipeline DefaultChannelPipeline{(reactor.left.sslHandler = io.netty.handler.ssl.SslHandler), (reactor.left.sslReader = reactor.netty.tcp.SslProvider$SslReadHandler), (reactor.left.httpCodec = io.netty.handler.codec.http.HttpClientCodec), (reactor.left.httpDecompressor = io.netty.handler.codec.http.HttpContentDecompressor), (reactor.right.reactiveBridge = reactor.netty.channel.ChannelOperationsHandler)}
16:39:42.304 [DEBUG] [reactor-http-nio-2] [r.n.r.PooledConnectionProvider] - [0a3d2492, L:/10.64.154.214:64162 - R:kip17-api.klaytnapi.com/13.125.28.148:443] Channel acquired, now: 12 active connections, 0 inactive connections and 0 pending acquire requests.
16:39:42.306 [DEBUG] [reactor-http-nio-5] [r.n.r.DefaultPooledConnectionProvider] - [b6593b8c, L:/10.64.154.214:64170 - R:kip17-api.klaytnapi.com/13.125.50.215:443] Registering pool release on close event for channel
16:39:42.306 [DEBUG] [reactor-http-nio-5] [r.n.r.PooledConnectionProvider] - [b6593b8c, L:/10.64.154.214:64170 - R:kip17-api.klaytnapi.com/13.125.50.215:443] Channel connected, now: 12 active connections, 0 inactive connections and 0 pending acquire requests.
16:39:42.309 [DEBUG] [reactor-http-nio-1] [reactor.netty.tcp.SslProvider] - [2ac83947] SSL enabled using engine sun.security.ssl.SSLEngineImpl@41867521 and SNI kip17-api.klaytnapi.com:443
16:39:42.309 [TRACE] [Test worker] [o.s.w.r.f.client.ExchangeFunctions] - [251dd78f] HTTP GET https://kip17-api.klaytnapi.com/v2/contract/0x2d8e54bf078dfbfa490c877d74909be3e84dfb71/owner/0xEa06ee0577795e39A0465b46d509168ff6302973, headers={masked}
16:39:42.309 [DEBUG] [reactor-http-nio-2] [r.n.http.client.HttpClientConnect] - [0a3d2492-52, L:/10.64.154.214:64162 - R:kip17-api.klaytnapi.com/13.125.28.148:443] Handler is being applied: {uri=https://kip17-api.klaytnapi.com/v2/contract/0xe13e1f3c1270b5f9f7a641ae0eadfc18582e0b93/owner/0xEa06ee0577795e39A0465b46d509168ff6302973, method=GET}
16:39:42.311 [DEBUG] [reactor-http-nio-1] [r.netty.transport.TransportConfig] - [2ac83947] Initialized pipeline DefaultChannelPipeline{(reactor.left.sslHandler = io.netty.handler.ssl.SslHandler), (reactor.left.sslReader = reactor.netty.tcp.SslProvider$SslReadHandler), (reactor.left.httpCodec = io.netty.handler.codec.http.HttpClientCodec), (reactor.left.httpDecompressor = io.netty.handler.codec.http.HttpContentDecompressor), (reactor.right.reactiveBridge = reactor.netty.channel.ChannelOperationsHandler)}
16:39:42.322 [TRACE] [Test worker] [o.s.w.r.f.client.ExchangeFunctions] - [68c5dcd9] HTTP GET https://kip17-api.klaytnapi.com/v2/contract/0x83889653394ba6162b1b88b4b13ae50febe941ef/owner/0xEa06ee0577795e39A0465b46d509168ff6302973, headers={masked}
16:39:42.325 [DEBUG] [reactor-http-nio-1] [i.netty.resolver.dns.DnsNameResolver] - [id: 0x6cf98367] RECEIVED: UDP [16838: /10.4.1.151:53], DatagramDnsResponse(from: /10.4.1.151:53, to: /0:0:0:0:0:0:0:0:64537, 16838, QUERY(0), NoError(0), RD RA)
	DefaultDnsQuestion(kip17-api.klaytnapi.com. IN A)
	DefaultDnsRawRecord(kip17-api.klaytnapi.com. 47 IN A 4B)
	DefaultDnsRawRecord(kip17-api.klaytnapi.com. 47 IN A 4B)
	DefaultDnsRawRecord(kip17-api.klaytnapi.com. 47 IN A 4B)
	DefaultDnsRawRecord(OPT flags:0 udp:4000 0B)
```
- 우선 아까보다 훨씬 많은 쓰레드를 쓰고 있음 `reactor-http-nio-1` ~ `reactor-http-nio-7`
- DnsNameResolver를 통해 "kip17-api.klaytnapi.com" 의 DNS 주소 <-> IP 주소를 UDP를 통해 가져오고 있음 
- 소켓 Connection을 다른 API를 쓰는데도 그대로 쓰는 경우도 발견 => Keep-Alive?
  - 아 아니구나, 해당 소켓 통신 끝나가지고 그 포트 그대로 쓰는 거 일수도?
```
16:39:42.260 [DEBUG] [reactor-http-nio-2] - [0a3d2492, L:/10.64.154.214:64162 - R:kip17-api.klaytnapi.com/13.125.28.148:443] onStateChange(GET{uri=/v2/contract/0xa875f3b7e62ea14cde486cfb6f4c3e5926dceedb/owner/0xEa06ee0577795e39A0465b46d509168ff6302973, connection=PooledConnection{channel=[id: 0x0a3d2492, L:/10.64.154.214:64162 - R:kip17-api.klaytnapi.com/13.125.28.148:443]}}, [response_completed])
16:39:42.309 [DEBUG] [reactor-http-nio-2] - [0a3d2492-52, L:/10.64.154.214:64162 - R:kip17-api.klaytnapi.com/13.125.28.148:443] Handler is being applied: {uri=https://kip17-api.klaytnapi.com/v2/contract/0xe13e1f3c1270b5f9f7a641ae0eadfc18582e0b93/owner/0xEa06ee0577795e39A0465b46d509168ff6302973, method=GET}
```

## 어떻게 WebFlux는 적은 리소스로 많은 트래픽을 감당할 수 있을까?
**[Blocking I/O]**
- RestTemplate은 동기적으로 동작한다는 거야~
```java
@Test
public void blocking() {
    final RestTemplate restTemplate = new RestTemplate();
    
    final StopWatch stopWatch = new StopWatch();
    stopWatch.start();
    
    for (int i=0; i<3; i++) {
        final ResponseEntity<String> response = restTemplate.exchange(THREE_SEC_URL);
    }
    
    stopWatch.stop();
    System.out.println(stopWatch.getTotalTimeSeconds());
}
```
- 총 3*3 = 9초가 걸림
- 이걸 3개에 쓰레드에 각각 할당시켜 처리한다하더라도 Context Switching으로 인해 오버헤드 발생해 3초 넘어감
- **[과정]**
  1. Spring MVC에서 들어온 Http Request는 Tomcat의 하나의 쓰레드풀에 있던 쓰레드에 매핑이 됨 (http-nio-8080-exec-#)
  2. 해당 쓰레드가 RestTemplate을 생성함
  3. RestTemplate이 네트워크 요청을 보냄 (I/O 발생)
     - RestTemplate에서 HttpURLConnection 소켓 만들어서 커넥션 수립 (쓰레드를 만들겠죠?)
     - **커널이 제어권을 가져가 (Sync/Blocking)**
     - 커널에서 해당 요청을 받아 네트워크 다녀옴
  4. 해당 쓰레드는 응답이 올때까지 약 3초간 아무것도 못함
  5. 응답이 왔을 때, RestTemplate이 네트워크 요청을 보냄 (I/O 발생)
  6. 이렇게 반복해서 약 9초의 실행시간이 걸림

**[Non-Blocking I/O]**
- WebClient는 비동기적으로 동작한다는 거야~
```java
@Test
public void nonBlocking() {
    final StopWatch stopWatch = new StopWatch();
    stopWatch.start();
  
    for (int i=0; i<1000; i++) {
        this.webClient.get()
        .uri(THREE_SEC_URL)
        .retrieve()
        .bodyToMono(String.class)
        .subscribe(it -> {
            count.countDown();
            System.out.println(it);
        });
    }
    
    count.await(10, TimeUnit.SECONDS);
    stopWatch.stop();
    System.out.println(stopWatch.getTotalTimeSeconds());
}
```
- 1000번 호출해도 약 4초 훨씬 효율적
- **[과정]**
  1. Spring MVC에서 들어온 Http Request는 Tomcat의 하나의 쓰레드풀에 있던 쓰레드에 매핑이 됨 (http-nio-8080-exec-#)
  2. 해당 쓰레드가 WebClient를 생성함
  3. WebClient가 네트워크 요청을 보냄 (I/O 발생)
     - WebClient에서 만들어둔 쓰레드 풀 사용하여 네트워크 태움 `reactor-http-epoll-1`
     - WebClient는 Event-Driven/Async/Non-Blocking이라, **바로 제어권을 어플리케이션 단에 돌려줘**
     - 커널은 요청 보내고 응답을 기다려
  4. 제어권을 다시 받은 쓰레드는 그 다음 행동 수행, WebClient가 네트워크 요청을 보냄 (I/O 발생)
  5. 또 제어권을 다시 받은 쓰레드는 그 다음 행동 수행, WebClient가 네트워크 요청을 보냄 (I/O 발생)
  6. 이때, 커널이 요청에 대한 응답을 받고, 쓰레드의 EventListener한테 작업이 끝났다고 알려줘!
  7. 그 때 EventListener에서 구현해뒀던 코드를 실행
  8. 이렇게 보인 이벤트들이 반복되어 3초면 쇼부봄