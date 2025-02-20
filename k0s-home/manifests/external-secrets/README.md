
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout cd3d2f550ac16abc98cbe85c1a19485d9f9e2822
helm template . --name-template external-secrets-k0s --include-crds
```