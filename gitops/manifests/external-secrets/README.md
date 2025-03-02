
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 84123939b910297706aa01feeacab3aef950796c
helm template . --name-template external-secrets-k0s --include-crds
```