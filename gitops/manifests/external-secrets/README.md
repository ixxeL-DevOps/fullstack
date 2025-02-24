
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 7365b45878741e8ae9ae7e0319e904a85d37a03c
helm template . --name-template external-secrets-k0s --include-crds
```