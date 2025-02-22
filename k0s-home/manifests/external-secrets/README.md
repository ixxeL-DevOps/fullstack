
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 3bedc11018adc0ca0e234ad5335ea84a6b3052ff
helm template . --name-template external-secrets-k0s --include-crds
```