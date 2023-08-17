import os
from pathlib import Path
from typing import Final

import pyperclip
import typer
from beni import bcolor, bfile, bfunc, binput, bpath, btask
from beni.btype import Null

from . import bin, venv

app: Final = btask.newSubApp('BTask 工具')


@app.command()
@bfunc.syncCall
async def create(
    project_path: Path = typer.Argument(None, help="项目路径"),
):
    '创建 BTask 项目'
    if not project_path:
        project_path = Path.cwd()
    if project_path.exists():
        await binput.confirm(f'项目路径 {project_path} 已存在，是否覆盖？')
    await bfile.makeFiles(_files, project_path)
    init(project_path)


@app.command()
@bfunc.syncCall
async def init(
    project_path: Path = typer.Argument(None, help="项目路径"),
):
    '初始化 BTask 项目，包括 venv 和 bin 操作'
    if not project_path:
        project_path = Path.cwd()
    venv.venv(
        packages=Null,
        path=project_path,
        disabled_mirror=False,
        quiet=True,
    )
    bin.download(
        names=Null,
        file=project_path / 'bin.list',
        output=project_path / 'bin',
    )


@app.command()
@bfunc.syncCall
async def export(
    project_path: Path = typer.Argument(None, help="项目路径"),
):
    '导出文件内容到剪贴板'
    if not project_path:
        project_path = Path.cwd()
    ignores = [
        project_path / 'bin',
        project_path / 'venv',
        project_path / 'venv.lock',
    ]
    files = await bpath.listFile(project_path, True)
    files = [x for x in files if '__pycache__' not in x.parts]
    contents: list[str] = []
    for file in files:
        for ignore in ignores:
            if file.is_relative_to(ignore):
                break
        else:
            contents.append(f'>>> {str(file.relative_to(project_path)).replace(os.path.sep, "/")}\n{await bfile.readText(file)}')
    contents.sort()
    content = '_files = \'\'\'\n' + '\n\n\n'.join(contents) + '\n\'\'\''
    pyperclip.copy(content)
    bcolor.printGreen('已复制到剪贴板')


@app.command()
@bfunc.syncCall
async def tidy(
    tasks_path: Path = typer.Argument(None, help="tasks 路径"),
):
    '整理 tasks 文件'
    initFile = tasks_path / '__init__.py'
    assert initFile.is_file(), f'文件不存在 {initFile}'
    files = await bpath.listFile(tasks_path)
    files = [x for x in files if not x.name.startswith('_')]
    contents = [f'from . import {x.stem}' for x in files]
    contents.insert(0, '# type: ignore')
    contents.append('')
    content = '\n'.join(contents)
    await bfile.writeText(
        initFile,
        content,
    )
    print(content)


_files = '''
>>> .gitignore
__pycache__
bin/
venv/


>>> bin.list



>>> src/.vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "debug",
            "type": "python",
            "request": "launch",
            // "console": "internalConsole",
            "program": "${workspaceFolder}/main.py",
        }
    ],
}


>>> src/.vscode/settings.json
{
    "files.exclude": {
        "**/__pycache__": true,
        ".pytest_cache": true,
    },
    "python.defaultInterpreterPath": "${workspaceFolder}/../venv/Scripts/python.exe",
}


>>> src/.vscode/tasks.json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "git commit",
            "type": "shell",
            "problemMatcher": [],
            "command": "TortoiseGitProc.exe",
            "args": [
                "/command:commit",
                "/path:${workspaceFolder}/../../",
            ],
        },
        {
            "label": "git commit file",
            "type": "shell",
            "problemMatcher": [],
            "command": "TortoiseGitProc.exe",
            "args": [
                "/command:commit",
                "/path:${file}",
            ],
        },
        {
            "label": "git pull",
            "type": "shell",
            "problemMatcher": [],
            "command": "TortoiseGitProc.exe",
            "args": [
                "/command:pull",
                "/path:${workspaceFolder}/../../",
            ],
        },
        {
            "label": "git revert",
            "type": "shell",
            "problemMatcher": [],
            "command": "TortoiseGitProc.exe",
            "args": [
                "/command:revert",
                "/path:${workspaceFolder}/../../",
            ],
        },
        {
            "label": "git sync",
            "type": "shell",
            "problemMatcher": [],
            "command": "TortoiseGitProc.exe",
            "args": [
                "/command:sync",
                "/path:${workspaceFolder}/../../",
            ],
        },
        {
            "label": "git log",
            "type": "shell",
            "problemMatcher": [],
            "command": "TortoiseGitProc.exe",
            "args": [
                "/command:log",
                "/path:${workspaceFolder}/../../",
            ],
        },
        {
            "label": "git log file",
            "type": "shell",
            "problemMatcher": [],
            "command": "TortoiseGitProc.exe",
            "args": [
                "/command:log",
                "/path:${file}",
            ],
        },
        {
            "label": "tasks tidy",
            "type": "shell",
            "problemMatcher": [],
            "command": "beni",
            "args": [
                "task",
                "tidy",
                "${workspaceFolder}/tasks"
            ],
        },
    ],
}


>>> src/main.py
import asyncio

from beni import btask

from tasks import *

btask.options.lock = 'bcmd'
asyncio.run(btask.main())

# python main.py hello
# python main.py sub haha



>>> src/tasks/__init__.py
# type: ignore
from . import hello
from . import sub



>>> src/tasks/hello.py
from typing import Final

from beni import bfunc, btask

app: Final = btask.app


@app.command()
@bfunc.syncCall
async def hello():
    '打印 hello'
    print('hello')


>>> src/tasks/sub.py
from typing import Final

from beni import bfunc, btask

app: Final = btask.newSubApp('子工具集')


@app.command()
@bfunc.syncCall
async def haha():
    '打印 haha'
    print('haha')


@app.command()
@bfunc.syncCall
async def bye():
    '打印 bye'
    print('bye')


>>> venv.list
aioconsole
aiofiles
aiohttp
aiosqlite
autopep8
benimang==0.4.21
nest-asyncio
orjson
portalocker
pretty_errors
prettytable
pydantic
pyinstaller
pyyaml
qiniu
typer
'''
