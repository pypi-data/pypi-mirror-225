"""
radiens CLI
"""
import click
from datetime import datetime
from pprint import pprint

from radiens.base_client import BaseClient


@ click.group()
@ click.option('--hub', default='default', help='radiens hub name')
@ click.pass_context
def radiens(ctx, hub):
    ''' Radiens file system commands
    '''
    ctx.ensure_object(dict)
    ctx.obj['client'] = BaseClient()
    ctx.obj['hub'] = hub


@ radiens.command()
@ click.pass_context
@ click.option('-s', '--sort', default='date', help='sort attribute', show_default=True)
@ click.option('-b', '--brief', default=True, type=bool, help='show brief description', show_default=True)
@ click.argument('path', nargs=-1)
def ls(ctx, sort, brief, path):
    '''List directory
    '''
    try:
        resp = ctx.obj['client'].ls(path, sort_by=sort, hub_name=ctx.obj['hub'])
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    if len(resp.datasource_table) == 0:
        pprint('No Radiens data file sets in requested directory')
        return
    if brief:
        pprint(resp.datasource_table[['path', 'base_name', 'type', 'bytes_total', 'timestamp']])
    else:
        pprint(resp.datasource_table[['path', 'base_name', 'type', 'bytes_total', 'timestamp', 'num_chan', 'dur_sec']])
