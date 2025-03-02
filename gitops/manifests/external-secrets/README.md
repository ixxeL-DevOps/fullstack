
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 5612b40ae0cb0b2678cdc1099034e9758a81232b
helm template . --name-template external-secrets-k0s --include-crds
```