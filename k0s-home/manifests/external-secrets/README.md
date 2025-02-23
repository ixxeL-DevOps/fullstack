
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 874761ab62ee5aa81c23ab7b9bb909985006d70a
helm template . --name-template external-secrets-k0s --include-crds
```