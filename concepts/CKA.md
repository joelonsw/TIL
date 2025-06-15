## CKA
*참고: https://learn.kodekloud.com/user/courses/udemy-labs-certified-kubernetes-administrator-with-practice-tests/module/22051647-8ef0-4f24-8551-caa14ec77d40/lesson/e57ddf3f-4325-4ba3-8a94-833762ec631b*  

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
    ```yaml
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