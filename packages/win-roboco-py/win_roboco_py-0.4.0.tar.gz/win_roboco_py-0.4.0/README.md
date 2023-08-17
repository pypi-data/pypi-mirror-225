# win-roboco-py
A thin python wrapper around Window's [Robocopy](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy) utility.

This package is not intended to cover 100% of Robocopy's functionality.
Instead, the focus of the package is allow you to easily take advantage of Robocopy's robustness for the most common operations.

# Contributions
Pull requests or issue tickets are very welcome and appreciated.

# Quick Usage

```python
import win_roboco_py as robo

# Copies the file to the destination, with the same filename.
robo.copy_file(Path('./src/file.txt'), Path('./dst'))

# Copies the file to the destination, then deletes the source file.
robo.move_file(Path('./src/file.txt'), Path('./dst'))

# Copies all files to the destination.
robo.copy_directory(Path('./src'), Path('./dst'), recursive=True)

# Copies all files to the destination, then deletes the sources.
robo.move_directory(Path('./src'), Path('./dst'), recursive=False)

# Copies all files to the destination, and deletes extra files.
robo.mirror_directory(Path('./src'), Path('./dst'))
```
