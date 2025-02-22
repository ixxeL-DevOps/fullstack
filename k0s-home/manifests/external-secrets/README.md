
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 0716ec7e28f5762cd692e29954f1ac2e686cba90
helm template . --name-template external-secrets-k0s --include-crds
```