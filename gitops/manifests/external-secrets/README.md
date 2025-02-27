
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 6dea758927b636b204aeaa4ff3956b0e6e5ccc3c
helm template . --name-template external-secrets-k0s --include-crds
```