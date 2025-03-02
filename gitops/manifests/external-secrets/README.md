
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 7d1f77c7090ad0b69f979842e293b10ea530e05c
helm template . --name-template external-secrets-k0s --include-crds
```