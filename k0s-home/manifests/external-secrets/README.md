
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout b633b123ba2f0b88a8083fd49b774aa6256159c0
helm template . --name-template external-secrets-k0s --include-crds
```