
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout ec00f82766ea97cf4f6048842cc052062b53fd5a
helm template . --name-template external-secrets-k0s --include-crds
```