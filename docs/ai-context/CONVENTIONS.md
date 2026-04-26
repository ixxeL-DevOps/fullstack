---
description: Coding standards for Helm charts, ApplicationSets, ArgoCD Applications, and manifests
tags: ["Conventions", "Helm", "ArgoCD", "ApplicationSet"]
audience: ["LLMs", "Humans"]
categories: ["Reference[100%]"]
---

# Conventions

## Helm Chart Structure

Every application follows this layout:

```
gitops/manifests/{app}/
├── common/
│   └── common-values.yaml       # Shared values applied to all clusters
├── beelink/
│   ├── Chart.yaml               # Helm wrapper chart (may have upstream dependency)
│   ├── beelink-values.yaml      # Cluster-specific overrides
│   └── templates/               # ExternalSecrets, PVCs, custom resources
└── genmachine/
    ├── Chart.yaml
    ├── genmachine-values.yaml
    └── templates/
```

### Chart.yaml

```yaml
---
apiVersion: v2
name: { app }
version: 1.0.0
dependencies: # Only present if wrapping an upstream chart
  - name: { upstream }
    # renovate: datasource=helm depName={upstream} registryUrl={url}
    version: 1.2.3
    repository: https://...
```

### Value File Naming

- `common/common-values.yaml` — shared configuration (image tags, common labels, feature flags)
- `{cluster}/{cluster}-values.yaml` — cluster-specific overrides (replicas, domain names, storage class, resource limits)

### Release Name

Helm release name always matches the app directory name:

```yaml
helm:
  releaseName: { app }
```

---

## ApplicationSet Convention (Genmachine)

```yaml
---
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: { app }
  namespace: argocd
  annotations:
    argocd.argoproj.io/manifest-generate-paths: .;../common
spec:
  goTemplate: true
  generators:
    - git:
        repoURL: "https://github.com/ixxeL-DevOps/fullstack.git"
        revision: main
        directories:
          - path: "gitops/manifests/{app}/*"
            exclude: false
          - path: "gitops/manifests/{app}/common"
            exclude: true
          - path: "gitops/manifests/{app}/beelink" # only if beelink dir exists
            exclude: true
          - path: "gitops/manifests/{app}/k0s" # legacy — exclude if present
            exclude: true
  template:
    metadata:
      name: "{app}-{{ .path.basenameNormalized }}"
      annotations:
        argocd.argoproj.io/manifest-generate-paths: .;../common
    spec:
      project: { project }
      destination:
        name: "{{ .path.basenameNormalized }}"
        namespace: { namespace }
      sources:
        - path: "gitops/manifests/{app}/{{ .path.basenameNormalized }}"
          repoURL: https://github.com/ixxeL-DevOps/fullstack.git
          targetRevision: main
          helm:
            releaseName: { app }
            valueFiles:
              - $values/gitops/manifests/{app}/common/common-values.yaml
              - $values/gitops/manifests/{app}/{{ .path.basenameNormalized }}/{{ .path.basenameNormalized }}-values.yaml
            ignoreMissingValueFiles: true
        - repoURL: https://github.com/ixxeL-DevOps/fullstack.git
          targetRevision: main
          ref: values
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - Validate=true
          - PruneLast=true
          - RespectIgnoreDifferences=true
          - Replace=false
          - ApplyOutOfSyncOnly=true
          - CreateNamespace=true
          - ServerSideApply=true
        retry:
          limit: 6
          backoff:
            duration: 10s
            factor: 2
            maxDuration: 3m
```

**Important**:

- `manifest-generate-paths: .;../common` appears **twice**: on the ApplicationSet metadata AND the template metadata
- If the app requires namespace labels (e.g., for CA injection), add `managedNamespaceMetadata.labels`
- AppProject must be chosen from the existing list — never create a new project without discussion

---

## ArgoCD Application Convention (Beelink)

Beelink uses plain `Application` CRDs (not ApplicationSets):

```yaml
---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {app}-beelink
  namespace: argocd
spec:
  project: {project}
  destination:
    name: beelink
    namespace: {namespace}
  sources:
    - path: gitops/manifests/{app}/beelink
      repoURL: https://github.com/ixxeL-DevOps/fullstack.git
      targetRevision: main
      helm:
        releaseName: {app}
        valueFiles:
          - $values/gitops/manifests/{app}/common/common-values.yaml
          - $values/gitops/manifests/{app}/beelink/beelink-values.yaml
        ignoreMissingValueFiles: true
    - repoURL: https://github.com/ixxeL-DevOps/fullstack.git
      targetRevision: main
      ref: values
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - Validate=true
      - PruneLast=true
      - RespectIgnoreDifferences=true
      - Replace=false
      - ApplyOutOfSyncOnly=true
      - CreateNamespace=true
      - ServerSideApply=true
    retry:
      limit: 6
      backoff:
        duration: 10s
        factor: 2
        maxDuration: 3m
```

---

## Ingress Convention

```yaml
ingress:
  enabled: true
  ingressClassName: traefik
  annotations:
    cert-manager.io/cluster-issuer: fredcorp-ca
    cert-manager.io/common-name: {app}.{cluster-domain}.fredcorp.com
    traefik.ingress.kubernetes.io/router.entrypoints: websecure
    traefik.ingress.kubernetes.io/service.scheme: https   # only if backend is HTTPS
  hosts:
    - host: {app}.{cluster-domain}.fredcorp.com
      paths:
        - path: /
  tls:
    - secretName: {app}-tls-cert
      hosts:
        - {app}.{cluster-domain}.fredcorp.com
```

Cluster domains:

- Beelink: `k0s-fullstack.fredcorp.com`
- Genmachine: `talos-genmachine.fredcorp.com`

---

## ExternalSecret Convention

```yaml
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: {secret-name}
  namespace: {namespace}
spec:
  refreshInterval: 12h
  secretStoreRef:
    kind: ClusterSecretStore
    name: admin
  target:
    name: {secret-name}
    creationPolicy: Owner
  data:
    - secretKey: {key-in-k8s-secret}
      remoteRef:
        key: {app}/{secret-type}/{cluster}
        property: {vault-key}
```

Vault path convention: `{app}/{secret-type}/{cluster}` — e.g., `wireguard/oidc/beelink`, `vault/bootstrap/genmachine`.

---

## Renovate Annotations

Always annotate version pins so Renovate can update them:

```yaml
# Docker image
image:
  # renovate: datasource=docker depName=ghcr.io/org/app
  tag: "v1.2.3"

# Helm chart dependency
dependencies:
  - name: cert-manager
    # renovate: datasource=helm depName=cert-manager registryUrl=https://charts.jetstack.io
    version: "v1.14.4"
    repository: https://charts.jetstack.io

# GitHub release
# renovate: datasource=github-releases depName=org/repo
version: "0.1.8"
```

---

## Security Context

For non-privileged workloads, apply:

```yaml
securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL

podSecurityContext:
  runAsNonRoot: true
  runAsUser: 65532
  fsGroup: 65532
```

Only use `privileged: true` when accessing host resources (e.g., fstrim via nsenter). Document why.

---

## Namespace Labels

Namespaces that need the CA chain injected:

```yaml
managedNamespaceMetadata:
  labels:
    bundle.chain/inject: enabled
```

---

## Naming Summary

| Resource               | Pattern                               |
| ---------------------- | ------------------------------------- |
| ApplicationSet name    | `{app}`                               |
| Application name       | `{app}-{cluster}`                     |
| Helm release           | `{app}`                               |
| ArgoCD app (generated) | `{app}-{cluster}`                     |
| Vault path             | `{app}/{secret-type}/{cluster}`       |
| K8s Secret (from ESO)  | `{app}-{secret-type}`                 |
| TLS Secret             | `{app}-tls-cert`                      |
| Ingress hostname       | `{app}.{cluster-domain}.fredcorp.com` |
