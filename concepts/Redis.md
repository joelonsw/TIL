## Redis

### Redis란?

### Spring에서 Redis를 사용하기
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