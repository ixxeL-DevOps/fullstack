
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout cde26ab2c529dd815b1621b39b3285d9720e3704
helm template . --name-template external-secrets-k0s --include-crds
```