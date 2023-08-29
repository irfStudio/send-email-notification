# Send Email Notification 
This repo contains a re-usable GitHub Action that when installed sends an e-mail to a distribution list with the release notes every time a GitHub Release is created for the repository.

![python-checks](https://github.com/studioirf/send-email-notification/actions/workflows/python-checks.yml/badge.svg)
![self-test](https://github.com/studioirf/send-email-notification/actions/workflows/self-test.yml/badge.svg)

Using [the Python library](https://pypi.org/project/sendgrid/), send email to people
with the content, subject, attachments of your choice.


## Pre-Requisites
To run this action you'll need:

A [SendGrid API Key](https://sendgrid.com/docs/ui/account-and-settings/api-keys/). SendGrid is [free to up 100 e-mails a day](https://sendgrid.com/pricing/) so feel free to register and get your API KEY.

## Setup
### 1. Create the workflow
Add a new YML file workflow in `.github/workflows` to trigger on `release`. For example:


from-email: must be a verified sendgrid email
subject: is the subject of the email
api-key: SendGrid API Key
markdown-body: markkdown body
to-email: space or `\n` separated list of 

#### Send email to one address
```yaml
      - uses: studioirf/send-email-notification@v1
        with:
          api-key: ${{ secrets.SENDGRID_API_KEY }}
          subject: Test Subject
          from-email: sender@domain.tld
          to-email: recipient30@domain.tld
          markdown-body: |
            # My Markdown Title

            This is a description

            ## Another header

            Another description
```

#### Send email to multiple address upon Github release
By using matrix strategy multiple emails can be sent

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
          - recipient10@domain.tld recipient11@domain.tld
          - recipient20@domain.tld
          - recipient30@domain.tld

    steps:
      - uses: studioirf/send-email-notification@v1
        with:
          api-key: ${{ secrets.SENDGRID_API_KEY }}
          subject: New Release ${{ github.repository }}:${{ github.ref_name }}
          from-email: sender@domain.tld
          to-email: ${{ matrix.to-emails }}
          markdown-body: ${{ github.event.release.body }}

```

#### Send email with attachments

The step can be configured to send an email with file `example.txt` as attachment
```yaml
    steps:
      - uses: studioirf/send-email-notification@v1
        with:
          api-key: ${{ secrets.SENDGRID_API_KEY }}
          subject: New Release ${{ github.repository }}:${{ github.ref_name }}
          from-email: sender@domain.tld
          to-email: ${{ matrix.to-emails }}
          markdown-body: ${{ github.event.release.body }}
          attachments: Attachments/example.txt
```


In the following example the step is configured to send all the `.txt` files in the directory `Attachments`:
```yaml
    steps:
      - uses: studioirf/send-email-notification@v1
        with:
          api-key: ${{ secrets.SENDGRID_API_KEY }}
          subject: New Release ${{ github.repository }}:${{ github.ref_name }}
          from-email: sender@domain.tld
          to-email: ${{ matrix.to-emails }}
          markdown-body: ${{ github.event.release.body }}
          attachments: Attachments/*.txt
```

In the following example the step is configured to send multiple files matching specified patterns:
- all `.txt` files in the directory `Attachments`
- all `.csv` files across multiple directory levels
- 
```yaml
    steps:
      - uses: studioirf/send-email-notification@v1
        with:
          api-key: ${{ secrets.SENDGRID_API_KEY }}
          subject: New Release ${{ github.repository }}:${{ github.ref_name }}
          from-email: sender@domain.tld
          to-email: recipient1@domain.tld recipients@domain.tld 
          markdown-body: ${{ github.event.release.body }}
          attachments: Attachments/*.txt Attachments/**/*.csv 
```

##### References
- for details on how to search for multiple files see [glob](https://docs.python.org/3/library/glob.html)

### 2. Set the secrets
- Create a new secret on your project named SENDGRID_API_TOKEN. Set the value to your [SendGrid API Key](https://sendgrid.com/docs/ui/account-and-settings/api-keys/).


### 3. Test the workflow!

Create a new release for your repository and verify that the action triggers and that the e-mails were sent. Sometimes it's worth checking the spam inbox.
