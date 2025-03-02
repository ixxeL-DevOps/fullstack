
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 5d6e784468f7dc9953f3d9a4a92f6fc7319ff0e7
helm template . --name-template external-secrets-k0s --include-crds
```