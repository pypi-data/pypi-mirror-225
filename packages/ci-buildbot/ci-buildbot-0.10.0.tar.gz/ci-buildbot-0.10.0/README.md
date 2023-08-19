# ci-buildbot

`ci-buildbot` is a command line tool to do slack messaging from CodePipelines.  `ci-buildbot` acts as a Slack App in
order to do its work.

To install:

```bash
pyenv virtualenv 3.8.5 ci-buildbot
pyenv local ci-buildbot
pip install -r requirements.txt
pip install -e .
```

Now set up the environment:

```bash
cp etc/environment.text .env
```

You'll need to know two things:

* `SLACK_API_TOKEN`: this your Slack app's Oath token
* `CHANNEL`: this is the channel you want `ci-buildbot` to post into.  Note that if this is a private channel, you'll need to invite the `ci-buildbot` app into that channel before you'll see any messages.

Now you can run the main command, `buildbot`:

```bash
buildbot --help
```

## Icons

I get the icons for the Slack messages here: https://iconmonstr.com.

Get them as .pngs, 64x64px, name them appropriately to the build steps they're going to be used in, and save them to `./icons/`

For the gray icons (`foo-start.png`), use #909090 as the icon color.
For the green icons (`foo-success.png`), use #0D6B19 as the icon color.
For the red icons (`foo-failure.png`), use #801B0B as the icon color.

`ci-buildbot` tells slack to retrieve the icons from an S3 bucket: ads-utils-icons.s3.amanzonaws.com.  Do this to sync `./icons` to S3:

```bash
make icons
```

## Testing: CodeBuild environment variables

```bash
export CODEBUILD_START_TIME=1594856732.3577878
export CODEBUILD_VPC_AZ=us-west-2b
export CODEBUILD_LAST_EXIT=0
export CODEBUILD_START_TIME=1538752095466
export CODEBUILD_BMR_URL=https://CODEBUILD_AGENT:3000
export CODEBUILD_SOURCE_VERSION=arn:aws:s3:::bucket/pipeline/App/OGgJCVJ.zip
export CODEBUILD_KMS_KEY_ID=arn:aws:kms:us-west-2:000000011111:alias/aws/s3
export CODEBUILD_BUILD_ID=codebuild-project:40b92e01-706b-422a-9305-8bdb16f7c269
export OLDPWD=/codebuild/output/src00011222/src
export CODEBUILD_GOPATH=/codebuild/output/src084981953
export CODEBUILD_RESOLVED_SOURCE_VERSION=9e0d29404ee30b7b63258414ecccc996bbeb55c6
export CODEBUILD_BUILD_SUCCEEDING=1
export CODEBUILD_BUILD_ARN=arn:aws:codebuild:us-west-2:000000001111:build/codebuild-project:40b92e01-706b-422a-9305-8bdb16f7c269
export AWS_CONTAINER_CREDENTIALS_RELATIVE_URI=/v2/credentials/e5f23b9f-c72e-4384-9ba1-37d08aa052b7
export CODEBUILD_INITIATOR=codepipeline/pipeline-name
export AWS_DEFAULT_REGION=us-west-2
export CODEBUILD_LOG_PATH=40b92e01-706b-422a-9305-8bdb16f7c269
export CODEBUILD_BUILD_IMAGE=000011112222.dkr.ecr.us-west-2.amazonaws.com/codebuild:docker-image
export AWS_REGION=us-west-2
export CODEBUILD_SRC_DIR=/codebuild/output/src00011222/src
export CODEBUILD_AUTH_TOKEN=0730f0ab-5299-4235-a2c2-bb1f6ad07033
```
