
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout ad9ad1015ecb4ca9fb2a0ce614c8289cf9df2dd2
helm template . --name-template external-secrets-k0s --include-crds
```