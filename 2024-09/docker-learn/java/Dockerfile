FROM openjdk:17-oracle

# /bin/bash: 실행될 프로그램
# -c: bash에게 뒤따르는 문자열을 커맨드로 읽으란 소리
# sleep 500: 프로세스를 약 500초 (8.3 분) 간 멈추기
# -> 이렇게 하면 exec 등으로 해당 컨테이너에 접근 가능해짐
ENTRYPOINT ["/bin/bash", "-c", "sleep 500"]
