
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 7e6f4f01c56555c474c7e7a4959286b4055fa272
helm template . --name-template external-secrets-k0s --include-crds
```