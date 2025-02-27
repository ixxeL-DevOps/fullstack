
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout b5f2d978d259cc066585f8562605f7c8f1245d89
helm template . --name-template external-secrets-k0s --include-crds
```