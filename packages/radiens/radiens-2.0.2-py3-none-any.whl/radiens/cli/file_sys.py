"""
radiens CLI
"""
import click
import pandas as pd
from datetime import datetime
from pprint import pprint
from pathlib import Path


@ click.group(short_help='file system commands')
@ click.option('--hub', default='default', help='radiens hub name')
@ click.pass_context
def filesys(ctx, hub):
    '''
    RADIENS file system commands

    The commands operate on Radiens `data sets`.  A `data set` consists of one or more files that contain
    the primary data and meta data.
    '''
    ctx.obj['hub'] = hub


@ filesys.command(short_help='lists data sets in one or more directories')
@ click.pass_context
@ click.option('-s', '--sort', default='date', help='sort attribute', show_default=True)
@ click.option('-b', '--brief', default=True, type=bool, help='show brief description', show_default=True)
@ click.argument('path', nargs=-1)
def ls(ctx, sort, brief, path):
    '''
    List the Radiens-aware data sets in one or more directories.

    A `data set` represents one set of primary data and its associated meta data in one or more files.
    '''
    path = '.' if len(path) == 0 else path
    try:
        resp = ctx.obj['fsys_client'].ls(path, sort_by=sort, hub_name=ctx.obj['hub'])
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    if resp.num_data_sources == 0:
        print('No Radiens data file sets in requested directory')
        return
    df = resp.datasource_table
    df['bytes_total'] = df['bytes_total'] / 1e6
    df['bytes_total'] = df['bytes_total'].map('{:,.3f}'.format)
    if brief:
        pprint(df[['path', 'base_name', 'type', 'bytes_total', 'timestamp']].rename(
            {'base_name': 'name', 'bytes_total': 'size MB'}, axis='columns'))
    else:
        pprint(df[['path', 'base_name', 'type', 'bytes_total', 'timestamp', 'num_chan', 'dur_sec']].rename({'base_name': 'name',
                                                                                                            'bytes_total': 'size MB',
                                                                                                            'num_chan': 'channels',
                                                                                                            'dur_sec': 'dur (sec)'}, axis='columns'))


@ filesys.command(short_help='copy one data file set')
@ click.pass_context
@ click.argument('source', type=click.STRING)
@ click.argument('dest', type=click.STRING)
@ click.option('-f', '--force', default=False, help='force replace of `dest` if it exists', show_default=True)
def cp(ctx, source, dest, force):
    '''
    Copy one Radiens-aware data file set to a 'dest' data file set.
    '''
    try:
        resp = ctx.obj['fsys_client'].cp(Path(source), Path(dest), force=force, hub_name=ctx.obj['hub'])
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    if resp.num_data_sources == 0:
        print('No data sets were copied : {resp.cmd_msg}')
        return
    click.echo('Copied {} to {} ({}, {} Mb)'.format(Path(source).expanduser().absolute(), Path(resp.datasources[0].descriptor.path,
                                                                                               resp.datasources[0].descriptor.base_name),
                                                    resp.datasources[0].descriptor.file_type,
                                                    resp.datasources[0].stat.num_bytes['total']))


@ filesys.command(short_help='move one data file set')
@ click.pass_context
@ click.argument('source', type=click.STRING)
@ click.argument('dest', type=click.STRING)
@ click.option('-f', '--force', default=True, help='force replace of `dest` if it exists', show_default=True)
def mv(ctx, source, dest, force):
    '''
    Move one Radiens-aware data file set to a 'dest' location.

    source : path to source file set. Use dataset name as in `ls`. Wildcards are allowed.
    dest   : destination location. If `dest` is a directory then the data set name is retained. 

    '''
    try:
        resp = ctx.obj['fsys_client'].mv(Path(source), Path(dest), force=force, hub_name=ctx.obj['hub'])
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    if resp.num_data_sources == 0:
        print('No data sets were moved : {resp.cmd_msg}')
        return
    click.echo('Moved {} to {} ({}, {} Mb)'.format(Path(source).expanduser().absolute(), Path(resp.datasources[0].descriptor.path,
                                                                                              resp.datasources[0].descriptor.base_name),
                                                   resp.datasources[0].descriptor.file_type,
                                                   resp.datasources[0].stat.num_bytes['total']))


@ filesys.command(short_help='remove (delete) one data file set')
@ click.pass_context
@ click.argument('source', type=click.STRING)
def rm(ctx, source):
    '''
    Removes (deletes) one Radiens-aware data file set from the file system. This is irreversible. 

    source : path to source file set. Use dataset name as in `ls`. Wildcards are allowed.

    '''
    try:
        resp = ctx.obj['fsys_client'].rm(Path(source), hub_name=ctx.obj['hub'])
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    if resp.num_data_sources == 0:
        print('Requested data set was not found : {resp.cmd_msg}')
        return
    click.echo('Removed {} ({}, {} Mb)'.format(Path(resp.datasources[0].descriptor.path,
                                                    resp.datasources[0].descriptor.base_name),
                                               resp.datasources[0].descriptor.file_type,
                                               resp.datasources[0].stat.num_bytes['total']))


@ filesys.command(short_help='print meta data for one file set')
@ click.pass_context
@ click.argument('source', type=click.STRING)
def metadata(ctx, source):
    '''
    Prints the meta data for one Radiens-aware data file set.

    source : path to source file set. Use dataset name as in `ls`. Wildcards are allowed.

    '''
    try:
        resp = ctx.obj['fsys_client'].get_data_file_metadata(Path(source), hub_name=ctx.obj['hub'])
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        return
    pprint(resp.table)
