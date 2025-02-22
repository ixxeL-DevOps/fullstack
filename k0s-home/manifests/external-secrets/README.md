
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 39e448994bab17b4736463118c0f8636fa9a7d24
helm template . --name-template external-secrets-k0s --include-crds
```