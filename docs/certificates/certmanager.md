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
        secretRef:
          name: certmanager-vault-auth-k0s
          key: token
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
    kubernetes.io/service-account.name: "certmanager-vault-auth-k0s"
```

Then you need to configure the HC Vault server. First login:

```bash
vault login -method=token -tls-skip-verify -address=https://vault.k0s-fullstack.fredcorp.com
```

Enable auth:

```bash
vault auth enable -path=genmachine/ -tls-skip-verify -address=https://vault.k0s-fullstack.fredcorp.com kubernetes
```

Get the current kubernetes cluster CA certificate :

```bash
kubectl config view --raw --minify --flatten -o jsonpath='{.clusters[].cluster.certificate-authority-data}' | base64 --decode > ca.crt
```

Get the `ServiceAccount` generated token :

```bash
TOKEN="$(kubectl get secret -n cert-manager certmanager-vault-auth-k0s -o jsonpath='{.data.token}' | base64 -d)"
```

Write the entry in Vault kubernetes Auth:

```bash
vault write -tls-skip-verify -address=https://vault.k0s-fullstack.fredcorp.com \
            auth/genmachine/config token_reviewer_jwt="$TOKEN" \
            kubernetes_host="https://k0s.fullstack.fredcorp.com:6443" \
            kubernetes_ca_cert=@ca.crt
```

And then create the associated role :

```bash
vault write -tls-skip-verify -address=https://vault.k0s-fullstack.fredcorp.com \
            auth/genmachine/role/certmanager \
            bound_service_account_names=certmanager-auth \
            bound_service_account_namespaces=cert-manager \
            policies=pki_fredcorp ttl=24h
```

You also need to create an associated policy, here named `pki_fredcorp`:

```hcl
path "*" {
    capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "pki_int*"
{
  capabilities = ["read", "list"]
}

path "pki_int/roles/fredcorp.com"
{
  capabilities = ["create", "update"]
}

path "pki_int/sign/fredcorp.com"
{
  capabilities = ["create", "update"]
}

path "pki_int/issue/fredcorp.com"
{
  capabilities = ["create", "update", "read", "list"]
}
```

Then refresh the `ClusterIssuer` it should be valid and working:

```console
NAME          READY   AGE
fredcorp-ca   True    24s
```

## Bundles

Trust-manager handles CA Bundles to make it easier for you to manage cluster trusted certificates.

You can use a Bundle and reference a secret as source of certificates. Target can be either `configMap` or `secret`.

```yaml
---
apiVersion: trust.cert-manager.io/v1alpha1
kind: Bundle
metadata:
  name: fredcorp-ca-chain
spec:
  sources:
    - useDefaultCAs: false
    - secret:
        name: "root-ca-chain"
        key: "ca.crt"
  target:
    secret:
      key: "fredcorp-ca-chain.pem"
    additionalFormats:
      pkcs12:
        key: "fredcorp-ca-chain.p12"
        password: ""
    namespaceSelector:
      matchLabels:
        bundle.chain/inject: "enabled"
```
