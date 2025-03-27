# Kubernetes (CKA)
*참고: https://kubernetes.io/docs/home/*  
*참고: https://www.udemy.com/course/certified-kubernetes-administrator-with-practice-tests/*

## 쿠버네티스 아키텍쳐
#### 공통
- 모든 노드에서는 도커와 같은 컨테이너 엔진이 필요

#### Master Node
- 역할 - Manage / Plan / Schedule / Monitor

- **ETCD cluster**
  - key-value 형식의 DB
  - 2379 포트에서 listening

- **kube-scheduler**
  - 어떤 Pod가 어떤 Node에 들어갈지 결정 (실제 배치는 Kubelet에서 진행)
    - 적재할만큼 용량이 되는지, 올바른 dest 인지
    - Scheduling
      1. Filter Nodes: Cpu/memory 하한 검증
      2. Rank Nodes: 0~10 점수 메겨서 어디가 적합할지 검증

- **kube-controller-manager**
  - node controller: 노드 상태 및 장애 감지
  - replication controller: 파드 갯수 유지 및 복제 관리
  - endpoint controller: 서비스-파드 간 연결 관리
  - service account & token controller: API 접근 위한 계정/토큰 관리
  - 기타 역할 많음: deployment, namespace, endpoint, job, pv-protection, service-account, pv-binder, cronjob, stateful set, replicaset

- **kube-apiserver**
  - 클러스터 구성요소 통신하는 중심 허브
  - `kubectl` 명령어 및 다른 클라이언트 요청 처리
  - 인증/인가
  - etcd 통신하여 클러스터 상태 저장/조회

#### Worker Node
- **kubelet**
  - `kube-apiserver`에게 현재 워커 노드 상태 보고
  - 각 Container의 선장으로, 컨테이너 런타임을 통해 컨테이너 실행/모니터링
    1. Node Register
    2. Pod 생성
    3. Node/Pod 모니터

- **kube-proxy**
  - 네트워크 통신 관리 역할
  - iptable/IPVS 통한 네트워크 트래픽 라우팅
  - 클러스터 내/외부 서비스 접근을 위한 네트워크 규칙 설정

## Kubernetes Workload Resource
- **ReplicaSet**
  - 특정 갯수의 Pod 갯수를 유지하는 역할
  - 파드 죽으면 새로운 파드 생성
  - 직접 사용하기보단 Deployment에서 주로 관리

- **Deployment**
  - 내부적으로 `ReplicaSet` 생성/관리
  - 어플리케이션 배포 및 업데이트 기능 제공
  - 롤링 업데이트 및 롤백 가능
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: my-deployment
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: my-app
      template:
        metadata:
          name: myapp-pod
      spec:
        containers:
          - name: nginx-container
            image: nginx
    ```

- **DaemonSet**
  - 클러스터의 모든(혹은 특정) 노드에 하나의 파드를 실행하도록 보장하는 리소스
  - 각 노드 별 하나의 파드로 배포하는 방식
  - 특징
    1. 모든 노드에 자동 배포
    2. 노드마다 하나의 파드만 실행됨
    3. 일반적인 사용 사례
       - 로그수집 에이전트 (Fluentd, Logstash)
       - 모니터링 에이전트 (Prometheus Node Exporter, Datadog)
       - 네트워크 관리 도구 (CNI 플러그인, kube-proxy)
       - 보안/시스템 관리 도구 (Falco, Sysdig)
    ```yaml
    apiVersion: apps/v1
    kind: DaemonSet
    metadata:
      name: monitoring-daemon
    spec:
      selector:
        matchLabels:
          app: monitoring-agent
      template:
        metadata:
          labels:
            app: monitoring-agent
        spec:
          containers:
          - name: monitoring-agent
            image: monitoring-agent
    ```

## Kubernetes Service & Ingress
- **개요**
  - 여러개의 파드를 하나의 네트워크 엔드포인트 (고정 IP)로 묶어주는 역할
  - 파드가 동적으로 변해도 안정적인 네트워크 접근 제공
  - 로드밸런싱 가능
  - 내부/외부 트래픽 파드로 전달

- **ClusterIP**
  - 클러스터 내부에서만 접근 가능한 가상 IP 부여
  - 외부 접근 X
  - `my-service.default.svc.cluster.local` 같은 내부 DNS 접근 가
  - ex. 클러스터 내부에서만 사용되는 마이크로서비스간 통신
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: backend-service
    spec:
      selector:
        app: backend
      ports: 
        - protocol: TCP
          port: 80          # 서비스에서 노출할 포트
          targetPort: 8080  # 파드 내부에서 실행되는 포트
      type: ClusterIP
    ```

- **NodePort**
  - 각 노드의 특정 포트를 통해 외부에서 접근 가능
  - `<노드IP>:<노드Port>` 통해 외부에서 접근 가능
  - 포트 범위: 30000~32767
  - 작은 규모 테스트/내부 네트워크 운영시 사용
    ```yaml
    apiVersion: v1
    kind: Service
    metadat:
      name: nodeport-service
    spec:
      selector:
        app: web-app
      ports:
        - protocol: TCP
          port: 80
          targetPort: 8080
          nodePort: 30080
      type: NodePort
    ```

- **LoadBalancer**
  - AWS/GCP/Azure에서 외부 로드 밸런서 자동 생성
    - 클라우드 벤더가 제공하는 외부 로드 밸런서를 사용하여 트래픽을 파드로 전달 가능
  - `EXTERNAL-IP` 통해 클러스터 외부에서 직접 접근 가능 (클라우드 서비스에서만)
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: lb-service
    spec:
      selector:
        app: frontend
      ports:
        - protocol: TCP
          port: 80
          targetPort: 8080
      type: LoadBalancer
    ```
 
- **ExternalName**
  - 쿠버네티스 내부에서 외부 도메인으로 트래픽 전달 (CNAME 이라고 생각)
  - 내부 서비스에서 외부 서비스 접근할 때 사용
  - DNS 기반 라우팅 제공
  - 실제 트래픽은 쿠버 네트워크 벗어나 외부 서비스로 전송
  - ex) 
    - 쿠버네티스 내부에서 외부 DB에 접근
    - 클러스터 내부에서 외부 API 서버 호출
    - 내부 DNS를 통해 외부 서비스로 트래픽 라우팅
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: external-db
    spec: 
      type: ExternalName
      externalName: db.external-company.com
    ```
    
- **Ingress**
  - 쿠버네티스 내부 서비스에 대한 HTTP/HTTPS 요청 관리하는 API Gateway
  - 쿠버 클러스터 외부에서 들어오는 HTTP/HTTPS 요청을 내부 서비스로 라우팅하는 역할 수행
  - 특징
    - 여러 서비스를 하나의 진입점 (도메인) 관리 가능
    - 경로/호스트 기반 라우팅 가능
    - SSL/TLS 가능
    ```yaml
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: my-ingress
    spec:
      rules:
      - host: myapp.example.com
        http:
          paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: backend-service
                port: 
                  number: 80
    ```

## Scheduling
- **Taints & Tolerations**
  - 특정 노드에서 특정 파드를 제한하거나 허용하는 메커니즘
  - Taints: 노드에 적용하는 제한 규칙
    - `kubectl taint nodes node1 env=production:NoSchedule`
  - Toleration: 파드가 특정 노드의 제한을 무시하고 실행될 수 있도록 허용하는 설정
    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: production-pod
    spec:
      tolerations:
      - key: "env"
        operator: "Equal"
        value: "production"
        effect: "NoSchedule"
      containers:
      - name: app
        image: my-app:latest
    ```

- **nodeSelector**
  - node Selector 조건 중 가장 간단. 
  - pod에서 node labels를 통해서 지정
  - 하지만, not ssd, ssd or hdd 이런 논리연산자 등의 사용은 어려움
  - 예시)
    1. add label to node
       - `kubectl label nodes node01 disktype=ssd`
    2. node label 보기
      - `kubectl get nodes --show-labels`
    3. 해당 node로 pod 스케쥴링하기
       ```yaml
       apiVersion: v1
       kind: Pod
       metadata:
         name: nginx
         labels:
           env: test
       spec:
         containers:
         - name: nginx
           image: nginx
           imagePullPolicy: IfNotPresent
         nodeSelector:
           disktype: ssd
       ```

- **nodeAffinity**
  - 특정 조건을 만족하는 노드에만 파드 배치하도록 강제 (nodeSelector의 확장)
  - 강제 배치: `requiredDuringSchedulingIngnoredDuringExecution`
    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: nginx
      labels:
        env: test
    spec:
      containers:
      - name: nginx
        image: nginx
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
                - key: gpu
                  operator: In
                  values:
                  - "true"
    ```
- 선호 배치: `preferredDuringSchedulingIgnoredDuringExecution`
  ```yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: gpu-pod-preferred
  spec:
    affinity:
      nodeAffinity:
        preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 10
            preference:
              matchExpressions:
                - key: gpu
                  operator: In
                  values:
                    - "true"
    containers:
      - name: my-app
        image: my-app:latest
  ```
  
- **Additional Scheduler**
  - 커스텀 스케줄러가 생성 가능하다. 
  - yaml에 `schedulerName: ~` 으로 지정할 수 있음
    ) 

  
## Kubernetes Configuration
- **Static Pods**
  - kubelet이 스스로 만든 Pod (타 쿠버 클러스터 컴포넌트와 무관)
  - 특정 노드에서 직접 실행되는 파드
  - kubelet에 의해 직접 관리되며, API 서버 등록되지 않아도 실행 가능
  - 쿠버네티스 스케줄러가 관여 X
  - 셋업 경로: `/etc/kubernetes/manifest`
  - Control Plane(MasterNode)에 의존적이지 않기에, Control Plane 자체를 구성하는데 쓸 수 있음

- **Multi-Container Pods**
  - 사이드카로 같이 하나의 pod에 올릴 container 등록 가능
  ```yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: simple-webapp
    labels:
      name: simple-webapp
  spec:
    containers:
    - name: simple-webapp
      image: simple-webapp
      ports:
      - containerPort: 8080
    - name: log-agent
      image: log-agent
  ```

- **ConfigMap**
  1. 환경변수, 명령줄인자, 설정파일 등 저장 가능
  2. Pod와 독립적으로 관리됨
  3. k-v 페어로, data 관리
  - 예시)
    - configMap
    ```yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: app-config
    data:
      APP_COLOR: blue
      APP_MODE: prod
    ```
    - in Pods
    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: simple-webapp
      labels:
        name: simple-webapp
    spec:
      containers:
      - name: simple-webapp
        image: simple-webapp
        ports:
        - containerPort: 8080
      envFrom:
        - configMapRef:
            name: app-config
    ```

- **Secrets**
  - yaml `kind: Secret` 으로 생성하면, k-v BASE64 인코딩해서 저장 (깃헙에 푸시하지마...)
    - helm secret, vault 등을 추천
  - Secret 저장해도 etcd에는 그냥 plaintext로 보임 => etcd 암호화 가능하도록 만들자
    - `--encryption-provider-config` 활성화 여부 체크
    - encryption algorithm + key => yaml로 지정

- **logging/monitoring**
  - metrics server
    - 클러스터 당 하나 설치 권장
    - Node/Pod 정보 받아 인메모리에 저장: 히스토리 X
    - minikube: `minikube addons enable metrics-server`
    - others: `git clone https://github.com/kubernetes-incubator/metrics-server.git && k create -f deploy/1.8+/`
  - view
    - `k top node`, `k top pod`
  - log
    - 도커라면: `docker logs -f image`
    - 쿠버라면: `kubectl logs -f event-pod`

## Application Lifecycle & Management
- **Deployment Strategy**
  1. Rolling Update
     - 기본값 (명시 안하면 기본 이거)
     - 기존 파드 점진적으로 교체하여 어플리케이션 업데이트
     - 서비스 중단없이 고가용성 유지하며 배포
     - 설정할 수 있는 주요 옵션
       - `maxSurge`: 한번에 최대 몇개의 파드를 새롭게 생성할 수 있는지?
       - `maxUnavailable`: 업데이트 중 최소한으로 유지되어야 하는 파드 수 설정
  2. Recreate
     - 기존의 파드 종료한 뒤 새로운 버전의 파드 전부 시작
     - 서비스 중단 발생함
      ```yaml
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: my-deployment
      spec:
        replicas: 3
        selector: # 관리할 파드 선택 기준. 주로 template과 일치
          matchLabels:
            app: my-app
        template:
          metadata:
            labels:
              app: my-app
          spec:
            containers:
            - name: my-container
              image: my-image:v2
        strategy:
          type: Recreate
      ```

- **Lifecycle Management**
  - 라이프사이클 훅과 조정방법으로 수명주기 관리 가능
  1. Pod Lifecycle Hooks: `preStop`, `postStart`
  2. Horizontal Pod Autoscaler (HPA): 파드 수 부하에 맞게 리소스 할당
  3. Rolling Back
     - 배포 중 문제가 발생하면 기존 버전 롤백 가능. 
     - Deployment 리소스에 대해 버전 관리 제공
       - `kubectl rollout undo deployment/my-app`
       - `kubectl rollout undo deployment/my-app --to-revision=2`

- **Horizontal Pod Autoscaling (HPA)**
  - Vertical: CPU/Memory 더 많이 쓰자! 재구동이 필수
  - Horizontal: 서버 댓수 더 끌어와서 Load Balance
  - HPA: 쿠버에서 리소스 사용량 기반으로 자동으로 Pod 갯수를 조절
    - 주기적으로 메트릭 확인 -> 설정 기준 초과/미만 시 ReplicaSet의 Pod 갯수 조절
    - CPU 사용율, 메모리 사용율 기반 조정
    - Custom Metrics 사용 가능 (ex. HTTP 요청, Kafka MQ 길이)
      - 다만 Custom Metrics 사용을 위해선 Prometheus Adapter 등 추가 설정 필요할 수 있음
  - HorizontalPodAutoscaler로 Deployment/ReplicaSet의 scale을 조절
    - `desiredReplicas = ceil{currentReplicas * currentMetricValue / desiredMeetricValue}`
  - 구성 
  ```yaml
  apiVersion: autoscaling/v2
  king: HorizontalPodAutoscaler
  metadata:
    name: my-app-hpa
  spec:
    scaleTargetRef:
      apiVersion: apps/v1
      kind: Deployment
      name: my-app
    minReplicas: 1
    maxReplicas: 10
    metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
  ```
  - `kubectl get hpa`

## API Access Control
- **Admission Controller**
  - 리소스 요청이 승인될 때, 실제로 API 서버가 요청될 때 추가적인 검사 및 수정 작업 수행하는 컴포넌트
  - 리소스 생성/업데이트 전 마지막 검증 단계 + 클러스터 보안/정책/규칙 enforce
    - 요청 수락/거부/수정
  - 역할
    1. 리소스 생성 전 검증
    2. 리소스 수정 전 적용
    3. 보안 정책
    4. 감사 및 로깅
  - kubectl 요청 flow
    - `kubectl` > `Authentication` > `Authorization` > `Admission Controller` > `Create Pod`
  - 종류
    1. NamespaceLifecycle: Namespace 존재여부 확인
    2. LimitRanger: pod/container 리소스 제한 강제
    3. ServiceAccount: pod에 SA 자동 추가
    4. NodeRestriction: 노드에 관련 리소스 제한
    5. PodSecurityPolicy: 파드 보안 정책 적용하여 파드 실행환경 정의
    6. MutatingAdmissionWebhook: 리소스 생성/업데이트 -> 리소스 수정
    7. ValidatingAdmissionWebhook: 리소스 요청 검증/유효한지 확인
    8. AlwaysPullImages: 파드 생성시, 이미지 항상 최신 상태로 풀하도록 강제
    9. PodTolerationRestriction: 특정 taint에 대해 toleration 명시해야만 생성 가능 제한
    10. ResourceQuota: 네임스페이스 단위 리소스 제한
  - `kube-apiserver --enable-admission-plugins=MutatingAdmissionWebhook,ValidatingAdmissionWebhook,PodSecurityPolicy`

## Cluster Maintenance
- **OS upgrade**
  - 기본 명령어
  ```
  > k drain node-1      # 특정 노드 내 작업들을 타 노드로 이관. 노드 끔
  > k uncorden node-1   # 해당 노드 다시 스케줄링 대상으로 ON
  > k corden node-2     # 새로운 pod가 스케줄링 되지 않도록 마킹
  ```
  - drain 하는 시점에 Pod는 다음으로 관리되어야 함
    - ReplicationController
    - ReplicaSet
    - Job
    - DaemonSet
    - StatefulSet

- **Cluster upgrade process**
  - 클러스터 최근 마이너 3버전 (ex. 1.11 ~ 1.13) 지원
  - 업그레이드 추천은 마이너 하나씩 올리기
  - GCP는 클릭 몇번으로 업그레이드 가능
  - 직접: `> kubeadm upgrade plan`, `> kubeadm upgrade apply`
  - 마스터 부터 업그레이드 추천. 워커 노드에서 구동 중인 것들은 마스터 없이 그대로 유지됨
    - kubectl, scheduling, self-healing 등 마스터 관장 기능은 못쓰지만, 돌아가고 있는건 돌아감

- **Backup and Restore Methods**
  - Backup 대상은 다음과 같음
  - [Resource Config]
    - 리소스가 선언형으로 yaml 파일로 되어 있다면, redeploy 쉬움 `> k apply -f ~.yaml`
    - 아니라면, kube-apiserver에서 모든 구성 가져올 수 있음
      - `> k get all --all-namespace -o yaml > all-deploy.yaml`
  - [ETCD Cluster]
    - 클러스터 상태 저장 / 마스터 노드에 저장
    - etcd service에 (`--data-dir=/var/lib/etcd` 에 디렉토리 저장)
    - `> etcdctl snapshot save snap.db` => 해당 이름으로 저장
    - `> etcdctl snapshot restore snap.db --data-dir=/var/lib/etcd-for-backup` => 복원
    - 이후...
    ```
    > systemctl damon-reload
    > systemctl etcd restart
    > service kube-apiserver start
    ```

## Kubernetes Security
- **Authentication(인증)**
  - Files - Username/Password
  - Files - Username/Tokens
    - csv와 같은 파일로 kube-apiserver에 사용자 설정 가능
    - volume-mount + 안정성 이슈로 비추
  - Certificates
  - External Authentication Providers - LDAP
  - Service Accounts: 유저 직관리

- **TLS in k8s**
  - Server Certificates for Servers
    - kube-api server (apiserver.crt / apiserver.key)
    - etcd server (etcdserver.crt / etcdserver.key)
    - kubelet server (kubelet.crt / kubelet.key)

- **kubeconfig**
  - kubeconfig을 통해 클러스터/사용자/네임스페이스/인증 메커니즘 정보 관리 가능
    - kubeconfig: 클러스터에 대한 접근을 구성하는데 사용되는 파일
    - 어떤 클러스터에, 어떤 인증 정보로, 어떤 네임스페이스에서 명령 실행할지 결정
    - `kubectl`은 `$HOME/.kube/config` 디렉토리에서 kubeconfig 파일 찾음
    - 우리가 kubeapi 서버(`kubectl`)에 tls 요청 없이 기본빵으로 요청할 수 있게 하는 요소
      - 클러스터가 RBAC을 사용하면, `kubeconfig`에 서비스 계정 토큰 포함되어 있으면 TLS 없이 인증서 접속 가능
  - 구성요소
    - clusters: 쿠버네티스 API 서버 정보를 포함 (서버 주소/인증서)
    - contexts: `cluster`+`user`+`namespace` 조합으로 환경 정의
    - users(credentials): 인증 정보를 포함 (TLS, 토큰, 기본 인증 등)
    ```yaml
    apiVersion: v1
    kind: Config
    clusters:
    - name: my-cluster
      cluster: 
        server: https://my-cluster.example.com  # API 서버 주소
        certificate-authority: /path/to/ca.crt  # 클러스터의 CA 인증서
    contexts:
    - name: my-context
      context:
        cluster: my-cluster
        user: my-user
        namespace: default                      # 기본 네임스페이스
    users:
    - name: my-user
      user:
        client-certificate: /path/to/client.crt # 사용자 인증서
        client-key: /path/to/client.key         # 사용자 개인 키
    current-context: my-context                 # 활성화된 컨텍스트
    ```
  - 주요 명령어
    - `> k config view`
    - `> k config current-context`
    - `> k config use-context my-context`

- **Authorization(인가)**
  - [Node Auth]
    - 노드의 요청을 제한하는 특별한 권한 부여 모드
    - 자신이 호스팅하는 Pod와 관련된 리소스에 대해서만 접근 가능
    - 노드는 특정 API 경로에만 접근 가능: `/api/v1/nodes/<node-name>`
  - [RBAC Auth]
    - 사용자의 역할 기반으로 리소스 접근 제어
    - 구성요소
      - Role: 특정 네임스페이스에서 권한 설정
      ```yaml
      kind: Role
      apiVersion: rbac.authorization.k8s.io/v1
      metadata:
        namespace: default
        name: pod-reader
      rules:
      - apiGroups: [""]
        resources: ["pods"]
        verbs: ["get", "list"]
      ```
      - ClusterRole: 클러스터 전체에서 권한 설정
      - RoleBinding: 특정 사용자/그룹에게 롤 부여
      - ClusterRoleBinding: 클러스터 전체에서 ClusterRole 부여
  - [ABAC Auth]
    - RBAC 보다 유연한, 정책 JSON 기반 파일로 권한 부여
    - 쿠버 API 서버 실행시 `--authorization-policy-file=policy.json` 옵션 필요
    ```json
    {
      "apiVersion": "abac.authorization.kubernetes.io/v1beta",
      "kind": "Policy",
      "spec": {
        "user": "alice",
        "namespace": "default",
        "resource": "pods",
        "readonly": true
      }
    }
    ```
    - RBAC 보다 어려워 잘 사용 X
  - [Webhook Mode]
    - 외부 서비스에서 관리할 때 유용
    - 방식: 요청 API 서버로 인입 > API 서버가 Webhook 서버에 요청 전달 > Webhook 서버가 allow/deny
    ```yaml
    apiVersion: v1
    kind: Config
    clusters:
    - name: example
      cluster:
        server: https://webhook-auth-server.example.com/authz
    ```
    
- **Role-Based Access Control**
  - 쿠버네티스에서 사용자-리소스간 권한을 제어하는 핵심 메커니즘
    - Role | 특정 네임스페이스 내에서 리소스에 대한 권한 정의
    - RoleBinding | 특정 네임스페이스에서 Role을 사용자/그룹에 부여
    - ClusterRole | 클러스터 전체에서 리소스에 대한 권한 정의
    - ClusterRoleBinding | 클러스터 전체에서 ClusterRole을 사용자/그룹에 부여
  - [Role]
    - 네임스페이스에서만 적용. 네임스페이스 내 리소스 접근 권한 정의
    - `pods`, `services`, `deployments` 같은 리소스 접근 설정 가능
    ```yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      namespace: default
      name: pod-reader
    rules:
    - apiGroups: [""]
      resources: ["pods"]
      verbs: ["get", "list", "watch"]
    ```
  - [RoleBinding]
    - 특정 namespace에서 Role을 사용자/그룹/서비스 계정에 부여
    ```yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: RoleBinding
    metadata:
      name: pod-reader-binding
      namespace: default
    subjects:
    - kind: User
      name: alice
      apiGroup: rbac.authorization.k8s.io
    roleRef:
      kind: Role
      name: pod-reader
      apiGroup: rbac.authorization.k8s.io
    ``` 
  - [ClusterRole]
    - 클러스터 전체에서 사용되는 Role
    - 네임스페이스가 없는 리소스에 대한 권한 정의 (node, pv)
    ```yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRole
    metadata:
      name: pod-reader
    rules:
    - apiGroups: [""]
      resources: ["pods"]
      verbs: ["get", "list", "watch"]
    ```
  - [ClusterRoleBinding]
    - 클러스터 전체에서 ClusterRole을 사용자, 그룹, 서비스 계정에 부여
    ```yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: pod-reader-binding
    subjects:
    - kind: User
      name: alice
      apiGroup: rbac.authorization.k8s.io
    roleRef:
      kind: ClusterRole
      name: pod-reader
      apiGroup: rbac.authorization.k8s.io
    ```

- **ServiceAccount**
  - 쿠버네티스 Pod와 API 서버가 안전하게 상호작용할 수 있도록 인증 제공하는 계정
    - 기본 Pod에 Secret Mount 해서 kube-api 서버에 접근 가능하도록 할 수 있음
    - metrics 서버가 pod로 띄워지면 필요할 수 있겠다
  - `User`와 다르게 `ServiceAccount`는 Pod 내부에서 실행되는 어플리케이션이 쿠버 API 호출할 수 있도록 도와줌
  - 예시)
    ```yaml
    # ServiceAccount
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: prometheus
      namespace: monitoring
    ```
    ```yaml
    # ClusterRole
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRole
    metadata:
      name: prometheus-role
    rules:
      - apiGroups: [""]
        resources:
          - nodes
          - nodes/metrics
          - nodes/stats
          - pods
          - services
          - endpoints
        verbs: ["get", "list", "watch"]
    ```
    ```yaml
    # ClusterRoleBinding
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: prometheus-binding
    subjects:
      - kind: ServiceAccount
        name: prometheus
        namespace: monitoring
    roleRef:
      kind: ClusterRole
      name: prometheus-role
      apiGroup: rbac.authorization.k8s.io
    ```
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: prometheus
      namespace: monitoring
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: prometheus
      template:
        metadata:
          labels:
            app: prometheus
        spec:
          serviceAccountName: prometheus  # ✅ ServiceAccount 적용
          containers:
          - name: prometheus
            image: prom/prometheus
            ports:
            - containerPort: 9090
    ```

## Network
- **Network Policy**
  - 기본적으로 Pod는 서로 통신 가능. 정책을 통해 트래픽 ingress/egress 제어 가능
    - ingress: 인입, egress: 반출
  - 네트워크 플러그인(CNI, Calico 등)이 지원해야 적용됨
  ```yaml
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
    name: db-policy
  spec:
    podSelector:
      matchLabels:
        role: db
    policyTypes:
    - Ingress
    ingress:
    - from:
      - podSelector:
          matchLabels:
            name: api-pod
        namespaceSelector:
          matchLabels:
            name: prod
      ports:
      - protocol: TCP
        port: 3306
  ```

- **리눅스 네트워크**
  - 기본 개념
    - [Switching]
      - LAN 내에서 사용되는 패킷을 전달하는 방식 중 하나
      - MAC 주소 기반 목적지 포트로 전달
      - Layer2(데이터 링크 계층) 에서 작동
      - ex) 사무실에서 여러 컴퓨터 연결/인터넷 사용에는 스위치 사용
    - [Routing]
      - 네트워크 간의 패킷 전달 (2개 이상의 다른 네트워크 연결)
      - 라우터는 IP주소를 기반으로 네트워크 간 패킷 전달
      - Layer3(네트워크 계층) 에서 작동
      - ex) 인터넷에 연결된 여러 네트워크 간 데이터 전달 역할
    - [Gateway]
      - 다양한 네트워크 연결 장치. 서로 다른 프로토콜 사용하는 네트워크 간 데이터 통신 중계
      - 사설 네트워크 - 공인 인터넷 네트워크 연결 장치
      - ex) 집/회사 네트워크에서 사용하는 인터넷 공유기는 게이트웨이
    - [NAT(Network Address Translation)]
      - 내부 네트워크의 사설 IP 주소와 외부 네트워크 공인 IP 주소 변환 담당 기술
      - 주로 사설 네트워크 장치들이 공인 IP 주소 공유하여 외부와 통신
      - NAT는 내부 네트워크에서 발신되는 패킷의 소스 IP 주소를 공인 IP 주소로 변환하여 외부 네트워크로 전송

  - 네트워크 인터페이스
    - [Bridge]
      - 두 개 이상의 네트워크 연결 장치. 동일 네트워크 내 패킷 전달
      - 분할된 네트워크 연결: 하나의 논리적 네트워크 처럼 연결
      - 스위치와 유사하게 동작. 여러 포트를 갖춘 스위치라고 봐도 무방
    - [VLAN]
      - 물리적으로는 동일한 네트워크에 속하지만, 논리적으로는 다른 네트워크로 분리
  
  - 리눅스 호스트를 라우터로 사용하려면?
    - IP 라우팅 활성화 + 네트워크 인터페이스간 트래픽 전달할 수 있는 구성
      - `ip route` 명령 사용해 라우팅 테이블 수정
      - 호스트가 네트워크 간 데이터 중계할 수 있도록 설정
    1. IP 포워딩 활성화
      - 다른 네트워크 간 데이터 전달 역할. 
      - 리눅스 호스트가 타 네트워크 간 패킷 전달 가능
      - `echo 1 > /proc/sys/net/ipv4/ip_forward`
    2. 라우팅 설정
      - 어떤 트래픽이 어디로 가야하는지 설정
      - `ip route add` 명령을 통해 특정 네트워크로 향하는 라우트 추가 가능
      - ex) `192.168.2.0/24` 네트워크로 향하는 트래픽을 `192.168.1.1` 게이트웨이를 통해 전달하기
        - `ip route add 192.168.2.0/24 via 192.168.1.1`
    3. 네트워크 인터페이스에 IP 할당
      - 여러 네트워크에 연결되려면, 각 네트워크 인터페이스에 IP 주소 설정
      - 리눅스 호스트가 라우터로 동작하려면 네트워크 인터페이스에 IP 주소 할당
      - `eth0`에 `192.168.1.1` IP 할당
      - `ip addr add 192.168.1.1/24 dev eth0`
      - `ip addr add 192.168.2.1/24 dev eth1`
    4. 패킷 포워딩 규칙 설정
      - 외부 네트워크(인터넷) 연결되기 위해선, 리눅스 서버가 내부 네트워크 사설 IP -> 공인 IP 변경해주는 NAT 필요
      - `iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE`
        - eth1에 연결된 내부 네트워크 트래픽을 eth0의 공인 IP로 변경해 인터넷 나가게 함
      - 해당 리눅스 서버가 인터넷에 연결된 다른 라우터 뒤에 있다면, 그 라우터를 기본 게이트웨이로 설정하자
      - ex. 인터넷 연결이 있는 라우터 IP 주소가 `192.168.1.1` 이라면, 리눅스 서버에 기본 게이트웨이는 다음과 같이 설정
        - `ip route add default via 192.168.1.1`

- **Pod Networking**
  - 요구사항
    - 각 Pod는 고유한 ip address 있을 것
    - 각 Pod는 같은 노드 내 다른 Pod와 소통할 수 있을 것
    - 각 Pod는 다른 노드 내 다른 Pod들과 NAT 설정 없이 소통할 수 있을 것
  - Pod로 생성되는 시점에 network 설정을 담은 script들이 함께 실행되면서 도커 컨테이너 브릿지/쿠버 네트워크 필요 세팅 일어남
    1. Create veth pair
    2. Attach veth pair
    3. Assign IP Address
    4. Bring up interface

- **CNI**
  - 컨테이너 네트워크 설정하고 관리하는 표준 인터페이스
  - 기능
    - IP 할당
    - 네트워크 플러그인
    - Pod 간 네트워크 통신
    - 네트워크 정책 관리
  - CNI 플러그인: Calico/Flannel/Weave/Cilium
  - `kubelet.service`
  ```
  ExecStart=/usr/local/bin/kubelet \\
    --config=/var/lib/kubelet/kubelet-config.yaml \\
    --container-runtime=remote \\
    --container-runtime-endpoint=unix:///var/run/containerd/containerd.sock \\
    --kubeconfig=/var/lib/kubelet/kubeconfig  \\
    --network-plugin=cni  \\ 
    --cni-bin-dir=/opt/cni/bin \\
    --cni-conf-dir=/etc/cni/net.d \\
  ```

- **DNS**
  - coreDNS를 통한 DNS 관리
    - configMap을 통한 설정 관리
  - 역할
    1. 서비스 이름을 통한 서비스 디스커버리: `my-service.default.svc.cluster.local`
    2. Pod 이름을 통한 통신: `my-pod.default.svc.cluster.local`
    3. 네임스페이스와 서비스 이름을 통한 통신
    4. DNS의 자동 생성과 관리
    5. DNS의 역할과 주요 리소스

- **Ingress**
  - 개요
    - Ingress: 클러스터 내부의 서비스로 외부 트래픽을 라우팅 하는 역할
      - 쿠버 내부에서는 Service(내부 IP)를 통해 접근 가능하지만,
      - 쿠버 외부에서는 NodePort/LoadBalancer를 사용해야 함 (하지만 이 방식은 확장성 부족)
    - Ingress를 통해 도메인 기반 라우팅, SSL/TLS 관리, 다중 서비스 라우팅 기능 제공
  - 주요 기능
    1. 도메인 기반 라우팅
       - foo.example.com -> service-a | bar.example.com -> service-b
    2. path 기반 라우팅
       - /api -> backend-service, /web -> frontend-service
    3. TLS/SSL
       - Ingress를 통한 HTTPS 트래픽 관리
       - kubectl을 통한 TLS 인증서 -> HTTPS
    4. 리버스 프로시
       - Ingress 내부 앞단에서 로드 밸런서 역할 수행가능
    5. 다양한 Ingress 컨트롤러
       - Nginx/Traefik/HAProxy/AWS ALB Ingress Controller/GCE Ingress Controller

- **LoadBalancer**
  - 개요
    - 쿠버에서 `LoadBalancer` 타입의 서비스를 사용하면, **클라우드 제공자**의 LB 자동 생성하여 외부에서 서비스 직접 접근할 수 있게 해줌
    - AWS/GCP/Azure 등 클라우드 환경에서 사용 (기본 지원)
    - 로컬 쿠버 환경 (ex. Minikube, BareMetal) 에서는 별도 설정 필요
  - 동작 방식
    1. 클라우드 제공자의 로드 밸런서 자동 생성
    2. 외부에서 접근할 수 있는 공인 IP 할당
    3. 로드 밸런서가 내부 쿠버 노드들의 특정 포트로 트래픽 전달
    4. 서비스가 내부 파드로 트래픽 분배
  - LoadBalancer 서비스 설정 방법
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: nginx-service
    spec:
      type: LoadBalancer
      selector:
        app: nginx
      ports:
        - protocol: TCP
          port: 80         # 외부에서 접근할 포트
          targetPort: 80   # Pod에서 사용하는 포트
    
    # NAME            TYPE           CLUSTER-IP      EXTERNAL-IP       PORT(S)        AGE
    # nginx-service   LoadBalancer   10.100.200.1    34.125.56.78      80:30201/TCP   5m
    ```

- **Gateway API**
  - 개요
    - Ingress 보다 유연하고 강력한 트래픽 제어 기능 표준 API
    - 클라우드 네이티브 환경에서 더 확장성 있게 동작
    - 로드밸런서/게이트웨이/서비스 메시 등 다양한 네트워크 기능 통합
    - Ingress는 HTTPS 만 처리가능하나, Gateway API는 TCP/gRPC 등 L4도 관리 가능
  - Gateway API 주요 개념
    1. GatewayClass (로드밸런서 타입 정의)
    ```yaml
    apiVersion: gateway.networking.k8s.io/v1
    kind: GatewayClass
    metadata:
      name: my-gateway-class
    spec:
      controllerName: example.com/gateway-controller
    ```
    2. Gateway (Ingress 역할 수행)
    ```yaml
    apiVersion: gateway.networking.k8s.io/v1
    kind: Gateway
    metadata:
      name: my-gateway
    spec:
      gatewayClassName: my-gateway-class
      listeners:
      - protocol: HTTP
        port: 80
    ```
    3. HTTPRoute/TCPRoute (트래픽 라우팅 설정)
    ```yaml
    apiVersion: gateway.networking.k8s.io/v1
    kind: HTTPRoute
    metadata:
      name: my-route
    spec:
      parentRefs:
      - name: my-gateway
      rules:
      - matches:
        - path:
            type: Prefix
            value: /api
        backendRefs:
        - name: my-backend-service
          port: 8080
    ```

## Storage
- **Docker Storage**
  - File System: `/var/lib/docker/volumes` 가 있음
  - 도커 Layered architecture
    - 도커의 Dockerfile은 겹겹이 레이어로 저장되며, 재사용됨
  - volumes(pv)
    - `> docker volume create data-volume`
      - 해당 명령어를 통해 `/var/lib/docker/data-volume`이 생김
    - `> docker run -v data_volume:/var/lib/mysql_mysql`

- **Volumes**
  - 사실 도커 컨테이너는 잠깐 살다가 가는게 본질 (데이터도 같이 폐기)
  - 쿠버에서도 Pod는 일시적. Volume 붙여 해결
    - 다양한 File solution이 제공됨. 
    - NFS, ceph, flocker, scaleIO, AWS EBS, Azure Disk, google persistence disk 등

- **Persistent Volume**
  - 클러스터 전체에서 통용되는 storage volume
  - 스토리지(PV) 미리 생성해두고, 어플리케이션은 PVC를 통해 PV 요청하는 방식
  ```yaml
  apiVersion: v1
  kind: PersistentVolume
  metadata:
    name: my-pv
  spec:
    capacity:
      storage: 10Gi                         # 10Gi 스토리지 제공
    accessModes:
      - ReadWriteOnce                       # 하나의 노드에서 읽기/쓰기 가능
    persistentVolumeReclaimPolicy: Retain   # PVC 삭제에도 데이터 유지
    storageClassName: standard
    nfs:
      path: /exported/data                  # NFS 서버의 경로
      server: 192.168.1.100                 # NFS 서버 주소
  ```
  - Reclaim 정책
    - Retain: PV 삭제되지 않고, 수동으로 클린업
    - Recycle: PV 데이터 삭제하고 초기화하여 다시 사용
    - Delete: PVC 삭제시, 바인딩된 PV도 삭제

- **Persistent Volume Claim**
  - pv는 어드민이 만든다. pvc는 유저가 하나의 pv와 1:1 관계
  - 동작 과정
    1. 관리자가 PV 생성해둠
    2. Pod가 PVC를 생성하여 필요한 스토리지 요청
    3. 쿠버가 PV-PVC 자동으로 바인딩
    4. Pod에서 PVC를 마운트하여 사용
    5. PVC 삭제되면, PV는 정책에 따라 삭제 or 재사용
  - PVC 선언
    ```yaml
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: my-pvc
    spec:
      accessModes:
        - ReadWriteOnce             # 하나의 노드에서만 읽기/쓰기
      resources:
        requests:
          storage: 10Gi
      storageClassName: standard    # PVC가 바인딩될 PV 찾을 때 사용
    ```
  - Pod에 PVC 연결
    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: my-pod
    spec:
      containers:
      - name: my-container
        image: nginx
        volumeMounts:  # PVC의 데이터를 Pod내 mountPath에 마운트하여 사용해주세요!
        - name: my-volume
          mountPath: /usr/share/nginx/html
      volumes:
      - name: my-volume
        persistentVolumeClaim:
          claimName: my-pvc
    ```

## High Availability
- **Control Plane**
  - 한 대만 뒀다가 고장나면 답이 없음. SPOF 방지를 위한 클러스터 내 요소 중복 설치 권장
  - API 서버 앞단에 LB를 배치하는 것이 일반적

- **ETCD**
  - Read 요청 O, Write 요청은 선택된 리더에게 몰빵
    - 리더가 차후 타 노드에 Write 복사를 진행
    - 리더는 RAFT 알고리즘을 통해 선출
  - 데이터 일관성 유지를 위해 Quorom(N/2+1)을 만족하는 etcd 노드 수가 필요함
    - etcd 노드를 짝수로 운영하면 낭비가 되니, 항상 홀수개로 운영하는 것이 일반적

## Helm
- **개요**
  - 쿠버 어플리케이션에 너무 많은 Yaml 파일이 작성되면
    - 환경 및 구성 관리가 어려움
    - 중복도 많고, 롤백도 어렵고...
  - 하나의 어플리케이션 처럼, 쿠버 환경에서 패키지 설치/관리 역할을 Helm에게 맡김
    - 리눅스의 APT와 유사
  - [장점]
    - 배포 자동화 : 여러 YAML 파일을 하나의 Helm 차트로 묶어서 배포 가능
    - 환경별 설정 적용 : 템플릿 엔진을 통해 환경별 설정 쉽게 변경 가능 (values.yaml)
    - 버전 관리 : 어플리케이션 버전 관리 Helm으로 가능, 롤백도 쉬움
    - 의존성 관리 : `charts/` 하위 Helm Chart 포함하여 서비스 배포 가능

- **Helm Chart**
  - 쿠버 어플리케이션 정의하는 패키지 템플릿
  - YAML 파일 묶어서 재사용 가능하게 함
  - 환경별 변수 (values.yaml) 적용으로 중복 최소화
  ```
  myapp/
   ├── Chart.yaml          # Chart의 메타정보 (이름, 버전 등)
   ├── values.yaml         # 기본 설정값 (사용자 입력 가능)
   ├── templates/          # Kubernetes 리소스(YAML) 템플릿
   │   ├── deployment.yaml
   │   ├── service.yaml
   │   ├── configmap.yaml
   │   └── _helpers.tpl    # 템플릿 함수 정의
   └── charts/             # 다른 차트(의존성) 포함 가능
  ```

- **Helm Release**
  - Chart를 기반으로 쿠버 클러스터에 실제 배포된 인스턴스
  - `helm install` 실행시, 차트 기반으로 쿠버 리소스 생성 => 이게 릴리즈
  - Helm은 배포된 릴리즈 추적/관리, 롤백 가능

- **Helm Repository**
  - https://artifacthub.io/
  - Helm Chart를 저장하는 곳이 따로 또 있음
  - 강의 예시에서는 워드프레스를 그냥 앱 구동하듯 다운 받고 install 해서 설치해서 사용했음.
  ```
  > helm repo add bitnami https://~
  > helm install my-release bitnami/wordpress
  > helm list
  > helm uninstall my-release
  > helm upgrade my-release bitnami/wordpress --set replicaCount=5
  > helm rollback my-release 1
  ```

- **Helm 사용처**
  - CI/CD 파이프라인 자동 배포
  - Prometheus/Grafana/Nginx Ingress 등 자주 사용하는 어플리케이션 배포
  - MSA 환경에서 Helm Chart 적용
  - 쿠버에서 어플리케이션 배포/업그레이드/롤백

## Kustomize
- **개요**
  - 기존 YAML을 유지하면서, YAML overlay 방식으로 쿠버네티스 리소스를 커스터마이징 할 수 있도록 도와줌
  - 쿠버 기본 내장이라 설치없이 사용 가능
  - Helm은 템플릿 문법이 있어서 읽기 어려울 수 있지만, kustomize는 그냥 YAML

- **사용법**
  1. Kustomization.yaml
    ```yaml
    apiVersion: kustomize.config.k8s.io/v1beta1
    kind: Kustomization
    resources:
      - base/deployment.yaml
      - base/service.yaml
      - base/configmap.yaml
    ```
  2. Overlays
    ```yaml
    # overlays/dev/kustomization.yaml
    apiVersion: kustomize.config.k8s.io/v1beta1
    kind: Kustomization
    resources:
      - ../../base
    patches:
      - target:
          kind: Deployment
          name: my-app
        patch: |-
          - op: replace
            path: /spec/replicas
            value: 2
    ```
  - 기본 리소스 적용: `kubectl apply -k overlays/dev/`
  - YAML 생성 미리보기: `kubectl kustomize overlays/dev/`
