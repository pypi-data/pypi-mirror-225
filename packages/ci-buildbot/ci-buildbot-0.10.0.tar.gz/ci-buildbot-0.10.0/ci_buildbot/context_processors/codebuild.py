import os
import time

from typing import Optional

from ..typedefs import MessageContext
from .base import AbstractContextProcessor


class CodebuildProcessor(AbstractContextProcessor):
    """
    Adds the following keys to the context:

    * ``build_id``: the CodeBuild build id
    * ``build_project_name``: the CodeBuild project name
    * ``build_status_url``: the URL to the CodeBuild build status page
    * ``account_id``: the AWS account id
    * ``pipeline_url``: the URL to the CodePipeline pipeline status page
    * ``pipeline``: the CodePipeline pipeline name
    * ``status``: the CodePipeline pipeline status
    * ``region``: the AWS region
    * ``build_time``: the elapsed time for the build in minutes and seconds
    """

    def get_build_log_url(self, context: MessageContext) -> None:
        fields = os.environ['CODEBUILD_BUILD_ARN'].split(':')
        context['account_id'] = fields[4]
        context['build_project_name'] = fields[5].split('/')[1]
        context['build_id'] = fields[6]
        context['build_status_url'] = f"<https://{context['region']}.console.aws.amazon.com/codesuite/codebuild/{context['account_id']}/projects/{context['build_project_name']}/build/{context['build_project_name']}%3A{context['build_id']}/log?region=us-west-2|Click here>"

    def get_pipeline_url(self, context: MessageContext) -> None:
        # FIXME: detect region from the environment instead of hardcoding it to us-west-2
        context['pipeline'] = os.environ['CODEBUILD_INITIATOR'].split('/')[1]
        context['pipeline_url'] = f"<https://{context['region']}.console.aws.amazon.com/codesuite/codepipeline/pipelines/{context['pipeline']}/view?region=us-west-2|{context['pipeline']}>"

    def annotate(self, context: MessageContext) -> None:
        context['status'] = 'Success' if 'CODEBUILD_BUILD_SUCCEEDING' in os.environ else 'Failed'
        context['region'] = os.environ['AWS_DEFAULT_REGION']
        context['build_id'] = os.environ.get('CODEBUILD_BUILD_ID', None)
        build_seconds = time.time() - float(os.environ['CODEBUILD_START_TIME']) / 1000
        build_minutes = int(build_seconds // 60)
        build_seconds = int(build_seconds - build_minutes * 60)
        context['build_time'] = f"{build_minutes}m {build_seconds}s"
        self.get_build_log_url(context)
        self.get_pipeline_url(context)
