
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 8dc85b6ba75a29dca3f2c21644c5d9cc7fffc377
helm template . --name-template external-secrets-k0s --include-crds
```