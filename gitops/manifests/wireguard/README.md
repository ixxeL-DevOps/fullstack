
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 0ad643b97a2b49dce00c5e227057d445b4064c9f
helm template . --name-template wireguard-k0s --include-crds
```