
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout a1ef9c24326c2675076d4ec5feda5a1cd70edcef
helm template . --name-template external-secrets-k0s --include-crds
```