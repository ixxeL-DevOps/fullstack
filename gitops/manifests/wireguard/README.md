
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout d3fc59971c34ea511ce4d6ca0353eec27f8075b6
helm template . --name-template wireguard-k0s --include-crds
```