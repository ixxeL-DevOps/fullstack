
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 7f391c92851af16229867c50014bd6e741d09c8c
helm template . --name-template external-secrets-k0s --include-crds
```