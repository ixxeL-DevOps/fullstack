
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout e22fec439b1999ac24e3d1feed189c30985cda31
helm template . --name-template external-secrets-k0s --include-crds
```