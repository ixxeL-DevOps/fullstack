
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 1099ce74a76cecc28f35cbd33b6361d6c2d2ef8d
helm template . --name-template external-secrets-k0s --include-crds
```