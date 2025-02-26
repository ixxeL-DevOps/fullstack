
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout a79c4366800e7d16f9ae6af60d16153467e2e6d3
helm template . --name-template external-secrets-k0s --include-crds
```