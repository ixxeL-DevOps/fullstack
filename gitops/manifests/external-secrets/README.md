
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout e38927dc2cd1ecf582da1364ddb76411142b01ea
helm template . --name-template external-secrets-k0s --include-crds
```