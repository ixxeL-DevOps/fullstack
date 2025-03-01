
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout f04f700edb38dc012f6ec4bede3775ec1c3e28d4
helm template . --name-template external-secrets-k0s --include-crds
```