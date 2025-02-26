
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout e227c3f21d2b8971e33bc11c1e6c22d226dc5955
helm template . --name-template external-secrets-k0s --include-crds
```