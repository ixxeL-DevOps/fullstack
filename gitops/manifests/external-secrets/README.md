
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout ddca05500152838c344a8b5783178a1736043c4f
helm template . --name-template external-secrets-k0s --include-crds
```