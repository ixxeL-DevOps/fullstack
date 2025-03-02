
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout dc78725e825231f220e648e312b3858b63bbe80a
helm template . --name-template external-secrets-k0s --include-crds
```