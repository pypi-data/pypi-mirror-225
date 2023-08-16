import click
import click_log
from convisoappsec.common.box import ContainerWrapper
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.common import on_http_error, project_code_option
from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.logger import LOGGER

click_log.basic_config(LOGGER)


@click.command()
@click_log.simple_verbosity_option(LOGGER)
@project_code_option(
    help="Not required when --no-send-to-flow option is set",
    required=False
)
@click.option(
    '-r',
    '--repository-dir',
    default=".",
    show_default=True,
    type=click.Path(
        exists=True,
        resolve_path=True,
    ),
    required=False,
    help="The source code repository directory.",
)
@click.option(
    "--send-to-flow/--no-send-to-flow",
    default=True,
    show_default=True,
    required=False,
    help="""Enable or disable the ability of send analysis result
    reports to flow. When --send-to-flow option is set the --project-code
    option is required""",
    hidden=True
)
@click.option(
    "--custom-sca-tags",
    hidden=True,
    required=False,
    multiple=True,
    type=(str, str),
    help="""It should be passed as <repository_name> <image_tag>. It accepts multiple values"""
)
@click.option(
    "--scanner-timeout",
    hidden=True,
    required=False,
    default=7200,
    type=int,
    help="Set timeout for each scanner"
)
@click.option(
    "--parallel-workers",
    hidden=True,
    required=False,
    default=2,
    type=int,
    help="Set max parallel workers"
)
@click.option(
    "--deploy-id",
    default=None,
    required=False,
    hidden=True,
    envvar="FLOW_DEPLOY_ID"
)
@help_option
@pass_flow_context
def run(
    flow_context, project_code, repository_dir, send_to_flow, custom_sca_tags, scanner_timeout, parallel_workers, deploy_id
):
    '''
      This command will perform SCA analysis at the source code. The analysis
      results can be reported or not to flow application. 

    '''
    perform_command(
        flow_context,
        project_code,
        repository_dir,
        send_to_flow,
        custom_sca_tags,
        scanner_timeout,
        parallel_workers,
        deploy_id
    )


def perform_command(
    flow_context, project_code, repository_dir, send_to_flow, custom_sca_tags, scanner_timeout, parallel_workers, deploy_id
):
    if send_to_flow and not project_code:
        raise click.MissingParameter(
            'It is required when sending reports to flow api.',
            param_type='option',
            param_hint='--project-code',
        )

    try:
        REQUIRED_CODEBASE_PATH = '/code'
        DANDELION_IMAGE_NAME = 'scabox-dandelion'
        RAMPHASTOS_IMAGE_NAME = 'scabox-ramphastos'

        scanners = {
            DANDELION_IMAGE_NAME: {
                'repository_name': DANDELION_IMAGE_NAME,
                'tag': 'latest',
                'command': [
                    '-c', REQUIRED_CODEBASE_PATH,
                    '-f', 'json',
                    '-o', '/{}.json'.format(DANDELION_IMAGE_NAME)
                ],
                'repository_dir': repository_dir
            },
            RAMPHASTOS_IMAGE_NAME: {
                'repository_name': RAMPHASTOS_IMAGE_NAME,
                'tag': 'latest',
                'command': [
                    '-c', REQUIRED_CODEBASE_PATH,
                    '-f', 'json',
                    '-o', '/{}.json'.format(RAMPHASTOS_IMAGE_NAME)
                ],
                'repository_dir': repository_dir
            },
        }

        if custom_sca_tags:
            for custom_tag in custom_sca_tags:
                scan_name, tag = custom_tag
                if scan_name in scanners.keys():
                    scanners[scan_name]['tag'] = tag
                else:
                    raise click.BadOptionUsage(
                        option_name='--custom-sca-tags',
                        message="Custom scan {0} or tag {1} invalid".format(
                            scan_name, tag)
                    )

        flow = flow_context.create_conviso_rest_api_client()
        token = flow.docker_registry.get_sast_token()
        LOGGER.info('\U0001F4AC Preparing Environment')
        scabox = ContainerWrapper(
            token=token,
            containers_map=scanners,
            logger=LOGGER,
            timeout=scanner_timeout
        )
        LOGGER.info('\U0001F4AC Starting SCA')
        scabox.run()

        LOGGER.info('\U0001F4AC Processing Results')
        if send_to_flow:
            for unit in scabox.scanners:
                report_file_path = unit.results
                if report_file_path:
                    report_file = open(report_file_path)
                    LOGGER.info("   Sending {} data to AppSec Flow...".format(
                        unit.name
                    ))
                    response = flow.findings.create(
                        project_code=project_code,
                        commit_refs=None,
                        finding_report_file=report_file,
                        deploy_id=deploy_id,
                    )
                    if response < 210:
                        LOGGER.info('   {} data has been sent successfully'.format(
                            unit.name
                        ))
                    else:
                        LOGGER.info('   {} was not sent, Conviso will be notified about this error.'.format(
                            unit.name
                        ))
                    report_file.close()
                else:
                    LOGGER.info('   {} has no issues to report'.format(
                        unit.name
                    ))

        # TODO add CI Decision block code
        LOGGER.info('\U00002705 SCA Scan Finished')

    except Exception as e:
        on_http_error(e)
        raise click.ClickException(str(e)) from e


EPILOG = '''
Examples:

  \b
  1 - Reporting the results to flow api:
    1.1 - Running an analysis at all commit range:
      $ export FLOW_API_KEY='your-api-key'
      $ export FLOW_PROJECT_CODE='your-project-code'
      $ {command}

'''  # noqa: E501

SHORT_HELP = "Perform Source Composition analysis"

command = 'conviso sca run'
run.short_help = SHORT_HELP
run.epilog = EPILOG.format(
    command=command,
)
