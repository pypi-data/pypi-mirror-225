import json
import typer
from typing import Optional
from rich import print
from rich.table import Table

from scoamp.api import AmpApi
from ..utils.api_utils import (ApiEnv, save_auth, load_auth, PAGE_MAX)
from ..utils.helper import format_datetime
from ..utils.error import (NotLoginError, err_wrapper)

app = typer.Typer(name='api')

@app.command(help='login user')
def login(
    access_key: Optional[str] = typer.Option(None, '-ak', '--access-key'),
    secret_key: Optional[str] = typer.Option(None, '-sk', '--secret-key'),
    env: ApiEnv = typer.Option(ApiEnv.standard.value, help="login server, use 'custom' to specify your arbitrary address")
    ):
    # parameter validation
    env_name, endpoint = env.value, env.endpoint()
    if env is ApiEnv.custom:
        env_name = typer.prompt('Env name')

    # check already exists auth
    auth_info = None
    try:
        auth_info = load_auth(env_name)
    except NotLoginError:
        pass
    else:
        if env is ApiEnv.custom:
            flag = typer.confirm(f"Found already logined env '{auth_info.endpoint}', use it?")
            if flag:
                endpoint = auth_info.endpoint
            else:
                auth_info  = None

    if not endpoint:
        endpoint = typer.prompt('Env endpoint')
    print(f'Environment ({env_name}): {endpoint}')

    if auth_info and not access_key:
        flag = typer.confirm(f"Found already logined access key '{auth_info.access_key}', use it?")
        if flag:
            access_key = auth_info.access_key
            secret_key = auth_info.secret_key

    # normal
    if not access_key:
        access_key = typer.prompt('Input access key')
    if not secret_key:
        secret_key = typer.prompt('Input secret key', hide_input=True)

    # auth validation
    api = AmpApi(access_key, secret_key, endpoint)
    _ = api.get_user_info()

    # cache auth
    save_auth(env_name, endpoint, access_key, secret_key)

    print("Login Succeed!")


@app.command(help="list user's models")
@err_wrapper
def list(
    n: int = typer.Option(-1, '-n', '--num', min=-1, max=PAGE_MAX, help="max record numbers, '-1' for all"),
    s: Optional[str] = typer.Option(None, '-s', '--search', help="fuzzy search keyword for model name"),
    simple: bool = typer.Option(False, help='simple json formatted output')
    ):
    # load auth info from cache
    auth = load_auth()

    # make request
    api = AmpApi(**auth.asdict())
    jr = api.list_user_models(n, s)
    if not jr:
        print("Nothing returned.")
        raise typer.Exit(0)

    # parse response and print result
    models, page = jr['models'], jr['page']
    count, total = page['size'], page['total']
    res = []
    for m in models:
        meta = m['metadata']
        tags = meta['tags']
        tags.extend(filter(lambda x: x, (meta['training_frameworks'], meta['type'], meta['algorithm'], meta['industry'])))
        res.append({
            'display_name': m['display_name'],
            'name': m['name'],
            'repository_uri': m['repository_uri'],
            'owner_name': m['owner_name'],
            'tags': tags,
            'create_time': m['create_time'],
            'update_time': m['update_time']
        })

    if simple:
        print(json.dumps(res, indent=2))
    else:
        table = Table(title=f'Model Information({count}/{total})', show_lines=True, show_edge=True)
        for header in ('Name', 'ID', 'URL', 'Owner', 'Tags', 'Created', 'Updated'):
            table.add_column(header, style='cyan', overflow='fold')
        for r in res:
            table.add_row(r['display_name'], r['name'], r['repository_uri'], r['owner_name'],
                          ','.join(r['tags']), format_datetime(r['create_time']), format_datetime(r['update_time']),
                         )

        print(table)



@app.command(help="command stub", hidden=True)
@err_wrapper
def stub(
    ):
    # load auth info from cache
    #auth = load_auth()

    # make request
    #from scoamp.api import set_auth_info, set_endpoint
    #set_endpoint(auth.endpoint)
    #set_auth_info(auth.access_key, auth.secret_key)

    from scoamp.globals import global_api
    from scoamp.toolkit import model_file_download, snapshot_download
    model_id = 'test-0714-2'
    file_path = 'mock1.bin'
    local_dir = 'data/model'
    is_public = False
    #r = model_file_download(
    #    model_id=model_id,
    #    file_path=file_path,
    #    local_dir=local_dir,
    #    remote_validate=False,
    #    is_public=is_public,
    #) 
    r = snapshot_download(model_id=model_id, local_dir=local_dir,)
    print(r)

 