
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 3504f4cc60e41048d929748aea6db957af0d3e42
helm template . --name-template external-secrets-k0s --include-crds
```