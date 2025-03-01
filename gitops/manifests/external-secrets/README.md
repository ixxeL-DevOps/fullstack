
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 7892b12461e0e8567a39cc376d3951d3ecc7a57d
helm template . --name-template external-secrets-k0s --include-crds
```