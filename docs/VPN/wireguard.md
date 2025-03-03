# WireGuard

## Privileges

WireGuard will need some specific privileges to be able to NAT traffic and redirect your requests. Consider using `sysctls` options on your nodes. You need to specify it at kubelet level:

- `net.ipv4.ip_forward`
- `net.ipv4.conf.all.src_valid_mark`

For example in `k0s` :

```yaml
---
apiVersion: k0sctl.k0sproject.io/v1beta1
kind: Cluster
metadata:
  name: fullstack
  user: admin
spec:
  hosts:
    - role: single
      installFlags:
        - --debug
        - --disable-components=autopilot,helm,windows-node,konnectivity-server
        - --kubelet-extra-args="--allowed-unsafe-sysctls=net.ipv4.ip_forward,net.ipv4.conf.all.src_valid_mark"
```

And your also need to specify it at pod level as well as `NET_ADMIN` capability:

```yaml
spec:
  automountServiceAccountToken: false
  containers:
    - image: wgportal/wg-portal:v2
      imagePullPolicy: IfNotPresent
      name: wg-portal
      securityContext:
        capabilities:
          add:
            - NET_ADMIN
  securityContext:
    sysctls:
      - name: net.ipv4.ip_forward
        value: '1'
      - name: net.ipv4.conf.all.src_valid_mark
        value: '1'
```
