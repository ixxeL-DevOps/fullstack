
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 5c9674e7931bdc56914338d0ffcc8caf9525ea05
helm template . --name-template external-secrets-k0s --include-crds
```