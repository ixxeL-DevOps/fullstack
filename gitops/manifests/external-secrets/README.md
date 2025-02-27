
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 15dd9b41aac530b223018c64d6d35063e9b364de
helm template . --name-template external-secrets-k0s --include-crds
```