
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 82d4d62322ec197b33eac0fb67d4232ea973515c
helm template . --name-template external-secrets-k0s --include-crds
```