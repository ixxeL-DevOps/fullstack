
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout abff0244a5f9dd497215b9bfc3bb7362459f4a55
helm template . --name-template external-secrets-k0s --include-crds
```