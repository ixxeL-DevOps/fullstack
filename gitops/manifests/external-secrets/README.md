
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout eef76d770f0de81dc27b81bdf34a547c5adcda9e
helm template . --name-template external-secrets-k0s --include-crds
```