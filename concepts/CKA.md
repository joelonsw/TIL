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
