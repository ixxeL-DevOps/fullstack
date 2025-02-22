
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout bab8f854fccbf19bd1b9711bb9cba121eb340d48
helm template . --name-template external-secrets-k0s --include-crds
```