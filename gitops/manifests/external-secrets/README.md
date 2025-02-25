
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 1b9b82b112900b369d86eace1290bc61c42e06f1
helm template . --name-template external-secrets-k0s --include-crds
```