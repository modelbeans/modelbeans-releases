# Public release policy

The public destination for ModelBeans and RuntimeShare distribution is:

https://github.com/modelbeans/modelbeans-releases/releases

## Contents

This repository may contain user-facing documentation, release notes, reviewed SDK usage examples, compatibility manifests and license notices. Installers and runtime/developer archives are attached as GitHub Release assets, not committed as binary blobs in Git history.

Product implementation source, internal design/review documents, development history, credentials, user data and model caches are outside this repository's scope. Creating this channel does not authorize publishing any particular binary, SDK source package or model weights.

## Version records

- ModelBeans releases use `vX.Y.Z`; preview candidates may use `vX.Y.Z-rc.N` and are marked Pre-release.
- If RuntimeShare is released independently, use namespaced tags such as `runtimeshare-vX.Y.Z` to avoid version collisions.
- A release records supported platforms, included components and their versions, artifact hashes, relevant licensing, installation instructions and known limitations.
- A distribution-repository tag identifies the release documentation and manifest. It is not the implementation source revision; build provenance must be recorded separately.
- Published version tags and asset contents must not silently change. Corrections require a new version and explanatory release notes; unsafe releases can be withdrawn with an explanation.

## Verification

Only tested capabilities may be advertised. A successful build or mock test does not certify a hardware backend. A checksum verifies bytes, not publisher identity; signing status must be stated accurately.

For models, local hardware requirements and licenses apply independently. API compatibility refers to the documented and tested subset, not every feature of an upstream provider.

No automated publishing workflow is configured by this repository initialization.

## Release channels from 0.1.99

The final numeric component (patch number) is a project-specific channel convention:
odd numbers are reserved for tested stable releases; even numbers are experimental
and marked **Pre-release** on GitHub. Candidates may also use an explicit
`-rc.N` suffix and remain Pre-release, regardless of parity.
An odd version number alone is not proof of validation. Individual experimental
features, such as Audio Studio, may remain experimental inside a stable release.

自 0.1.99 起，版本号最后一位（补丁号）为奇数时用于经过验收的正式版本，
偶数时用于实验版本，并在 GitHub 标为 Pre-release。带 `-rc.N` 的候选版本
无论奇偶均为预发布。奇数本身不代表已经通过验证；正式版本中仍可能包含明确
标注的实验性功能，例如音频工作室。
