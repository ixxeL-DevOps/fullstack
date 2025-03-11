# ExternalSecrets

## Installation

ExternalSecret make GitOps secured by using

## Configuration

```yaml
---
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: admin
spec:
  provider:
    vault:
      server: https://vault.k0s-fullstack.fredcorp.com
      path: admin
      version: v2
      caProvider: # Using cert-manager Bundle for chain CA fredcorp (Vault PKI)
        type: Secret
        namespace: external-secrets
        name: fredcorp-ca-chain
        key: fredcorp-ca-chain.pem
      auth:
        kubernetes:
          mountPath: genmachine
          role: eso
          serviceAccountRef:
            name: eso-auth
            namespace: external-secrets
          secretRef:
            name: eso-auth
            key: token
            namespace: external-secrets
```

The `caProvider` should point to the chain certificate to trust Vault server.

To be able to get the cluster issuer permissions to connect to Vault PKI, use `ServiceAccount` and `ClusterRoleBinding` :

```yaml
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: tokenreview-binding-externalsecrets
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:auth-delegator
subjects:
  - kind: ServiceAccount
    name: eso-auth
    namespace: external-secrets
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: eso-auth
  namespace: external-secrets
---
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
  name: eso-auth
  namespace: external-secrets
  annotations:
    kubernetes.io/service-account.name: eso-auth
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
TOKEN="$(kubectl get secret -n external-secrets eso-auth -o jsonpath='{.data.token}' | base64 -d)"
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
            auth/genmachine/role/eso \
            bound_service_account_names=eso-auth \
            bound_service_account_namespaces=external-secrets \
            policies=secretstore ttl=24h
```

You also need to create an associated policy, here named `secretstore`:

```hcl
path "admin/*" {
  capabilities = ["read","list","create","update"]
}

# List existing secrets engines.
path "sys/mounts"
{
  capabilities = ["read", "list"]
}

# List UI metadata
path "+/metadata/*"
{
  capabilities = ["read", "list"]
}

# Read UI data
path "+/data/*"
{
  capabilities = ["read", "list"]
}

path "*"
{
  capabilities = ["read"]
}
```

Then refresh the `ClusterSecretStore` it should be valid and working:

```console
NAME    AGE   STATUS   CAPABILITIES   READY
admin   10m   Valid    ReadWrite      True
```
