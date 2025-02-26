
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 048ebb35b2b74db872da5996d5e98ed2809a7fd3
helm template . --name-template external-secrets-k0s --include-crds
```