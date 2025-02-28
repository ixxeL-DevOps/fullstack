
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout eb42dbf8c3412efd58ac3f4a2bc3b57f1b7222aa
helm template . --name-template external-secrets-k0s --include-crds
```