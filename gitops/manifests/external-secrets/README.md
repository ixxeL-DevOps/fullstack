
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout ccd6502593f7a1b26a35a0db4397c8236a6b4201
helm template . --name-template external-secrets-k0s --include-crds
```