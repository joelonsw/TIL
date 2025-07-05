## CKA
*참고: https://learn.kodekloud.com/user/courses/udemy-labs-certified-kubernetes-administrator-with-practice-tests/module/22051647-8ef0-4f24-8551-caa14ec77d40/lesson/e57ddf3f-4325-4ba3-8a94-833762ec631b*  
*참고: https://sunrise-min.tistory.com/entry/2025-CKA-%ED%95%A9%EA%B2%A9-%ED%9B%84%EA%B8%B0-%EC%9C%A0%ED%98%95-%EB%B3%80%EA%B2%BD-%EB%8C%80%EC%9D%91%EB%B2%95-%EB%B0%8F-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC-%EB%AC%B8%EC%A0%9C-%EA%B2%BD%ED%97%98-%EA%B3%B5%EC%9C%A0?category=1104944*   
*참고: https://sunrise-min.tistory.com/entry/2025-CKA-%EC%8B%9C%ED%97%98-%EC%A4%80%EB%B9%84-%ED%95%B5%EC%8B%AC-%EC%9A%94%EC%95%BD*  

### CKA 준비 후기
- crictl, journalctl을 사용하는 트러블 슈팅 문제 출제
- 설치 유형에 대한 대비가 필요
- ingress/gateway/httproute 이해가 있을 것
- CRD, Helm, Kustomize 이해할 것
- 문제 끝까지 읽을 것!

### 필요한 쿠버네티스 설치
- **deb 패키지 설치**
  - `cri-docker`: 쿠버네티스에서 도커 엔진을 컨타임으로 사용할 수 있게 해주는 어댑터
  - cri를 직접적으로 지원하지 않는 도커를 위해, `cri-dockerd`로 설치
  ```
  # 패키지 설치
  $ dpkg -i ~/cri-dockerd_0.3.9.3-0.ubuntu-focal_amd.deb
  
  # 서비스 활성화 및 상태 확인
  $ sudo systemctl enable --now cri-docker  
  $ sudo systemctl status cri-docker
  ```

- **`/etc/sysctl.d/k8s.conf`**
  - 리눅스 커널 파라미터를 영구적으로 설정하는 파일
  - 해당 파일에 쿠버네티스 클러스터 운영에 필요한 네트워크 커널 파라미터 명시해두면, 시스템 부팅시 자동적용
  - 주요 설정
    - `net.ipv4.ip_forward = 1` : 리눅스 커널이 IP 포워딩 허용. 컨테이너/노드 간 네트워크 통신 가능해짐
    - `net.bridge.bridge-nf-call-iptables = 1` : 브릿지 네트워크를 통해 전달되는 패킷도 iptables에서 필터링 할 수 있음
    - `net.bridge.bridge-nf-call-ip6tables = 1` : IPv6 패킷도 마찬가지로 ip6tables에서 필터링 가능
  ```
  $ cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
  net.ipv4.ip_forward = 1
  EOF
  ```

- **CNI - Calico**
  - CNI: 컨테이너 런타임 <-> 네트워크 플러그인 상호작용 표준화 인터페이스
    - kubelet이 파드 생성 시, CNI 플러그인을 호출하여 네트워크 구성 자동화
  - 문제의 조건에 따라 설치할 CNI가 달라짐
    - NetworkPolicy를 지원해야 한다는 문제가 있다면, Calico를 설치하자. 
    - Flannel 기본모드는 NetworkPolicy 지원 X
  ```
  # calico는 create로 설치
  $ k create -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.2/manifests/tigera-operator.yaml
  
  # 테스트 (command 안써도 -- 뒤로 도커의 기본 Entrypoint로 동작)
  k run test1 --image=busybox --restart=Never -- sleep 3600
  k run test2 --image=busybox --restart=Never -- sleep 3600
  k exec test1 -- ping -c 4 test2
  
  # calico pod 확인
  k get pods -n=kube-system
  ```

- **CNI - Flannel**
  ```
  # flannel은 apply로 설치
  $ k apply -f <https://github.com/flannel-io/flannel/releases/download/v0.26.1/kube-flannel.yml
  
  # 확인
  $ k get po -n kube-flannel
  ```

### Mock Exam 1
- **Q1. Multi-Container Pod**
  - env에서 `valueFrom.fieldRef.fieldPath` 를 통해 해당 pod에 사용될 변수를 지정할 수 있음
  - shell script에서 `while true; do ~; done` 패턴을 통해 무한 루프 안에서 뭔가를 지정할 수 있음. 
  - 두 개의 서로 다른 container에서 임의의 공간을 같이 공유하기 위해서는 pod 자체의 volume을 활용하여 나누어 사용 가능.
    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: mc-pod
      namespace: mc-namespace
    spec:
      containers:
      - name: mc-pod-1
        image: nginx:1-alpine
        env:
          - name: NODE_NAME
            valueFrom:
              fieldRef:
                fieldPath: spec.nodeName
      - name: mc-pod-2
        image: busybox:1
        command: ['sh', '-c', 'while true; do date; sleep 1; done > /var/log/shared/date.log']
        volumeMounts:
        - mountPath: /var/log/shared
          name: test-vol
      - name: mc-pod-3
        image: busybox:1
        command: ['sh', '-c', 'tail -f /var/log/shared/date.log']
        volumeMounts:
        - mountPath: /var/log/shared
          name: test-vol
      volumes:
      - name: test-vol
        emptyDir:
          sizeLimit: 1Gi
    ```

- **Q2. cri-docker 설치**
  - CRI-Dockerd: 쿠버네티스에서 Docker를 사용할 수 있게 해주는 중간 다리
    - 쿠버에서 컨테이너 실행하려면 CRI라는 표준 인터페이스 필요
    - 하지만 Docker에서는 CRI 직접 지원하지 않음. 
    - CRI-Dockerd => 쿠버네티스에서 Docker를 사용할 수 있도록 해주는 플러그인
    ```
    $ dpkg -i cri-docker_0.3.16.3-0.debian.deb
    $ systemctl start cri-docker
    $ systemctl status cri-docker
    $ systemctl enable cri-docker  # 시스템 시작시에 자동 시작되도록 설정
    $ systemctl is-enabled cri-docker
    ```

- **Q4. expose로 간단하게 service 구성**
  - expose 명령어로 pod/deployment에 대해 자동으로 Service를 생성할 수 있음
  - expose도 결국 service 간단히 생성하는 명령어
    - `k expose pod messaging --port=6379 --target-port=6379 --name=messaging-service`
  - 쿠버에서 clusterIp가 잘 붙는지 보기 위해서는...
    - `k run test-client --image=busybox --rm -it -- /bin/sh`
    - `# telnet service-name 6379`

- **Q10. VPA**
  - vpa는 쿠버 기본 리소스가 아니라, CRD. 하지만 얼추 정형화되어 있는 CRD라 좀 중요한 건 외워두자.
  - CRD 정의 아래와 같이 Group: `autoscaling.k8s.io` , kind: `VerticalPodAutoscaler` 사용토록 권장
    ```
    controlplane ~ ➜  k describe crd verticalpodautoscalers.autoscaling.k8s.io
    Name:         verticalpodautoscalers.autoscaling.k8s.io
    Namespace:    
    Labels:       <none>
    Annotations:  api-approved.kubernetes.io: https://github.com/kubernetes/kubernetes/pull/63797
                  controller-gen.kubebuilder.io/version: v0.16.5
    API Version:  apiextensions.k8s.io/v1
    Kind:         CustomResourceDefinition
    Metadata:
      Creation Timestamp:  2025-06-15T11:32:18Z
      Generation:          2
      Resource Version:    2542
      UID:                 54735657-ceeb-4465-8243-57ee74c9a91e
    Spec:
      Conversion:
        Strategy:  None
      Group:       autoscaling.k8s.io
      Names:
        Kind:       VerticalPodAutoscaler
        List Kind:  VerticalPodAutoscalerList
        Plural:     verticalpodautoscalers
        Short Names:
          vpa
        Singular:  verticalpodautoscaler
      Scope:       Namespaced
      Versions:
        Additional Printer Columns:
          Json Path:  .spec.updatePolicy.updateMode
          Name:       Mode
          Type:       string
          Json Path:  .status.recommendation.containerRecommendations[0].target.cpu
          Name:       CPU
          Type:       string
          Json Path:  .status.recommendation.containerRecommendations[0].target.memory
          Name:       Mem
          Type:       string
          Json Path:  .status.conditions[?(@.type=='RecommendationProvided')].status
          Name:       Provided
          Type:       string
          Json Path:  .metadata.creationTimestamp
          Name:       Age
          Type:       date
        Name:         v1
    ```
  - yaml의 기본 골자는 조금 외워두자.
    ```
    controlplane ~ ➜  cat webapp-vpa.yaml 
    apiVersion: autoscaling.k8s.io/v1
    kind: VerticalPodAutoscaler
    metadata:
      name: analytics-vpa
    spec:
      targetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: kkapp-deploy
      updatePolicy:
        updateMode: "Auto"
    ```

- **Q12. helm upgrade**
  - namespace를 명령어 끝마다 명시해줘야해!
    ```
    $  helm list -n=kk-ns
    $  helm repo update 
    $  helm upgrade kk-mock1 kk-mock1/nginx --version=18.1.15 -n=kk-ns
    ```

### killer.sh (CKA-A)
- **Q1. Contexts**
  - kubeconfig file에서 context 정보 추출하여 저장하기
    - `k --kubeconfig /config_path config get-contexts`: 컨텍스트 정보 추출
    - `k --kubeconfig /config_path config get-contexts -o name`: 이름만 추출
    - `k --kubeconfig /config_path config get-contexts -o name > /file_path`
  - 현재 컨텍스트 보기
    - `k --kubeconfig /config_path config current-context`
  - client certificate 데이터 디코딩
    - `k config view` 혹은, 실제 config 파일을 열어 `client-certificate-data` 추출
    - `$ echo base64encodedcertificatedata | base64 -d > /answer`
  - tips: 잘 모르겠으면 `k config -h`

- **Q3. Statefulset scaledown**
  - `pod`가 2개가 있다면, 이를 한개로 scale down
  - 해당 과정에서, pod를 매니지하는 리소스를 찾아보자
  - `k -n test-ns get deploy, ds, sts | grep targetName`
  - `deployment`, `daemonset`, `statefulset`, `replicaset`을 총체적으로 검색
    - `deployment`/`statefulset`/`replicaset`은 `kubernetes scale`로 갯수 조절 가능
    - `daemonset`은 node마다 하나씩 pod가 배포되도록 설계되었기에 scale로 제어 불가능

- **Q4. 가장 먼저 종료될 Pod 찾기**
  - node의 cpu/memory가 한도에 다다랐을 때, 쿠버네티스는 요청된 것 보다 더 많은 리소스를 사용중인 pod를 찾을 것
    - 특정 pod가 request/limit이 지정되어 있지 않다면, 요청보다 더 많이 쓰는 것으로 간주됨
    - 따라서, Pod 중에서 resource request가 정의되어 있지 않은 것을 찾아야 함
  - 방법1)
    - `k describe pods | grep -A 3 -E 'Name|Requests'`: `-E`(extended) / `-A`: 매칭 결과
    ```
    controlplane ~ ✖ k describe pods | grep -E 'Name|Requests'
    Name:             frontend
    Namespace:        default
        Requests:
        ConfigMapName:           kube-root-ca.crt
    Name:             test
    Namespace:        default
        ConfigMapName:           kube-root-ca.crt
    ```
  - 방법2)
    - `k get pod -o jsonpath="{range .items[*]}{.metadata.name}{.spec.containers[*].resources}{'\n'}{end}"`
    ```
    frontend{"limits":{"cpu":"500m","memory":"128Mi"},"requests":{"cpu":"250m","memory":"64Mi"}}
    test{}
    ```

- **Q5. kustomize 사용하기**
  - base 폴더 하위에 kustomize로 사용할 것을 정의해두고, 각 환경별로 덮어쓰고/패치 하면서 사용할 수 있도록 한다. 
  - `k kustomize <stage-name> | k apply -f -`
  ```
  $ controlplane ~/test5 ✖ ls
  base  prod  staging
  
  
  $ controlplane ~/test5/base ➜  ls
  cm.yaml  hpa.yaml  sa.yaml  deployment.yaml  kustomization.yaml
  
  
  $ controlplane ~/test5/base ➜  cat kustomization.yaml 
  apiVersion: kustomize.config.k8s.io/v1beta1
  kind: Kustomization
  resources:
    - deployment.yaml
    - hpa.yaml
    - cm.yaml
    - sa.yaml
  
  
  $ controlplane ~/test5/prod ➜  ls
  api-gateway-deployment.yaml  api-gateway-hpa.yaml  kustomization.yaml
  
  
  $ controlplane ~/test5/prod ➜  cat kustomization.yaml 
  apiVersion: kustomize.config.k8s.io/v1beta1
  kind: Kustomization
  resources:
    - ../base
  namespace: api-gateway-prod
  patches:
    - target:
        kind: Deployment
        name: api-gateway
      path: api-gateway-deployment.yaml
    - target:
        kind: HorizontalPodAutoscaler
        name: api-gateway
      path: api-gateway-hpa.yaml
      
  
  $ controlplane ~/test5/prod ➜  cat api-gateway-deployment.yaml 
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: api-gateway
    labels:
      env: prod
      
  
  $ controlplane ~/test5/prod ➜  cat api-gateway-hpa.yaml 
  apiVersion: autoscaling/v2
  kind: HorizontalPodAutoscaler
  metadata:
    name: api-gateway
  spec:
    maxReplicas: 6
  ```

- **Q7. Node/Pod Resource 사용량**
  - metrics-server를 설치하여 top 명령어를 통해 Node/Pod 사용량을 기록할 수 있음
  - *참고: https://velog.io/@nhj7804/%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A414-error-Metrics-API-not-available*
    1. metric-server 설치: `kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml`
  - `k top node`
  - `k top pod --containers=true`
  - 모르겠으면 -h 호출하자

- **Q8. kubernetes 버전 업그레이드 + 클러스터 Join**
  - *참고: https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/*
  - 요구사항 1. node의 쿠버네티스 버전을 올린뒤
    - `ssh node01`
    - `apt update`
    - `apt show kubectl -a | grep 1.32`
    - `apt install kubectl=1.32.1-1.1 kubelet=1.32.1-1.1`
    - `service kubelet restart`
    - `service kubelet status`
  - 요구사항 2. 쿠버 클러스터에 node를 합류시키세요
    - `ssh controlplane`
    - `kubeadm token create --print-join-command`
    - `kubeadm token list`
    - `ssh node01`
    - `kubeadm join controlplane:6443 --token 6c70qp.34m4fi9q7l3bnucg --discovery-token-ca-cert-hash sha256:2092f9d0d5336377c4d626fa289909d15b4724fcb668e7ab7d441babe671a56c`
    - `service kubelet status`

- **Q9. Pod 안에서 쿠버네티스 API 호출하기**
  - *참고: https://kubernetes.io/docs/tasks/run-application/access-api-from-pod/*
  - service account credential을 활용하면 API 서버와 통신 가능
  - 기본값으로 Pod는 service account와 연계되어 있으며, **해당 service account의 credential token은 filesystem tree 하위에 저장되어 있음**
    - `/var/run/secrets/kubernetes.io/serviceaccount/token`
    - 타 다른 값도 매핑되어 있음
      - certificate bundle: `/var/run/secrets/kubernetes.io/serviceaccount/ca.crt`
      - default namespace: `/var/run/secrets/kubernetes.io/serviceaccount/namespace`
  - 이제 API 호출
    - `k exec podName -it -- sh`
    - `TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)`
    - https 검사 ON
      - `curl -k https://kubernetes.default`: `-k`는 insecure의 약자로, https 유효성 검증 끄고 요청
      - `curl -k https://kubernetes.default/api/v1/secrets`
      - `curl -k https://kubernetes.default/api/v1/secrets -H "Authorization: Bearer ${TOKEN}"`
    - https 검사 OFF
      - `CACERT=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt`
      - `curl --cacert ${CACERT} https://kubernetes.default/api/v1/secrets -H "Authorization: Bearer ${TOKEN}"`
  - 앞서서 kubectl로 검증도 가능!
    - `kubectl auth can-i get secret --as system:serviceaccount:project-joel:secret-reader`

- **Q12. PodAntiAffinity**
  - `podAffinity`: 같은 노드에 붙어라
    - 같은 노드에 떠있어야 통신도 빠르고 좋을 때
    - 나랑 같은 라벨(`labelSelector`) 가진 Pod 있는 `topologyKey`에 나를 넣어줘!
    - `labelSelector`: 누구를 같은 걸로 볼지
    - `topologyKey`: 어떤 단위로 배치할지
  - 예시)
    ```yaml
    spec:
      affinity:
        requiredDuringSchedulingIgnoredDuringExecution:
        - labelSelector:
            matchLabels:
              app: frontend
          topologyKey: kubernetes.io/hostname
    ```
  - `podAntiAffinity`: 다른 노드로 떨어저라
    - 분산하여 파드를 배치함으로써 노드 하나 죽었을 때 대비
    - 나랑 같은 라벨(`labelSelector`)을 가진 Pod 있는 `topologyKey` 에는 가지 말 것!
  - 예시)
    - `id: very-important` 라벨을 가진 Pod를 이미 해당 노드가 가지고 있다면, 거기엔 배치하지 마!
    - `labelSelector`: 누구를 같은 걸로 볼지
    - `topologyKey`: 어떤 단위로 배치할지 (예시 hostname은 노드 단위)
    ```yaml
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                id: very-important
            topologyKey: kubernetes.io/hostname
    ```
    
- **Q13. Gateway Api Ingress**
  - http-header를 기반으로 routing 될 서비스를 구분할 수 있다. 
  ```yaml
  apiVersion: gateway.networking.k8s.io/v1
  kind: HTTPRoute
  metadata:
    name: traffic-director
    namespace: project-r500
  spec:
    parentRefs:
      - name: main
    hostnames:
      - "r500.gateway"
    rules:
      - matches:
          - path:
              type: PathPrefix
              value: /desktop
        backendRefs:
          - name: web-desktop
            port: 80
      - matches:
          - path:
              type: PathPrefix
              value: /mobile
        backendRefs:
          - name: web-mobile
            port: 80
      - matches:
          - path:
              type: PathPrefix
              value: /auto
            headers:  # 여기를 '- headers' 로 지칭한다면, path or headers로 잡힌다고 함. 둘 중 하나의 OR 조건이 아니라 AND 조건이라면 이렇게.
              - type: Exact
                name: user-agent
                value: mobile
        backendRefs:
          - name: web-mobile
            port: 80
      - matches:
          - path:
              type: PathPrefix
              value: /auto
        backendRefs:
          - name: web-desktop
            port: 80
  ```

- **Q14. kube-apiserver의 validation 날짜**
  ```
  controlplane /etc/kubernetes/manifests ➜  cat kube-apiserver.yaml | grep crt
      - --client-ca-file=/etc/kubernetes/pki/ca.crt
      - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
      - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
      - --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt
      - --proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-client.crt
      - --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
      - --tls-cert-file=/etc/kubernetes/pki/apiserver.crt
  ```
  - 이제, tls-cert-file를 복호화해보자.
    - `openssl x509 -noout -text -in /etc/kubernetes/pki/apiserver.crt`
      - `-noout`: 내용을 꺼내지 말고, 본문만 설명
      - `-text`: 사람이 읽을 수 있는 형식
    - `openssl x509 -noout -text -in /etc/kubernetes/pki/apiserver.crt | grep Validity -A2`
  - 또다른 방법으로는 `kubeadm` 사용
    - `kubeadm certs check-expiration`: 언제 만료되는지 나옴
    - `kubeadm certs renew apiserver`: apiserver 인증서 갱신 (실제로 만료날짜 변경됨)

- **Q17. pod w. crictl**
  - `crictl inspect CONTAINER_ID`를 인스펙션 가능
  - `crictl logs CONTAINER_ID`를 통해 로깅 가능
