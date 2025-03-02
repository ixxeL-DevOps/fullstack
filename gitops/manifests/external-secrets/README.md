
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 1e9ba8be70b2043228b53a03eb02c9a65fc300be
helm template . --name-template external-secrets-k0s --include-crds
```