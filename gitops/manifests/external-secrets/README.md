
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 9ffd5b0510fb26f1596eb956f1d84e48ef91391d
helm template . --name-template external-secrets-k0s --include-crds
```