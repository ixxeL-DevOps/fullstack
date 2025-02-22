
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout ef619b9b8369e6f3ad6936e9c7c5830b6d28d61f
helm template . --name-template external-secrets-k0s --include-crds
```