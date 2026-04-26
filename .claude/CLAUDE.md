# Homelab Repository Context

GitOps-managed Kubernetes homelab using ArgoCD, Talos and k0s.

## Read First

1. **@docs/ai-context/README.md** - Overview and navigation
2. **@docs/ai-context/Ethos.md** - Documentation philosophy
3. **@docs/ai-context/ARCHITECTURE.md** - System architecture
4. **@docs/ai-context/CONVENTIONS.md** - Coding standards

## Documentation

### System Context

- @docs/ai-context/ARCHITECTURE.md - Architecture, capsules, patterns
- @docs/ai-context/NETWORKING.md - Traffic flows, DNS, gateways, OIDC
- @docs/ai-context/DOMAIN.md - Rules, state machines, glossary
- @docs/ai-context/WORKFLOWS.md - How to deploy, update, troubleshoot
- @docs/ai-context/TOOLS.md - CLI commands
- @docs/ai-context/CONVENTIONS.md - Naming, structure, style

### Writing Guides

- @docs/ai-context/Ethos.md - Hard rules, guidance, values
- @docs/ai-context/PLANNING.md - Collaborative planning lifecycle
- @docs/ai-context/writing-documentation.md - Wisdom triggers
- @docs/ai-context/writing-capsules.md - Capsule format
- @docs/ai-context/mermaid-diagram-guide.md - Diagram rules

## Critical Invariants

### Clusters: Location of Source

There are two independent clusters:

genmachine(Talos): each `genmachine` or Talos directory relate to this cluster. Root at @infra/talos.
beelink(k0s): each `beelink` or k0s directory relate to this cluster. Root at @infra/k0s.

The only shared code is the `common` directories which host shared values for applies Helm deployments.
Except from that the clusters do not share code. When making changes, it is important
to know which cluster is being worked on. Make sure to know this in advance
of any planning or changes.

### Capsule: GitOpsReconciliation

**Invariant**: Cluster state converges to match Git; ArgoCD reverts manual changes.

## Directory Structure

```
infra/                  # Root directory for clusters configuration and boostrap
gitops/                 # Root directory for all deployed manifests
gitops/bootstrap        # ArgoCD installation directory
gitops/core             # ArgoCD CRs manifests (ApplicationSet, AppProject, VCS secrets...)
gitops/manifests        # Helm or plain YAML manifests to deploy applications
```

## Non-Obvious Truths

- **Automated update**: Always think about automated update for versions with Renovate
- **SOPS files**: End in `.sops.yaml`, encrypted before commit
