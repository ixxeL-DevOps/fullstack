# TLS encryption

## Reverse Proxy encryption : wildcard certificate

Traefik can handle TLS traffic with enforced HTTPS redirection and TLS Termination. You need to specify it inb Traefik configuration with rule for redirection and TLSStore.

here is the `value.yaml` file for `TLSStore` configuration:

```yaml
tlsStore:
  default:
    defaultCertificate:
      secretName: k0s-fullstack-wildcard
```

TLSStore:

```yaml
apiVersion: traefik.io/v1alpha1
kind: TLSStore
metadata:
  name: default
  namespace: traefik
spec:
  defaultCertificate:
    secretName: k0s-fullstack-wildcard
```

And provision the `Secret` with an `ExternalSecret` :

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: k0s-fullstack-wildcard
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: admin
    kind: ClusterSecretStore
  target:
    name: k0s-fullstack-wildcard
    creationPolicy: Owner
    template:
      type: kubernetes.io/tls
      data:
        tls.crt: "{{ .p12 | pkcs12cert  }}"
        tls.key: "{{ .p12 | pkcs12key }}"
  data:
    - secretKey: p12
      remoteRef:
        conversionStrategy: Default
        decodingStrategy: Base64
        metadataPolicy: None
        key: wildcard/k0s-fullstack
        property: p12
```

And finally enforce TLS redirection in `values.yaml` file :

```yaml
ports:
  web:
    redirections:
      entryPoint:
        to: websecure
        scheme: https
```

- https://doc.traefik.io/traefik/middlewares/http/headers/#sslredirect
- https://doc.traefik.io/traefik/routing/entrypoints/#redirection

This configuration will enforce HTTPS traffic to all endpoints behing Traefik with a wildcard certificate managed by Traefik.

## TLS re-encryption

The best configuration is to enable TLS re-encryption to the final backend. With a combination of Certmanager and Traefik you can achieve this quite easily.

You just need to add specific annotations to `Ingress` resources to re-encrypt traffic:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    cert-manager.io/cluster-issuer: fredcorp-ca
    cert-manager.io/common-name: homarr.k0s-fullstack.fredcorp.com
    traefik.ingress.kubernetes.io/router.entrypoints: websecure
    traefik.ingress.kubernetes.io/service.scheme: https
  name: homarr-k0s
  namespace: homarr
spec:
  ingressClassName: traefik
  rules:
    - host: homarr.k0s-fullstack.fredcorp.com
      http:
        paths:
          - backend:
              service:
                name: homarr-k0s
                port:
                  number: 7575
            path: /
            pathType: Prefix
  tls:
    - hosts:
        - homarr.k0s-fullstack.fredcorp.com
      secretName: homarr-tls-cert
```

Annotation for Cert-manager to automatically manage certificate provisionning and renewal :

```yaml
cert-manager.io/cluster-issuer: fredcorp-ca
cert-manager.io/common-name: homarr.k0s-fullstack.fredcorp.com
```

Annotation for Traefik to enforce TLS re-encryption:

```yaml
traefik.ingress.kubernetes.io/router.entrypoints: websecure
traefik.ingress.kubernetes.io/service.scheme: https
```
