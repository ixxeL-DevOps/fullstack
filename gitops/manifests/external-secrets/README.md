
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 9e916f46b839e7b34eef31ab0d79a154df31ec31
helm template . --name-template external-secrets-k0s --include-crds
```