
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 717ab9cd8af4493231b5584adfbd021b7e97a69c
helm template . --name-template external-secrets-k0s --include-crds
```