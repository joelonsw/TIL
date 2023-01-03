## Redis

### Redis란?
- *참고: https://github.com/redis/redis*
- *참고: https://ko.quish.tv/redis-vs-mysql-benchmarks*
- **왜 필요한데?**
  - DB, 캐시 및 메시지 브로커로 사용되는 오픈소스
  - 인메모리 데이터 구조 저장소
  - Key-Value 형식으로 저장
  - 110000 SET/second, 81000 GET/second 수행 가능 => 초고속

- **vs MySQL**
  - 레디스는 만료기간을 지원한다.
  - 레디스는 데이터 저장에 별도 테이블을 만들 필요 없다
  - MySQL은 Lock 범위가 Table
    - MySQL Memory Engine의 모든 동시 쓰레드는 큐에서 대기
    - 따라서 수정이 일어나는 경우 요청이 대기해야 함 
  - 레디스는 단일 쓰레드를 사용해 분산 잠금 필요 X

- **RDB 보다 얼마나 빠른데?**
  - *참고: https://dzone.com/articles/redis-vs-mysql-benchmarks*
  - 요청이 많이 늘수록, 레디스를 붙인 mysql이 성능 훨씬 좋아짐

- **Redis Datatype**
  - *참고: https://redis.io/docs/data-types/*
  - [Strings]
    ```
    > SET user:1 salvatore
    OK
    > GET user:1
    "salvatore"
    ```
    - 대부분 O(1)    
    - SUBSTR, GETRANGE, SETRANCE 등의 명령어는 O(n)이 될수도
  - [LIST]
    - head/tail 접근 O(1)
    - list 안에 들어있는 엘리멘트 조작 O(n)
  - [SET]
    - Unoredered Collection of unique strings
    - ADD/REMOVE/CHECK_ITEM_PRESENT => O(1)
  - [HASHES]
    - field-value 페어
    - 자바 해시맵과 비슷
    ```
    > HSET user:123 username martina firstName Martina lastName Elisa country GB
    (integer) 4
    > HGET user:123 username
    "martina"
    > HGETALL user:123
    1) "username"
    2) "martina"
    3) "firstName"
    4) "Martina"
    5) "lastName"
    6) "Elisa"
    7) "country"
    8) "GB"
    ```
  - [SORTED SETS]
  - [Streams]
  - [Geospatial indexes]
  - [Bitmaps]
  - [Bitfields]
  - [HyperLogLog]

- **레디스는 해시충돌을 어떻게 해결하지?**
  - *참고: https://intrepidgeeks.com/tutorial/hash-collision-and-progressive-rehash-source-analysis-in-redis*

- **A little internal on Redis hash table implementation**
  - *참고: https://kousiknath.medium.com/a-little-internal-on-redis-key-value-storage-implementation-fdf96bac7453*
  - 레디스는 메모리를 써서 높은 속도를 보장
  - 싱글쓰레드로 동작함
  - 레디스가 String을 저장하던, set을 저장하던, hash를 저장하던 모든건 다 hash table 안에 저장됨
  - 데이터 구조 살펴보기
    - dict
      - dictht ht[2]
    - dictht 
      - hashtable
    - dictEntry
      - 링크드리스트 key-value 
  - 초기 dictht 해시테이블 사이즈 4 => 리사이즈는 다음과 같을 때
    1. total_elements / total_buckets = 1 && dict_resize = true
       - 리해싱 최대한 피하려고함
    2. total_elements / total_buckets > 5
  - 단일 쓰레드 redis 입장에서 해시 테이블 크기 조정 및 리해싱을 block 되지 않는 방식으로 동작시켜야해

### Connectable에서 사용한 Redis
- **정필이 코드**
```java
@RequiredArgsConstructor
@Service
public class RedisUtil {
    private final StringRedisTemplate stringRedisTemplate;

    public String getData(String key) {
        ValueOperations<String, String> valueOperations = stringRedisTemplate.opsForValue();
        return valueOperations.get(key);
    }

    public void setData(String key, String value) {
        ValueOperations<String, String> valueOperations = stringRedisTemplate.opsForValue();
        valueOperations.set(key, value);
    }

    public void setDataExpire(String key, String value, long duration) {
        ValueOperations<String, String> valueOperations = stringRedisTemplate.opsForValue();
        Duration expireDuration = Duration.ofSeconds(duration);
        valueOperations.set(key, value, expireDuration);
    }
}

public AuthService {
    public String getAuthKey (String phoneNumber, Long duration){
        String generatedKey = generateCertificationKey();
        String message = "Connectable 인증번호는 " + generatedKey + "입니다.";
        sendSms(message, phoneNumber);
        redisUtil.setDataExpire(phoneNumber, generatedKey, 60 * duration);
        return generatedKey;
    }

    public boolean certifyKey (String phoneNumber, String authKey){
        String generatedKey = redisUtil.getData(phoneNumber);
        return validateAuthKey(generatedKey, authKey);
    }
}
```

- **내 코드**
```java
@Getter
@RedisHash(value = "UserTicketEntrance", timeToLive = 60)
public class UserTicketEntrance {

    @Id private final String klaytnAddress;
    private final Long ticketId;
    private final String verification;

    @Builder
    public UserTicketEntrance(String klaytnAddress, Long ticketId, String verification) {
        this.klaytnAddress = klaytnAddress;
        this.ticketId = ticketId;
        this.verification = verification;
    }
}

public interface UserTicketEntranceRedisRepository extends CrudRepository<UserTicketEntrance, String> {}

public class UserTicketService {
    private void saveUserTicketEntrance(String klaytnAddress, Long ticketId, String verification) {
        UserTicketEntrance userTicketEntrance =
            UserTicketEntrance.builder()
                .klaytnAddress(klaytnAddress)
                .ticketId(ticketId)
                .verification(verification)
                .build();
        userTicketEntranceRedisRepository.save(userTicketEntrance);
    }
}
```

### SpringBoot에서 Redis 사용하기
- *참고: https://kkambi.tistory.com/139*
- **StringRedisTemplate/RedisTemplate**
  - key-value를 조작하여 객체를 직접 설정
  - `@Autowired` StringRedisTemplate
  - opsForValue() = ValueOperations<K,V\>
    - 보통 <String, String\>
  ```java
  ValueOperations<String, String\> values = redisTemplate.opsForValue();
  values.set("name", "joel");
  ```

- **CrudRepository**
  - Spring Data JPA를 활용해 객체를 relation으로 매핑하는 것과 유사
  - Entity 역할의 클래스 생성
    - `@RedisHash` 도메인 클래스에 생성
      - KEY: 특정 해시값
      - VALUE : 클래스 인스턴스
    - `@Id` ID 필드
  - CrudRepository 상속받는 Interface 생성
    - 이후 JPA Repository 처럼 사용 가능

- **`@RedisHash` 저장 방법**
  - HashMap<`@RedisHash 이름`, HashMap<`@Id`, 엔티티\>\>
