
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout fc29c5714829b482dbf59eee916a31432adda7a3
helm template . --name-template external-secrets-k0s --include-crds
```