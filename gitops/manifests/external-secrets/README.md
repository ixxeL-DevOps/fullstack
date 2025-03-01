
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 4090075af92e01b82843b1d2772e231d3147a781
helm template . --name-template external-secrets-k0s --include-crds
```