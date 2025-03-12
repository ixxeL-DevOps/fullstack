# Cilium

**Cilium** is the best choice for Kubernetes CNI, leveraging eBPF technology. You can use Cilium as a CNI but also for LB announcement, Ingress Controller and also Gateway API controller.

## Installation

Cilium should be the first element to deploy in the cluster as postinstall action. One of the purpose of Cilium is to run instead of kube-router, so be sure to disable kube-router when installing your Kubernetes cluster.

For example in Talos (talhelper):

```yaml
cniConfig:
  name: none
```

and patch:

```yaml
- |-
  cluster:
    proxy:
      disabled: true
```

When installing Cilium you need to follow Talos documentation (https://www.talos.dev/v1.9/kubernetes-guides/network/deploying-cilium/)

Minimal install for Cilium in namespace `kube-system`:

```bash
helm install \
    cilium \
    cilium/cilium \
    --namespace kube-system \
    --set ipam.mode=kubernetes \
    --set kubeProxyReplacement=true \
    --set securityContext.capabilities.ciliumAgent="{CHOWN,KILL,NET_ADMIN,NET_RAW,IPC_LOCK,SYS_ADMIN,SYS_RESOURCE,DAC_OVERRIDE,FOWNER,SETGID,SETUID}" \
    --set securityContext.capabilities.cleanCiliumState="{NET_ADMIN,SYS_ADMIN,SYS_RESOURCE}" \
    --set cgroup.autoMount.enabled=false \
    --set cgroup.hostRoot=/sys/fs/cgroup \
    --set k8sServiceHost=localhost \
    --set k8sServicePort=7445
```

If you want Gateway API support just add :

```yaml
--set=gatewayAPI.enabled=true \
--set=gatewayAPI.enableAlpn=true \
--set=gatewayAPI.enableAppProtocol=true
```

On Talos you might need to add : `--set securityContext.privileged=true`

> [!TIP]
> If you deploy Cilium with ArgoCD on Talos, don't forget to add the proper labal to the Cilium namespace `pod-security.kubernetes.io/enforce: privileged`. You can add this section in your application
> `SyncPolicy` parameter:
>
> ```yaml
> managedNamespaceMetadata:
>   labels:
>     pod-security.kubernetes.io/enforce: privileged
> ```

## Configuration : LB announcement

Cilium can be configured for LB announcement in BGP mode and L2 mode. This feature is useful for bare metal and on-premise environment where you usually need a software loadBalancer such as `Metallb` to handle `loadBalancer` services in Kubernetes. In our case we will use L2 for a simple setup.

- https://docs.cilium.io/en/stable/network/l2-announcements/
- https://docs.cilium.io/en/stable/network/lb-ipam/

You need to add following parameters :

```yaml
enableLBIPAM: true
l2announcements:
  enabled: true
devices: eth+
```

The `devices` parameters should be reflecting interfaces name of your nodes.

Then deploy the following additional objects:

```yaml
---
apiVersion: "cilium.io/v2alpha1"
kind: CiliumLoadBalancerIPPool
metadata:
  name: local-pool
  namespace: kube-system
spec:
  blocks:
    - start: "10.0.0.50"
      stop: "10.0.0.70"
---
apiVersion: "cilium.io/v2alpha1"
kind: CiliumL2AnnouncementPolicy
metadata:
  name: default
  namespace: kube-system
spec:
  interfaces:
    - ^eth+
  externalIPs: true
  loadBalancerIPs: true
```

With this configuration you don't need `Metallb` installed in your cluster.

## Configuration : final

As a final result, you can use this `values.yaml` file to deploy Cilium:

```yaml
securityContext:
  privileged: true
  capabilities:
    ciliumAgent: [CHOWN, KILL, NET_ADMIN, NET_RAW, IPC_LOCK, SYS_ADMIN, SYS_RESOURCE, DAC_OVERRIDE, FOWNER, SETGID, SETUID]
    cleanCiliumState: [NET_ADMIN, SYS_ADMIN, SYS_RESOURCE]

priorityClassName: "system-node-critical"
debug:
  enabled: false
gatewayAPI:
  enabled: true
  enableAlpn: true
  enableAppProtocol: true
ipam:
  mode: kubernetes
cgroup:
  autoMount:
    enabled: false
  hostRoot: /sys/fs/cgroup
k8sServiceHost: 127.0.0.1
k8sServicePort: 7445
kubeProxyReplacement: true
ingressController:
  enabled: false

envoy:
  enabled: false
  priorityClassName: "system-node-critical"
operator:
  priorityClassName: "system-node-critical"

enableLBIPAM: true
l2announcements:
  enabled: true
devices: eth+

rollOutCiliumPods: true

localRedirectPolicy: true
```

> [!NOTE]
> In some cases, where you run controlPlane only nodes, be aware of the
> `node.kubernetes.io/exclude-from-external-load-balancers` label that might prevent loabBalancer service to work.
> You might need to disable it in Talos
>
> ```yaml
> - |-
>   - op: remove
>     path: /machine/nodeLabels/node.kubernetes.io~1exclude-from-external-load-balancers
> ```
>
> For `Metallb` there is a specific parameter to ignore such labels:
>
> ```yaml
> speaker:
>   ignoreExcludeLB: true
> ```
