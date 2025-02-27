
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 541f2f524c5f4769875cd4187d820103e908dd5a
helm template . --name-template external-secrets-k0s --include-crds
```