
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 6987a82a5242edb1dcd1397208bc05d6de142497
helm template . --name-template external-secrets-k0s --include-crds
```