# Kubernetes (CKA)
*참고: https://kubernetes.io/docs/home/*

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
