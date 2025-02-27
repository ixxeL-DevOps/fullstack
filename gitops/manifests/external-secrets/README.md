
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout cd3715b9eb574ee4a82fe3aa080589a700a15f8e
helm template . --name-template external-secrets-k0s --include-crds
```