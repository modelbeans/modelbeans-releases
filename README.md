# ModelBeans releases

Public distribution and user documentation for ModelBeans and RuntimeShare.

[简体中文](README.zh-CN.md) · [Releases](https://github.com/modelbeans/modelbeans-releases/releases) · [Report an issue](https://github.com/modelbeans/modelbeans-releases/issues)

## Release status

The public release channel is being prepared. No installer or runtime package has been published in this repository yet.

Future releases will provide ModelBeans installers with the RuntimeShare components listed in each release, and may provide separate runtime/developer packages. Model weights are separate unless a release explicitly says otherwise. Supported platforms, models and backends will be listed per release; repository creation does not establish platform support.

## Downloading a release

When a release is available, open its **Assets** section and select the installer or runtime archive for your supported platform. Read the release notes, known limitations and verification instructions first. Preview releases are marked **Pre-release**.

GitHub's automatically generated **Source code (zip/tar.gz)** downloads contain only this distribution repository's documentation. They are not installers and do not contain the ModelBeans or RuntimeShare implementation.

## For developers

Runtime API instructions, SDK usage guides and reviewed integration examples will be added alongside the applicable developer release. An SDK is not currently available for download from this repository. A runtime package and model files are required for real local inference.

## Repository scope

This repository is the public release destination. Product implementation source and internal development history are not published here. See [Release policy](RELEASE_POLICY.md) and [Licensing](LICENSING.md).

## Feedback

Include the release version, OS, hardware, model/backend, reproduction steps and redacted logs. Do not include API keys, private files or sensitive prompts in public issues.
