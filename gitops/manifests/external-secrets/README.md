
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 7c887b52ae010563e9e4170f6bb4c84cd29c2c7d
helm template . --name-template external-secrets-k0s --include-crds
```