from pathlib import Path
from typing import List
import subprocess
import sys

def _run_robocopy(source_dir: Path, destination_dir: Path, file: str, num_retries: int, verbose: bool, dry_run: bool, unbuffered_IO: bool, flags: List[str] = []) -> int:
    assert num_retries >= 0
    command = [
        'robocopy', str(source_dir), str(destination_dir), file,
        '/mt:8', f'/r:{num_retries}', '/w:1'
    ]
    command.extend(flags)

    if verbose:
        command.append('/v')
        command.append('/x')
    if dry_run:
        command.append('/l')
    if unbuffered_IO:
        command.append('/j')

    print(" ".join(command))
    with subprocess.Popen(command, text=True, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE) as process:
        for out in process.stdout:
            print(out)

        process.wait()
        if process.returncode < 8:
            print(f"robocopy succeeded with return code: {process.returncode}")
        else:
            print(f"robocopy returned error code: {process.returncode}", file=sys.stderr)

        return process.returncode


#
def copy_file(source_file: Path, destination_dir: Path, num_retries: int = 10, verbose: bool = False, dry_run: bool = False, unbuffered_IO: bool = False) -> bool:
    assert source_file.is_file()

    result = _run_robocopy(
        source_dir=str(source_file.parent),
        destination_dir=str(destination_dir),
        file=str(source_file.name),
        num_retries=num_retries,
        verbose=verbose,
        dry_run=dry_run,
        unbuffered_IO=unbuffered_IO
    )
    return result < 8

#
def move_file(source_file: Path, destination_dir: Path, num_retries: int = 10, verbose: bool = False, dry_run: bool = False, unbuffered_IO: bool = False):
    assert source_file.is_file()

    result = _run_robocopy(
        source_dir=str(source_file.parent),
        destination_dir=str(destination_dir),
        file=str(source_file.name),
        num_retries=num_retries,
        verbose=verbose,
        dry_run=dry_run,
        unbuffered_IO=unbuffered_IO,
        flags=['/mov']
    )
    return result < 8

#
def copy_directory(source_dir: Path, destination_dir: Path, recursive: bool = True, num_retries: int = 10, verbose: bool = False, dry_run: bool = False, unbuffered_IO: bool = False) -> bool:
    assert source_dir.is_dir()

    result = _run_robocopy(
        source_dir=str(source_dir),
        destination_dir=str(destination_dir),
        file='*',
        num_retries=num_retries,
        verbose=verbose,
        dry_run=dry_run,
        unbuffered_IO=unbuffered_IO,
        flags=['/e'] if recursive else []
    )
    return result < 8

#
def move_directory(source_dir: Path, destination_dir: Path, recursive: bool = True, num_retries: int = 10, verbose: bool = False, dry_run: bool = False, unbuffered_IO: bool = False) -> bool:
    assert source_dir.is_dir()

    result = _run_robocopy(
        source_dir=str(source_dir),
        destination_dir=str(destination_dir),
        file='*',
        num_retries=num_retries,
        verbose=verbose,
        dry_run=dry_run,
        unbuffered_IO=unbuffered_IO,
        flags=['/move', '/e'] if recursive else ['/move']
    )
    return result < 8

#
def mirror_directory(source_dir: Path, destination_dir: Path, num_retries: int = 10, verbose: bool = False, dry_run: bool = False, unbuffered_IO: bool = False) -> bool:
    assert source_dir.is_dir()

    result = _run_robocopy(
        source_dir=str(source_dir),
        destination_dir=str(destination_dir),
        file='*',
        num_retries=num_retries,
        verbose=verbose,
        dry_run=dry_run,
        unbuffered_IO=unbuffered_IO,
        flags=['/mir', '/im']
    )
    return result < 8
