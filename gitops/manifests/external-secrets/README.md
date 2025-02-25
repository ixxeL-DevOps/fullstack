
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout f5fac80eb7d3dd38165ab77028e0e392c587aa72
helm template . --name-template external-secrets-k0s --include-crds
```