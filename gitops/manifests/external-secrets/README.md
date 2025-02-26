
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 277b1d38f42fd03539d18d513884f2f976dd9f83
helm template . --name-template external-secrets-k0s --include-crds
```