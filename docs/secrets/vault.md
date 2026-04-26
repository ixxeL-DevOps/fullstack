# HashiCorp Vault

## Overview

Two Vault instances are deployed across the two clusters. Each instance serves as both a secrets engine and a PKI certificate authority for its cluster.

```mermaid
graph TB
    subgraph beelink["Beelink — k0s cluster"]
        vault_b["Vault beelink\nvault.k0s-fullstack.fredcorp.com"]
        pki_b["PKI Engine\nRoot + Intermediate CA\nfredcorp.com"]
        transit_b["Transit Engine\nSOPS encryption"]
        kv_b["KV Engine\nadmin/ secrets"]
    end

    subgraph genmachine["Genmachine — Talos cluster"]
        vault_g["Vault genmachine\nvault.talos-genmachine.fredcorp.com"]
        pki_g["PKI Engine\nRoot + Intermediate CA\nfredcorp.com"]
        transit_g["Transit Engine\nSOPS encryption"]
        kv_g["KV Engine\nadmin/ secrets"]
    end

    pki_b -->|signs certs for| cm_b["cert-manager\nbeelink"]
    pki_g -->|signs certs for| cm_g["cert-manager\ngenmachine"]
    kv_b -->|serves secrets to| eso_b["ExternalSecrets\nbeelink"]
    kv_g -->|serves secrets to| eso_g["ExternalSecrets\ngenmachine"]
    transit_b & transit_g -->|decrypt| sops["SOPS\nencrypted secrets in Git"]

    style vault_b fill:#1a2a3a,stroke:#FFB81C,color:#FFB81C
    style vault_g fill:#1a2a3a,stroke:#FFB81C,color:#FFB81C
```

## Authentication Methods

### Kubernetes Auth

Used by cert-manager and ExternalSecrets to authenticate with Vault using their ServiceAccount tokens:

```mermaid
sequenceDiagram
    participant app as cert-manager / ESO
    participant k8s as Kubernetes API
    participant vault as Vault

    app->>vault: Login with ServiceAccount JWT<br/>(auth/&lt;cluster&gt;-k8s/login)
    vault->>k8s: TokenReview — validate JWT
    k8s-->>vault: Token valid + bound SA info
    vault-->>app: Vault token (scoped to policy)
    app->>vault: Read secrets / sign certificates
```

Configure with:

```bash
task vault:eso-auth-setup cluster=genmachine
task vault:certmanager-auth-setup cluster=genmachine
```

### OIDC Auth

Human operators authenticate via Authentik SSO. See the [OIDC documentation](../authentication/oidc.md) for setup details.
