# GitOps-core

> [!CAUTION]
> This structure is opinionated and results from multiple experiences using ArgoCD in enterprise-grade environments.

## Overview

This Git repository serves as the central ArgoCD repository, containing the definition of the ArgoCD deployment itself, as well as the various ArgoCD objects (`Application`, `ApplicationSet`, `AppProject`, etc.).

The installation of ArgoCD follows the [App of Apps pattern](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/#app-of-apps-pattern), a recommended best practice for managing GitOps deployments at scale.

## Repository Structure

Below is the directory structure of the `gitops` repository:

```bash
gitops
├── bootstrap
│   └── kustomization.yaml
├── core
│   ├── appProjects
│   ├── apps
│   └── repos
├── local-storage
│   ├── adguard-data
│   ├── headscale-data
│   └── vault-data
└── manifests
    ├── adguard
    ├── authentik
    ├── crowdsec
    ├── external-secrets
    ├── headscale
    ├── homarr
    ├── local-path-provisioner
    ├── metallb
    ├── traefik
    ├── vault
    └── wireguard
```

### Directory Breakdown

- **`bootstrap/`**: Contains the ArgoCD installation manifests, which can be managed via `kustomization.yaml` or Helm charts.
- **`core/`**: Includes core ArgoCD resources such as `Application`, `ApplicationSet`, and `AppProject` definitions.
- **`local-storage/`** (optional): Used for applications requiring persistent storage, mapped via a local-path provisioner.
- **`manifests/`**: Stores Kubernetes manifests and Helm configurations for different cluster services and applications.

## Multi-Environment Setup

For a structured multi-environment approach, the `manifests` directory is organized as follows:

```bash
gitops/manifests/
├── metallb
│   ├── k0s
│   │   ├── Chart.yaml
│   │   ├── k0s-values.yaml
│   │   └── templates
│   ├── talos
│   │   ├── Chart.yaml
│   │   ├── talos-values.yaml
│   │   └── templates
│   └── values
│       └── common-values.yaml
└── traefik
    ├── k0s
    │   ├── Chart.yaml
    │   ├── k0s-values.yaml
    │   └── templates
    ├── talos
    │   ├── Chart.yaml
    │   ├── talos-values.yaml
    │   └── templates
    └── values
        └── common-values.yaml
```

Each application directory contains subdirectories for different environments (`k0s`, `talos`), allowing environment-specific Helm values while maintaining shared configurations in `common-values.yaml`.

## ApplicationSet Usage

To efficiently deploy applications while supporting multiple environments, `ApplicationSet` is utilized:

```yaml
---
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cert-manager
  namespace: argocd
  annotations:
    argocd.argoproj.io/manifest-generate-paths: .;../values
spec:
  goTemplate: true
  generators:
  - git:
      repoURL: 'https://github.com/ixxeL-DevOps/fullstack.git'
      revision: main
      directories:
        - path: 'gitops/manifests/cert-manager/*'
          exclude: false
        - path: 'gitops/manifests/cert-manager/values/*'
          exclude: true
  template:
    metadata:
      name: 'cert-manager-{{ .path.basenameNormalized }}'
      annotations:
        argocd.argoproj.io/manifest-generate-paths: .;../values
    spec:
      project: infra-security
      destination:
        name: '{{ .path.basenameNormalized }}'
        namespace: cert-manager
      sources:
      - path: 'gitops/manifests/cert-manager/{{ .path.basenameNormalized }}'
        repoURL: https://github.com/ixxeL-DevOps/fullstack.git
        targetRevision: main
        helm:
          valueFiles:
            - $values/gitops/manifests/cert-manager/values/common-values.yaml
            - $values/gitops/manifests/cert-manager/{{ .path.basenameNormalized }}/{{ .path.basenameNormalized }}-values.yaml
      - repoURL: https://github.com/ixxeL-DevOps/fullstack.git
        targetRevision: main
        ref: values
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - Validate=true
          - PruneLast=false
          - RespectIgnoreDifferences=true
          - Replace=false
          - ApplyOutOfSyncOnly=true
          - CreateNamespace=true
          - ServerSideApply=true
```

The ApplicationSet is annotated following [ArgoCD optimization recommendations](https://argo-cd.readthedocs.io/en/stable/operator-manual/high_availability/#manifest-paths-annotation).


### Key Features
- **Multi-environment support**: Uses directory-based environment segregation.
- **Hierarchical Helm values**: Supports multiple value files (`common-values.yaml` and environment-specific values).
- **Automated synchronization**: Ensures ArgoCD keeps applications up-to-date and reconciled with Git.
- **Flexible exclusions**: Allows selective inclusion of manifests while ignoring specific files if necessary.

By leveraging `ApplicationSet`, managing deployments across multiple clusters and environments becomes more scalable and maintainable.