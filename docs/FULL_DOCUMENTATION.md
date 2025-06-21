# ixxeL-DevOps Fullstack - Complete Documentation

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture Overview](#architecture-overview)
3. [Taskfile.yaml Analysis](#taskfileyaml-analysis)
4. [ArgoCD Ecosystem](#argocd-ecosystem)
5. [Talos Ecosystem](#talos-ecosystem)
6. [Infrastructure Components](#infrastructure-components)
7. [GitOps Workflow](#gitops-workflow)
8. [Security & Secrets Management](#security--secrets-management)
9. [Automation & CI/CD](#automation--cicd)
10. [Monitoring & Observability](#monitoring--observability)

---

## 🎯 Overview

This repository represents a modern, cloud-native home laboratory infrastructure built on GitOps principles. It combines Infrastructure as Code (IaC) with continuous deployment to create a fully automated, scalable, and maintainable home lab environment.

### Key Technologies
- **Kubernetes Distributions**: k0s (lab environment) & Talos (production environment)
- **GitOps**: ArgoCD for continuous deployment
- **Container Runtime**: Containerd with Cilium CNI
- **Automation**: go-task (Taskfile) for operational tasks
- **Secrets Management**: HashiCorp Vault + External Secrets Operator
- **Infrastructure**: Virtualized on Proxmox VE
- **Monitoring**: Prometheus, Grafana, Loki stack

---

## 🏗️ Architecture Overview

```mermaid
graph TB
    subgraph "Infrastructure Layer"
        PM[Proxmox VE Cluster]
        PM --> K0S[k0s Cluster - BeeLink]
        PM --> TALOS[Talos Cluster - GenMachine]
    end
    
    subgraph "GitOps Layer"
        GH[GitHub Repository]
        GH --> ARGO[ArgoCD]
        ARGO --> K0S
        ARGO --> TALOS
    end
    
    subgraph "Application Layer"
        ARGO --> APPS[Applications]
        APPS --> AUTH[Authentik - SSO]
        APPS --> VAULT[HashiCorp Vault]
        APPS --> TRAEFIK[Traefik - Ingress]
        APPS --> MONITOR[Monitoring Stack]
        APPS --> STORAGE[Storage Solutions]
    end
    
    subgraph "Automation Layer"
        TASK[Taskfile Automation]
        RENOVATE[Renovate Bot]
        ACTIONS[GitHub Actions]
    end
    
    GH --> RENOVATE
    GH --> ACTIONS
    TASK --> PM
    TASK --> K0S
    TASK --> TALOS
```

### Multi-Environment Strategy

```mermaid
flowchart TD
    subgraph "Production Environment"
        TALOS_PROD[Talos Cluster<br/>GenMachine Hardware<br/>192.168.1.151-153]
        TALOS_PROD --> CILIUM[Cilium CNI]
        TALOS_PROD --> ETCD[etcd Storage]
    end
    
    subgraph "Lab Environment"
        K0S_LAB[k0s Cluster<br/>BeeLink Hardware<br/>Resource Optimized]
        K0S_LAB --> KONNECTIVITY[Konnectivity]
        K0S_LAB --> SQLITE[SQLite Backend]
    end
    
    subgraph "Shared Services"
        ARGO_CENTRAL[Central ArgoCD]
        VAULT_CENTRAL[Central Vault]
        MONITOR_CENTRAL[Central Monitoring]
    end
    
    ARGO_CENTRAL --> TALOS_PROD
    ARGO_CENTRAL --> K0S_LAB
    VAULT_CENTRAL -.-> TALOS_PROD
    VAULT_CENTRAL -.-> K0S_LAB
```

---

## ⚙️ Taskfile.yaml Analysis

The main Taskfile.yaml serves as the orchestration hub for all operational tasks across the infrastructure.

### Core Structure

```yaml
version: '3'
vars:
  K0S_ROOT: '{{.ROOT_DIR}}/infra/k0s'
  TALOS_ROOT: '{{.ROOT_DIR}}/infra/talos'
  GITOPS_ROOT: '{{.ROOT_DIR}}/gitops'
  VAULT_ENDPOINT: 'https://vault.k0s-fullstack.fredcorp.com'
  AUTHENTIK_ENDPOINT_GENMACHINE: 'https://authentik.talos-genmachine.fredcorp.com'
  K8S_API: 'talos-cluster.genmachine.fredcorp.com'
```

### Task Modules

```mermaid
graph LR
    MAIN[Main Taskfile] --> K0S[k0s Tasks]
    MAIN --> TALOS[Talos Tasks]
    MAIN --> BOOTSTRAP[Bootstrap Tasks]
    MAIN --> VAULT[Vault Tasks]
    MAIN --> ESO[External Secrets]
    MAIN --> SOPS[SOPS Encryption]
    MAIN --> PROXMOX[Proxmox Management]
    MAIN --> HELM[Helm Operations]
    MAIN --> K8S[Kubernetes Utils]
    MAIN --> LINT[Linting & Quality]
    MAIN --> DOCS[Documentation]
    MAIN --> PRECOMMIT[Pre-commit Hooks]
```

### Key Task Categories

#### 1. Infrastructure Management
- **Proxmox**: VM creation, management, and configuration
- **Talos**: Cluster bootstrapping, configuration, and lifecycle
- **k0s**: Cluster deployment and management

#### 2. GitOps Operations
- **ArgoCD**: Application deployment and synchronization
- **Helm**: Chart management and templating
- **Kustomize**: Manifest customization

#### 3. Security & Secrets
- **SOPS**: File encryption and decryption
- **Vault**: Secret management and policy configuration
- **External Secrets**: Secret synchronization

#### 4. Development & Quality
- **Pre-commit**: Code quality enforcement
- **Linting**: YAML, Helm, and Kubernetes manifest validation
- **Documentation**: MkDocs site generation

---

## 🔄 ArgoCD Ecosystem

ArgoCD serves as the GitOps engine, implementing the "App of Apps" pattern for scalable application management.

### ArgoCD Architecture

```mermaid
graph TD
    subgraph "ArgoCD Core"
        ARGO_SERVER[ArgoCD Server]
        ARGO_CONTROLLER[Application Controller]
        ARGO_REPO[Repository Server]
        ARGO_DEX[Dex OIDC]
    end
    
    subgraph "Application Management"
        APP_PROJECTS[AppProjects]
        APPLICATIONS[Applications]
        APP_SETS[ApplicationSets]
    end
    
    subgraph "Target Clusters"
        CLUSTER_TALOS[Talos Cluster]
        CLUSTER_K0S[k0s Cluster]
    end
    
    ARGO_CONTROLLER --> APP_PROJECTS
    APP_PROJECTS --> APPLICATIONS
    APP_PROJECTS --> APP_SETS
    
    APPLICATIONS --> CLUSTER_TALOS
    APPLICATIONS --> CLUSTER_K0S
    APP_SETS --> CLUSTER_TALOS
    APP_SETS --> CLUSTER_K0S
    
    ARGO_DEX --> AUTHENTIK[Authentik SSO]
```

### Repository Structure

```mermaid
flowchart TD
    subgraph "GitOps Repository Structure"
        ROOT[gitops/]
        ROOT --> BOOTSTRAP[bootstrap/]
        ROOT --> CORE[core/]
        ROOT --> MANIFESTS[manifests/]
        ROOT --> STORAGE[local-storage/]
        
        BOOTSTRAP --> GENMACHINE_BOOT[genmachine/]
        BOOTSTRAP --> BEELINK_BOOT[beelink/]
        
        CORE --> PROJECTS[appProjects/]
        CORE --> APPS[apps/]
        CORE --> REPOS[repos/]
        
        MANIFESTS --> APP_DIRS[Application Directories]
        APP_DIRS --> ENV_SPECIFIC[Environment Specific]
        APP_DIRS --> COMMON_VALUES[Common Values]
    end
```

### Application Projects

```mermaid
graph LR
    subgraph "AppProjects"
        ARGOCD_PROJ[argocd]
        CORE_PROJ[core]
        MONITORING_PROJ[monitoring]
        NETWORK_PROJ[network]
        SECURITY_PROJ[security]
        STORAGE_PROJ[storage]
        TOOLS_PROJ[tools]
    end
    
    ARGOCD_PROJ --> ARGOCD_APPS[ArgoCD Applications]
    CORE_PROJ --> CORE_APPS[Core Infrastructure]
    MONITORING_PROJ --> MONITOR_APPS[Prometheus, Grafana, Loki]
    NETWORK_PROJ --> NETWORK_APPS[Traefik, Cilium, MetalLB]
    SECURITY_PROJ --> SECURITY_APPS[Vault, Cert-Manager, Authentik]
    STORAGE_PROJ --> STORAGE_APPS[CSI Drivers, MinIO]
    TOOLS_PROJ --> TOOL_APPS[Utility Applications]
```

### ApplicationSet Pattern

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cert-manager
  namespace: argocd
spec:
  generators:
    - git:
        repoURL: "https://github.com/ixxeL-DevOps/fullstack.git"
        revision: main
        directories:
          - path: "gitops/manifests/cert-manager/*"
            exclude: false
          - path: "gitops/manifests/cert-manager/values/*"
            exclude: true
  template:
    metadata:
      name: "cert-manager-{{ .path.basenameNormalized }}"
    spec:
      project: security
      destination:
        name: "{{ .path.basenameNormalized }}"
        namespace: cert-manager
      sources:
        - path: "gitops/manifests/cert-manager/{{ .path.basenameNormalized }}"
          repoURL: https://github.com/ixxeL-DevOps/fullstack.git
          targetRevision: main
          helm:
            valueFiles:
              - $values/gitops/manifests/cert-manager/values/common-values.yaml
              - $values/gitops/manifests/cert-manager/{{ .path.basenameNormalized }}/{{ .path.basenameNormalized }}-values.yaml
```

---

## 🐧 Talos Ecosystem

Talos Linux provides an immutable, API-driven Kubernetes platform optimized for security and simplicity.

### Talos Cluster Architecture

```mermaid
graph TB
    subgraph "Talos Cluster - GenMachine"
        VIP[VIP: 192.168.1.150<br/>talos-cluster.genmachine.fredcorp.com]
        
        subgraph "Control Plane Nodes"
            TALOS1[talos-1.genmachine.fredcorp.com<br/>192.168.1.151<br/>Control Plane + Worker]
            TALOS2[talos-2.genmachine.fredcorp.com<br/>192.168.1.152<br/>Control Plane + Worker]
            TALOS3[talos-3.genmachine.fredcorp.com<br/>192.168.1.153<br/>Control Plane + Worker]
        end
        
        VIP -.-> TALOS1
        VIP -.-> TALOS2
        VIP -.-> TALOS3
        
        TALOS1 <--> ETCD[etcd Cluster]
        TALOS2 <--> ETCD
        TALOS3 <--> ETCD
    end
    
    subgraph "Network Layer"
        CILIUM_NET[Cilium CNI<br/>eBPF Dataplane<br/>No kube-proxy]
        CILIUM_NET --> POD_CIDR[Pod CIDR: 10.244.0.0/16]
        CILIUM_NET --> SVC_CIDR[Service CIDR: 10.96.0.0/12]
    end
    
    subgraph "Storage Layer"
        LONGHORN[Longhorn Distributed Storage]
        PROXMOX_CSI[Proxmox CSI Plugin]
        NFS_CSI[NFS CSI Driver]
    end
    
    TALOS1 --> CILIUM_NET
    TALOS2 --> CILIUM_NET
    TALOS3 --> CILIUM_NET
    
    TALOS1 --> LONGHORN
    TALOS2 --> LONGHORN
    TALOS3 --> LONGHORN
```

### Talos Configuration Hierarchy

```mermaid
flowchart TD
    subgraph "Talos Configuration"
        TALCONFIG[talconfig.yaml<br/>Main Configuration]
        TALSECRET[talsecret.sops.yaml<br/>Encrypted Secrets]
        
        TALCONFIG --> CLUSTER_CONFIG[Cluster Configuration]
        TALCONFIG --> MACHINE_CONFIG[Machine Configuration]
        
        CLUSTER_CONFIG --> ETCD_CONFIG[etcd Configuration]
        CLUSTER_CONFIG --> API_CONFIG[API Server Configuration]
        CLUSTER_CONFIG --> CNI_CONFIG[CNI Configuration]
        
        MACHINE_CONFIG --> KUBELET_CONFIG[Kubelet Configuration]
        MACHINE_CONFIG --> SYSTEM_CONFIG[System Configuration]
        MACHINE_CONFIG --> NETWORK_CONFIG[Network Configuration]
    end
    
    subgraph "Generated Artifacts"
        TALOS_CONFIGS[Node Configurations]
        KUBECONFIG[Kubernetes Config]
        TALOS_CONFIG[Talos Config]
    end
    
    TALCONFIG --> TALOS_CONFIGS
    TALSECRET --> TALOS_CONFIGS
    TALOS_CONFIGS --> KUBECONFIG
    TALOS_CONFIGS --> TALOS_CONFIG
```

### Key Talos Features

#### 1. **Immutable Infrastructure**
- Read-only root filesystem
- API-driven configuration
- Atomic updates via system extensions

#### 2. **Security Hardening**
- No shell access by default
- Minimal attack surface
- Secure by default configuration

#### 3. **Kubernetes Optimization**
- Optimized for container workloads
- Built-in Kubernetes support
- Efficient resource utilization

#### 4. **System Extensions**
```yaml
systemExtensions:
  officialExtensions:
    - siderolabs/amd-ucode      # AMD microcode updates
    - siderolabs/amdgpu         # AMD GPU support
    - siderolabs/iscsi-tools    # iSCSI support for Longhorn
    - siderolabs/util-linux-tools # Additional Linux utilities
```

### Talos Bootstrap Process

```mermaid
sequenceDiagram
    participant USER as User
    participant TASK as Taskfile
    participant TALHELPER as Talhelper
    participant TALOS as Talos Nodes
    participant K8S as Kubernetes
    
    USER->>TASK: task talos:bootstrap cluster=genmachine
    TASK->>TALHELPER: Generate configurations
    TALHELPER->>TALHELPER: Process talconfig.yaml
    TALHELPER->>TALHELPER: Decrypt talsecret.sops.yaml
    TALHELPER-->>TASK: Generated configs
    
    TASK->>TALOS: Apply machine configs
    TALOS->>TALOS: Bootstrap etcd cluster
    TALOS->>K8S: Start Kubernetes components
    TASK->>TALOS: Fetch kubeconfig
    TALOS-->>TASK: Kubeconfig file
    
    Note over USER,K8S: Cluster Ready for Workloads
```

---

## 🔧 Infrastructure Components

### Core Infrastructure Stack

```mermaid
graph TB
    subgraph "Compute Layer"
        PROXMOX[Proxmox VE Cluster]
        PROXMOX --> VM_K0S[k0s VMs<br/>BeeLink Hardware]
        PROXMOX --> VM_TALOS[Talos VMs<br/>GenMachine Hardware]
    end
    
    subgraph "Network Layer"
        ROUTER[Home Router/Firewall]
        ROUTER --> VLAN_MGMT[Management VLAN]
        ROUTER --> VLAN_K8S[Kubernetes VLAN]
        
        VLAN_K8S --> LB_METALLB[MetalLB Load Balancer]
        VLAN_K8S --> INGRESS[Traefik Ingress]
    end
    
    subgraph "Storage Layer"
        PROXMOX_STORAGE[Proxmox Storage]
        NFS_SERVER[NFS Server]
        BACKUP_TARGET[Backup Targets]
        
        PROXMOX_STORAGE --> CSI_PROXMOX[Proxmox CSI]
        NFS_SERVER --> CSI_NFS[NFS CSI]
        CSI_PROXMOX --> LONGHORN[Longhorn]
        CSI_NFS --> VOLSYNC[VolSync Backups]
    end
    
    subgraph "Security Layer"
        VAULT_HA[HashiCorp Vault HA]
        AUTHENTIK_SSO[Authentik SSO]
        CERT_MANAGER[Cert-Manager]
        
        VAULT_HA --> ESO[External Secrets Operator]
        AUTHENTIK_SSO --> OIDC[OIDC Integration]
        CERT_MANAGER --> ACME[ACME Certificates]
    end
```

### Application Portfolio

```mermaid
mindmap
  root((Applications))
    Infrastructure
      ArgoCD
      Cilium
      MetalLB
      Traefik
      Cert-Manager
      External Secrets
    Security & Identity
      HashiCorp Vault
      Authentik SSO
      Kyverno Policies
    Monitoring & Observability
      Prometheus Stack
      Grafana Dashboards
      Loki Logging
      Metrics Server
      Popeye Cluster Scanner
    Storage & Backup
      Longhorn
      MinIO S3
      VolSync
      CSI Drivers
    Network & DNS
      AdGuard Home
      Technitium DNS
      Wireguard VPN
    Development & CI/CD
      GitHub Actions Runner
      Stakater Reloader
      System Upgrade Controller
    Utilities & Dashboard
      Homarr Dashboard
      Crossplane
      Spegel Registry Cache
```

---

## 🔄 GitOps Workflow

### GitOps Process Flow

```mermaid
flowchart TD
    subgraph "Source Control"
        GITHUB[GitHub Repository]
        FEATURE[Feature Branch]
        MAIN[Main Branch]
        
        FEATURE --> PR[Pull Request]
        PR --> MAIN
    end
    
    subgraph "Automation"
        RENOVATE[Renovate Bot]
        ACTIONS[GitHub Actions]
        PRECOMMIT[Pre-commit Hooks]
        
        RENOVATE --> PR
        ACTIONS --> BUILD[Build & Test]
        PRECOMMIT --> LINT[Linting & Validation]
    end
    
    subgraph "GitOps Engine"
        ARGOCD[ArgoCD]
        SYNC[Sync Process]
        HEALTH[Health Checks]
        
        MAIN --> ARGOCD
        ARGOCD --> SYNC
        SYNC --> HEALTH
    end
    
    subgraph "Target Infrastructure"
        K8S_CLUSTERS[Kubernetes Clusters]
        APPS[Applications]
        MONITORING[Monitoring]
        
        HEALTH --> K8S_CLUSTERS
        K8S_CLUSTERS --> APPS
        APPS --> MONITORING
    end
    
    MONITORING -.-> ARGOCD
```

### Deployment Strategies

#### 1. **Application Deployment**
```mermaid
sequenceDiagram
    participant DEV as Developer
    participant GIT as GitHub
    participant ARGO as ArgoCD
    participant K8S as Kubernetes
    participant VAULT as Vault
    
    DEV->>GIT: Push changes
    GIT->>ARGO: Webhook notification
    ARGO->>ARGO: Detect configuration drift
    ARGO->>VAULT: Fetch secrets
    VAULT-->>ARGO: Return secrets
    ARGO->>K8S: Apply manifests
    K8S->>K8S: Deploy/Update applications
    K8S-->>ARGO: Sync status
    ARGO-->>DEV: Deployment notification
```

#### 2. **Secret Management Flow**
```mermaid
flowchart LR
    subgraph "Secret Sources"
        VAULT_KV[Vault KV Store]
        VAULT_PKI[Vault PKI]
        EXTERNAL[External APIs]
    end
    
    subgraph "Secret Management"
        ESO[External Secrets Operator]
        SECRET_STORE[SecretStore/ClusterSecretStore]
        EXT_SECRET[ExternalSecret]
    end
    
    subgraph "Kubernetes"
        K8S_SECRET[Kubernetes Secret]
        POD[Application Pod]
    end
    
    VAULT_KV --> SECRET_STORE
    VAULT_PKI --> SECRET_STORE
    EXTERNAL --> SECRET_STORE
    
    SECRET_STORE --> ESO
    EXT_SECRET --> ESO
    ESO --> K8S_SECRET
    K8S_SECRET --> POD
```

---

## 🔐 Security & Secrets Management

### HashiCorp Vault Architecture

```mermaid
graph TB
    subgraph "Vault HA Cluster"
        VAULT1[Vault Node 1<br/>Active]
        VAULT2[Vault Node 2<br/>Standby]
        VAULT3[Vault Node 3<br/>Standby]
        
        VAULT1 <--> STORAGE[Integrated Storage<br/>Raft Consensus]
        VAULT2 <--> STORAGE
        VAULT3 <--> STORAGE
    end
    
    subgraph "Authentication Methods"
        OIDC_AUTH[OIDC<br/>via Authentik]
        K8S_AUTH[Kubernetes<br/>Service Accounts]
        APPROLE[AppRole<br/>for CI/CD]
    end
    
    subgraph "Secret Engines"
        KV_ENGINE[KV Secrets Engine]
        PKI_ENGINE[PKI Engine<br/>Certificate Authority]
        TRANSIT[Transit Engine<br/>Encryption as a Service]
    end
    
    subgraph "Policies & Access"
        ADMIN_POLICY[Administrator Policy]
        APP_POLICIES[Application Policies]
        READONLY_POLICY[Read-only Policy]
    end
    
    OIDC_AUTH --> VAULT1
    K8S_AUTH --> VAULT1
    APPROLE --> VAULT1
    
    VAULT1 --> KV_ENGINE
    VAULT1 --> PKI_ENGINE
    VAULT1 --> TRANSIT
    
    ADMIN_POLICY --> VAULT1
    APP_POLICIES --> VAULT1
    READONLY_POLICY --> VAULT1
```

### Authentik SSO Integration

```mermaid
graph LR
    subgraph "Identity Sources"
        LDAP[LDAP/AD]
        LOCAL[Local Users]
        SOCIAL[Social Providers]
    end
    
    subgraph "Authentik Core"
        AUTH_CORE[Authentik Core]
        FLOWS[Authentication Flows]
        POLICIES[Authorization Policies]
    end
    
    subgraph "Applications"
        VAULT_APP[HashiCorp Vault]
        ARGOCD_APP[ArgoCD]
        GRAFANA_APP[Grafana]
        MINIO_APP[MinIO]
        HOMARR_APP[Homarr Dashboard]
    end
    
    LDAP --> AUTH_CORE
    LOCAL --> AUTH_CORE
    SOCIAL --> AUTH_CORE
    
    AUTH_CORE --> FLOWS
    FLOWS --> POLICIES
    
    POLICIES --> VAULT_APP
    POLICIES --> ARGOCD_APP
    POLICIES --> GRAFANA_APP
    POLICIES --> MINIO_APP
    POLICIES --> HOMARR_APP
```

### Certificate Management

```mermaid
flowchart TD
    subgraph "Certificate Authorities"
        ROOT_CA[Root CA<br/>Vault PKI]
        INT_CA[Intermediate CA<br/>Vault PKI]
        ACME_CA[ACME CA<br/>Let's Encrypt]
    end
    
    subgraph "Cert-Manager"
        CERT_MGR[Cert-Manager Controller]
        VAULT_ISSUER[Vault Issuer]
        ACME_ISSUER[ACME Issuer]
    end
    
    subgraph "Certificate Consumers"
        INGRESS_CERTS[Ingress Controllers]
        APP_CERTS[Application TLS]
        SERVICE_MESH[Service Mesh]
    end
    
    ROOT_CA --> INT_CA
    INT_CA --> VAULT_ISSUER
    ACME_CA --> ACME_ISSUER
    
    VAULT_ISSUER --> CERT_MGR
    ACME_ISSUER --> CERT_MGR
    
    CERT_MGR --> INGRESS_CERTS
    CERT_MGR --> APP_CERTS
    CERT_MGR --> SERVICE_MESH
```

---

## 🤖 Automation & CI/CD

### GitHub Actions Workflows

```mermaid
graph LR
    subgraph "Triggers"
        PUSH[Push to Main]
        PR[Pull Request]
        SCHEDULE[Scheduled]
        MANUAL[Manual Trigger]
    end
    
    subgraph "Quality Gates"
        PRECOMMIT[Pre-commit Checks]
        LINT[Linting & Validation]
        SECURITY[Security Scanning]
        TESTS[Unit Tests]
    end
    
    subgraph "Deployment"
        BUILD[Build Artifacts]
        DEPLOY[Deploy to Staging]
        PROMOTE[Promote to Production]
        ROLLBACK[Rollback Capability]
    end
    
    PUSH --> PRECOMMIT
    PR --> PRECOMMIT
    SCHEDULE --> SECURITY
    MANUAL --> DEPLOY
    
    PRECOMMIT --> LINT
    LINT --> TESTS
    TESTS --> BUILD
    BUILD --> DEPLOY
    DEPLOY --> PROMOTE
    PROMOTE --> ROLLBACK
```

### Renovate Configuration

```mermaid
flowchart TD
    subgraph "Dependency Sources"
        DOCKER[Docker Images]
        HELM[Helm Charts]
        GITHUB[GitHub Releases]
        TERRAFORM[Terraform Modules]
    end
    
    subgraph "Renovate Bot"
        SCANNER[Dependency Scanner]
        UPDATER[Update Generator]
        PR_CREATOR[PR Creator]
    end
    
    subgraph "Update Strategies"
        AUTO_MERGE[Auto-merge<br/>Minor/Patch]
        MANUAL_REVIEW[Manual Review<br/>Major Updates]
        SCHEDULED[Scheduled Updates]
        GROUPED[Grouped Updates]
    end
    
    DOCKER --> SCANNER
    HELM --> SCANNER
    GITHUB --> SCANNER
    TERRAFORM --> SCANNER
    
    SCANNER --> UPDATER
    UPDATER --> PR_CREATOR
    
    PR_CREATOR --> AUTO_MERGE
    PR_CREATOR --> MANUAL_REVIEW
    PR_CREATOR --> SCHEDULED
    PR_CREATOR --> GROUPED
```

### Task Automation Framework

```mermaid
graph TB
    subgraph "Task Categories"
        INFRA[Infrastructure Tasks]
        K8S[Kubernetes Tasks]
        SECURITY[Security Tasks]
        QUALITY[Quality Assurance]
        DOCS[Documentation]
    end
    
    subgraph "Infrastructure Tasks"
        PROXMOX_TASKS[Proxmox Management]
        TALOS_TASKS[Talos Operations]
        K0S_TASKS[k0s Operations]
        NETWORK_TASKS[Network Configuration]
    end
    
    subgraph "Kubernetes Tasks"
        DEPLOY_TASKS[Deployment Tasks]
        DEBUG_TASKS[Debugging Tools]
        BACKUP_TASKS[Backup Operations]
        MONITOR_TASKS[Monitoring Tasks]
    end
    
    subgraph "Security Tasks"
        VAULT_TASKS[Vault Operations]
        SOPS_TASKS[SOPS Encryption]
        CERT_TASKS[Certificate Management]
        SECRET_TASKS[Secret Management]
    end
    
    INFRA --> PROXMOX_TASKS
    INFRA --> TALOS_TASKS
    INFRA --> K0S_TASKS
    INFRA --> NETWORK_TASKS
    
    K8S --> DEPLOY_TASKS
    K8S --> DEBUG_TASKS
    K8S --> BACKUP_TASKS
    K8S --> MONITOR_TASKS
    
    SECURITY --> VAULT_TASKS
    SECURITY --> SOPS_TASKS
    SECURITY --> CERT_TASKS
    SECURITY --> SECRET_TASKS
```

---

## 📊 Monitoring & Observability

### Observability Stack

```mermaid
graph TB
    subgraph "Data Collection"
        PROMETHEUS[Prometheus]
        LOKI[Loki]
        TEMPO[Tempo - Tracing]
        NODE_EXPORTER[Node Exporter]
        CADVISOR[cAdvisor]
        KUBE_STATE[Kube State Metrics]
    end
    
    subgraph "Visualization"
        GRAFANA[Grafana]
        DASHBOARDS[Custom Dashboards]
        ALERTS[Alert Manager]
    end
    
    subgraph "Storage"
        PROMETHEUS_STORAGE[Prometheus TSDB]
        LOKI_STORAGE[Loki Object Storage]
        TEMPO_STORAGE[Tempo Storage]
    end
    
    subgraph "Applications"
        APP_METRICS[Application Metrics]
        APP_LOGS[Application Logs]
        APP_TRACES[Application Traces]
    end
    
    NODE_EXPORTER --> PROMETHEUS
    CADVISOR --> PROMETHEUS
    KUBE_STATE --> PROMETHEUS
    APP_METRICS --> PROMETHEUS
    
    APP_LOGS --> LOKI
    APP_TRACES --> TEMPO
    
    PROMETHEUS --> PROMETHEUS_STORAGE
    LOKI --> LOKI_STORAGE
    TEMPO --> TEMPO_STORAGE
    
    PROMETHEUS --> GRAFANA
    LOKI --> GRAFANA
    TEMPO --> GRAFANA
    
    GRAFANA --> DASHBOARDS
    PROMETHEUS --> ALERTS
```

### Monitoring Architecture

```mermaid
flowchart LR
    subgraph "Data Sources"
        K8S_METRICS[Kubernetes Metrics]
        APP_METRICS[Application Metrics]
        INFRA_METRICS[Infrastructure Metrics]
        LOGS[Container Logs]
    end
    
    subgraph "Collection Layer"
        PROMETHEUS_OP[Prometheus Operator]
        PROMTAIL[Promtail]
        FLUENT_BIT[Fluent Bit]
    end
    
    subgraph "Storage Layer"
        PROM_STORAGE[Prometheus Storage]
        LOKI_BACKEND[Loki Backend]
        OBJECT_STORAGE[MinIO S3]
    end
    
    subgraph "Visualization"
        GRAFANA_UI[Grafana Dashboards]
        ALERT_MGR[Alert Manager]
        NOTIFICATIONS[Notifications]
    end
    
    K8S_METRICS --> PROMETHEUS_OP
    APP_METRICS --> PROMETHEUS_OP
    INFRA_METRICS --> PROMETHEUS_OP
    LOGS --> PROMTAIL
    LOGS --> FLUENT_BIT
    
    PROMETHEUS_OP --> PROM_STORAGE
    PROMTAIL --> LOKI_BACKEND
    FLUENT_BIT --> LOKI_BACKEND
    
    LOKI_BACKEND --> OBJECT_STORAGE
    
    PROM_STORAGE --> GRAFANA_UI
    LOKI_BACKEND --> GRAFANA_UI
    PROM_STORAGE --> ALERT_MGR
    ALERT_MGR --> NOTIFICATIONS
```

---

## 🚀 Getting Started

### Prerequisites Setup

1. **Install Development Tools**
   ```bash
   # Install Devbox for dependency management
   curl -fsSL https://get.jetify.com/devbox | bash
   
   # Initialize devbox environment
   devbox shell
   ```

2. **Configure Environment**
   ```bash
   # Clone the repository
   git clone https://github.com/ixxeL-DevOps/fullstack.git
   cd fullstack
   
   # Install dependencies via devbox
   devbox add talosctl kubectl go-task sops vault helm
   ```

3. **Infrastructure Prerequisites**
   - Proxmox VE cluster with sufficient resources
   - Static IP reservations for cluster nodes
   - DNS resolution for cluster endpoints
   - Storage backend (NFS, iSCSI, or local storage)

### Deployment Process

#### 1. **Talos Cluster Deployment**
```bash
# Generate Talos secrets
task talos:gen-secrets cluster=genmachine

# Bootstrap the cluster
task talos:bootstrap cluster=genmachine

# Verify cluster status
kubectl --context genmachine get nodes
```

#### 2. **k0s Cluster Deployment**
```bash
# Deploy k0s cluster
task k0s:deploy

# Verify cluster status
kubectl --context k0s get nodes
```

#### 3. **GitOps Bootstrap**
```bash
# Deploy ArgoCD
kubectl apply -k gitops/bootstrap/genmachine

# Sync applications
argocd app sync --all
```

### Operational Tasks

#### Daily Operations
```bash
# Check cluster health
task k8s:approve-certs cluster=genmachine
task k8s:delete-failed-pods cluster=genmachine

# Update dependencies
task renovate:run

# Backup operations
task restic:backup
```

#### Troubleshooting
```bash
# Debug networking
task k8s:netshoot cluster=genmachine

# Browse persistent volumes
task k8s:browse-pvc

# Check what's running
task k8s:what-dockerhub
```

---

## 📚 Additional Resources

### Documentation Structure
- `/docs/` - Comprehensive documentation
- `/gitops/` - GitOps manifests and configurations
- `/infra/` - Infrastructure as Code
- `/.taskfiles/` - Automation scripts and tasks

### Key Files
- `Taskfile.yaml` - Main automation entry point
- `devbox.json` - Development environment definition
- `mkdocs.yml` - Documentation site configuration
- `.pre-commit-config.yaml` - Code quality hooks

### External References
- [Talos Linux Documentation](https://www.talos.dev/)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [k0s Documentation](https://docs.k0sproject.io/)
- [Cilium Documentation](https://docs.cilium.io/)
- [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)

---

This documentation provides a comprehensive overview of the ixxeL-DevOps fullstack repository, covering all major components, workflows, and operational procedures. The repository represents a mature, production-ready home lab infrastructure that demonstrates modern DevOps and GitOps practices.
