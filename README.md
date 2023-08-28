# E-mail Release Notification
This repo contains a re-usable GitHub Action that when installed sends an e-mail to a distribution list with the release notes every time a GitHub Release is created for the repository.

[![Build Image](https://github.com/licenseware/send-email-notification/actions/workflows/build-image.yml/badge.svg)](https://github.com/licenseware/send-email-notification/actions/workflows/build-image.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

Using [the Python library](https://pypi.org/project/sendgrid/), send email to people
with the content, subject, attachments of your choice.


## Pre-Requisites
To run this action you'll need:

A [SendGrid API Key](https://sendgrid.com/docs/ui/account-and-settings/api-keys/). SendGrid is [free to up 100 e-mails a day](https://sendgrid.com/pricing/) so feel free to register and get your API KEY.

This repository is used inside Github Actions in the following format:

Setup
1. Create the workflow
Add a new YML file workflow in .github/workflows to trigger on release. For example:

### Send email to one address

```yaml
      - uses: licenseware/send-email-notification@v1
        with:
          api-key: ${{ secrets.SENDGRID_API_KEY }}
          subject: Test Subject
          from-email: verified-email@licenseware.io
          to-email: john-doe@licenseware.io
          markdown-body: |
            # My Markdown Title

            This is a description

            ## Another header

            Another description
```

### Send email to multiple address upon Github release

```yaml
on:
  release:
    types:
      - published

jobs:
  release-notification:
    name: release notification
    runs-on: ubuntu-latest
    strategy:
      matrix:
        to-emails:
          - receiver10@licenseware.io receiver11@licenseware.io
          - receiver2@licenseware.io
          - receiver3@licenseware.io

    steps:
      - uses: licenseware/send-email-notification@v1
        with:
          api-key: ${{ secrets.SENDGRID_API_KEY }}
          subject: New Release ${{ github.repository }}:${{ github.ref_name }}
          from-email: verified-email@licenseware.io
          to-email: ${{ matrix.to-emails }}
          markdown-body: ${{ github.event.release.body }}

```
2. Set the SendGrid secret
Create a new secret on your project named SENDGRID_API_TOKEN. Set the value to your [SendGrid API Key](https://sendgrid.com/docs/ui/account-and-settings/api-keys/).
