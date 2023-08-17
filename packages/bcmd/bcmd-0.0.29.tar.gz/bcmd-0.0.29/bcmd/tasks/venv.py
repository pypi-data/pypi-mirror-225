import os
from pathlib import Path
from typing import Final

import typer
from beni import bexecute, bfile, bfunc, binput, bpath, btask

app: Final = btask.app


@app.command()
@bfunc.syncCall
async def venv(
    packages: list[str] = typer.Argument(None),
    path: Path = typer.Option(None, '--path', '-p', help='指定路径，默认当前目录'),
    disabled_mirror: bool = typer.Option(False, '--disabled-mirror', '-d', help='是否禁用镜像'),
    quiet: bool = typer.Option(False, '--quiet', '-q', help='是否安静模式'),
):
    'python 虚拟环境配置'
    packages = packages or []
    async with bpath.useTempFile() as tempFile:
        pipIniFile = bpath.user('pip/pip.ini')
        if disabled_mirror and pipIniFile.is_file():
            await bpath.move(pipIniFile, tempFile)
        try:
            path = path or Path(os.getcwd())
            venvPath = bpath.get(path, 'venv')
            assertPath(venvPath)
            if not venvPath.exists() and not quiet:
                await binput.confirm('指定目录为非venv目录，是否确认新创建？')
            if not venvPath.exists():
                await bexecute.run(f'python.exe -m venv {venvPath}')
            venvLockFile = bpath.get(path, 'venv.lock')
            assertFile(venvLockFile)
            venvListFile = bpath.get(path, 'venv.list')
            assertFile(venvListFile)
            if not venvListFile.exists():
                await bfile.writeText(venvListFile, '')
            await tidyVenvFile(venvListFile, packages)
            if venvLockFile.exists():
                await tidyVenvFile(venvLockFile, packages)
                targetFile = venvLockFile
            else:
                targetFile = venvListFile
            pip = bpath.get(venvPath, 'Scripts/pip.exe')
            await pipInstall(pip, targetFile)
            await bexecute.run(f'{pip} freeze > {venvLockFile}')
        finally:
            if tempFile.is_file():
                await bpath.move(tempFile, pipIniFile, True)


async def pipInstall(pip: Path, file: Path):
    python = pip.with_name('python.exe')
    assert python.is_file()
    assert pip.is_file()
    assert not await bexecute.run(f'{python} -m pip install --upgrade pip'), '更新 pip 失败'
    assert not await bexecute.run(f'{pip} install -r {file}'), '执行失败'


async def tidyVenvFile(file: Path, packages: list[str]):
    packageNames = [getPackageName(x) for x in packages]
    ary = (await bfile.readText(file)).strip().replace('\r', '').split('\n')
    ary = list(filter(lambda x: getPackageName(x) not in packageNames, ary))
    ary.extend(packages)
    ary.sort()
    await bfile.writeText(file, '\n'.join(ary).strip())


def getPackageName(value: str):
    sep_ary = ['>', '<', '=']
    for sep in sep_ary:
        if sep in value:
            return value.split(sep)[0]
    return value


def assertFile(file: Path):
    assert file.is_file() or not file.exists(), f'必须是文件 {file=}'


def assertPath(folder: Path):
    assert folder.is_dir() or not folder.exists(), f'必须是目录 {folder=}'
