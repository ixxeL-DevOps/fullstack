
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 0a598fe2c32e236d93950ba35c3b05c34125744e
helm template . --name-template external-secrets-k0s --include-crds
```