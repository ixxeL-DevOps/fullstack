
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 13ae2fbed16f68aad5360f61ce89e8790dbe3dc3
helm template . --name-template external-secrets-k0s --include-crds
```