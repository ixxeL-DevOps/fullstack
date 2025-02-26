
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout ab04aedf40cdb7162ac8c2e2ed9c6db7db815d01
helm template . --name-template external-secrets-k0s --include-crds
```