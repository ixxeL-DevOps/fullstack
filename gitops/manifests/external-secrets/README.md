
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 78fe453dfa0fffddd5ddcd762b634407859ad4b8
helm template . --name-template external-secrets-k0s --include-crds
```