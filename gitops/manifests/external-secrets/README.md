
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 67857aad88cde06797b959db586c7025b9e5a872
helm template . --name-template external-secrets-k0s --include-crds
```