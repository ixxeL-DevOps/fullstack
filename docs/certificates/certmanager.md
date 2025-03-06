# Cert-Manager

## Installation

Cert-manager can be used to handle certificates lifecycle in your cluster. `cert-manager` and `trust-manager` should be installed to get a complete lifycle management.

## Configuration

Cert-manager must be bound to your CA, in our case this is **HC Vault**. The clusterIssuer represent the CA and should point to the `Intermediate` PKI and get a `kubernetes` Vault authentication.

```yaml
---
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: fredcorp-ca
spec:
  vault:
    server: https://vault.k0s-fullstack.fredcorp.com
    path: pki_int/sign/fredcorp.com
    caBundleSecretRef:
      key: ca.crt
      name: root-ca-chain
    auth:
      kubernetes:
        mountPath: /v1/auth/kubernetes
        role: certmanager-vault-auth-k0s
        serviceAccountRef:
          name: certmanager-vault-auth-k0s
```

The `caBundleSecretRef` should point to the chain certificate to trust Vault server.

To be able to get the cluster issuer permissions to connect to Vault PKI, use `ServiceAccount` and `ClusterRoleBinding` :

```yaml
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: tokenreview-binding-certmanager
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:auth-delegator
subjects:
  - kind: ServiceAccount
    name: certmanager-vault-auth-k0s
    namespace: cert-manager
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: certmanager-vault-auth-k0s
---
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
  name: certmanager-vault-auth-k0s
  annotations:
    kubernetes.io/service-account.name: 'certmanager-vault-auth-k0s'
```

Then you need to configure the HC Vault server:
