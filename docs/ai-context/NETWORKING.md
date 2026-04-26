---
description: Traffic flows, DNS, ingress, certificates, OIDC, and VPN configuration
tags: ["Networking", "Traefik", "Cilium", "MetalLB", "DNS", "OIDC", "WireGuard", "cert-manager"]
audience: ["LLMs", "Humans"]
categories: ["Architecture[90%]", "Reference[85%]"]
---

# Networking

## Traffic Flow

```
Internet / LAN client
        │
        ▼
   AdGuard Home (DNS)
   192.168.1.195
   *.fredcorp.com → MetalLB VIP
        │
        ▼
   MetalLB (L2 mode)
   Beelink: 192.168.1.191
   Genmachine: 192.168.1.160
        │
        ▼
   Traefik Ingress Controller
   TLS termination (cert-manager / Vault PKI)
   Entrypoints: web (80→redirect), websecure (443)
        │
        ▼
   Kubernetes Service → Pod
```

---

## Capsule: TraefikIngress

**Invariant**
All external traffic routes through Traefik via Kubernetes `Ingress` resources. TLS is terminated at Traefik using cert-manager-issued certificates. Traefik entry point `websecure` (443) is the default; `web` (80) redirects to HTTPS.

**Example**

```yaml
ingress:
  enabled: true
  ingressClassName: traefik
  annotations:
    cert-manager.io/cluster-issuer: fredcorp-ca
    cert-manager.io/common-name: vault.talos-genmachine.fredcorp.com
    traefik.ingress.kubernetes.io/router.entrypoints: websecure
  hosts:
    - host: vault.talos-genmachine.fredcorp.com
      paths:
        - path: /
  tls:
    - secretName: vault-tls-cert
      hosts:
        - vault.talos-genmachine.fredcorp.com
```

**Depth**

- Genmachine: LoadBalancer IP `192.168.1.160`, 2 replicas, default cert `genmachine-wildcard`
- Beelink: LoadBalancer IP `192.168.1.191`, 1 replica, default cert `k0s-fullstack-wildcard`
- KubernetesCRD, KubernetesIngress, and Kubernetes Gateway API providers all enabled
- Backend HTTPS: add `traefik.ingress.kubernetes.io/service.scheme: https`
- SeeAlso: `VaultPKI`, `MetalLB`

---

## Capsule: MetalLB

**Invariant**
MetalLB operates in Layer 2 mode, announcing LoadBalancer Service IPs via ARP.

**Depth**

- Beelink IP range: 192.168.1.191–192.168.1.195
- Genmachine IP range: starts at 192.168.1.160
- Traefik always gets the first IP in its range
- AdGuard Home: 192.168.1.195 (shared DNS server for both clusters)

---

## Capsule: CertManagerVaultPKI

**Invariant**
cert-manager issues all TLS certificates using Vault as the PKI backend. The `ClusterIssuer` is named `fredcorp-ca`. The CA chain is injected into namespaces via cert-manager `Bundle` (label `bundle.chain/inject: enabled`).

**Depth**

- CA bundle name: `fredcorp-ca-chain`
- Wildcard certificates for Traefik default TLS: `k0s-fullstack-wildcard`, `genmachine-wildcard`
- Pattern: one TLS secret per app (`{app}-tls-cert`)
- SeeAlso: `TraefikIngress`, `ExternalSecretSync`

---

## DNS

### AdGuard Home

Both clusters use AdGuard Home at `192.168.1.195` as the local DNS server.

Wildcard DNS entries resolve all `*.fredcorp.com` subdomains to MetalLB IPs:

- `*.k0s-fullstack.fredcorp.com` → `192.168.1.191`
- `*.talos-genmachine.fredcorp.com` → `192.168.1.160`

### CoreDNS

Genmachine runs CoreDNS for in-cluster DNS (`cluster.local`). Beelink uses k0s built-in DNS.

### Naming Pattern

| Cluster    | Pattern                               | Example                               |
| ---------- | ------------------------------------- | ------------------------------------- |
| Beelink    | `{app}.k0s-fullstack.fredcorp.com`    | `vault.k0s-fullstack.fredcorp.com`    |
| Genmachine | `{app}.talos-genmachine.fredcorp.com` | `vault.talos-genmachine.fredcorp.com` |

---

## OIDC via Authentik

Authentik is the OIDC identity provider for both clusters. It runs independently on each cluster.

### Provider Configuration Pattern

Each application requiring OIDC needs:

1. An Authentik `OAuth2Provider` (configured via Blueprint or UI)
2. An Authentik `Application` linked to the provider
3. Application-specific OIDC env vars injected via `ExternalSecret` → Kubernetes Secret

### Vault OIDC

```
Authentik discovery URL: https://authentik.{cluster-domain}/application/o/{slug}/
Role: reader (default)
Redirect URIs:
  - https://vault.{cluster-domain}/oidc/callback
  - https://vault.{cluster-domain}/ui/vault/auth/oidc/oidc/callback
```

### WireGuard Portal OIDC

WireGuard Portal uses the `is_admin` claim to grant admin access. This claim is provided via a custom Authentik Scope Mapping:

```python
return {
  "is_admin": ak_is_group_member(request.user, name="Wireguard admins")
}
```

### Homarr OIDC

```yaml
env:
  AUTH_PROVIDERS: credentials,oidc
  AUTH_OIDC_ISSUER: https://authentik.{cluster-domain}/application/o/fullstack-homarr/
  AUTH_OIDC_SCOPE_OVERWRITE: openid email profile groups
  AUTH_OIDC_GROUPS_ATTRIBUTE: groups
```

---

## VPN (WireGuard)

WireGuard Portal (`wg-portal`) is deployed on both clusters. Users authenticate via Authentik OIDC. Admin status is controlled by the `is_admin` OIDC claim mapped from Authentik group membership.

---

## Capsule: CiliumCNI

**Invariant**
Genmachine uses Cilium as CNI, installed at bootstrap before any pods can start. Talos is configured with `cni: none` in `talconfig.yaml`; Cilium is installed via `helmfile.yaml` during bootstrap.

**Depth**

- Beelink uses KubeRouter (built into k0s) — no Cilium on Beelink
- Cilium tolerates `node-role.kubernetes.io/control-plane` — all 3 Talos nodes are control-plane nodes
- KubeProxy replacement enabled (Cilium handles kube-proxy functionality)
- SeeAlso: `DualClusterIsolation`

---

## Network CIDRs (Genmachine)

| Range               | CIDR              |
| ------------------- | ----------------- |
| Pod CIDR            | 10.244.0.0/16     |
| Service CIDR        | 10.96.0.0/12      |
| Node IPs            | 192.168.1.151–153 |
| VIP (control plane) | 192.168.1.150     |
| Traefik LB          | 192.168.1.160     |
