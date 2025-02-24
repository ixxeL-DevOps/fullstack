
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 4dca6426bb2840a2bffcf3cb4c054a49d688f84a
helm template . --name-template external-secrets-k0s --include-crds
```