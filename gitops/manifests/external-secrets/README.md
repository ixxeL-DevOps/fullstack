
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 6185391b7bf9d0b4d644b945f9622dc0f9999648
helm template . --name-template external-secrets-k0s --include-crds
```