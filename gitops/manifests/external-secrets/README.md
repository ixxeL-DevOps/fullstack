
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 0b5faebdcc3955a25bfb20a380e9fb9322b70b2c
helm template . --name-template external-secrets-k0s --include-crds
```