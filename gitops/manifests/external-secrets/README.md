
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout ef9d2eee5f05f2d9ab8a74f3fa6c74f112543c4c
helm template . --name-template external-secrets-k0s --include-crds
```