# Korbit

Korbit mentor CLI will allow you to analyze any local files.

## Development

### Set environment variables

Fill the missing values.

```sh
cp .env.example .env
```

### Create env

```
conda env update -f environment.yml -n korbit-cli
```

### Run

If you don't have the environment variables set you can use the login command and export at least `KORBIT_HOST` to use dev server for testing.

```sh
python korbit.py login

export KORBIT_HOST=https://oracle.korbit.ai:8000
python korbit.py scan example/subfolder


# Or
KORBIT_HOST=https://oracle.korbit.ai:8000 python korbit.py scan example/subfolder
```

### Troubleshooting

We are using Python=3.11.3 because 3.11.4 and pyinstaller are causing a crash on execution of the script.

https://stackoverflow.com/a/76731974

<details>
<summary>Exception on python==3.11.4</summary>

```
❯ dist/korbit example/subfolder
[8650] Module object for pyimod02_importers is NULL!
Traceback (most recent call last):
  File "PyInstaller/loader/pyimod02_importers.py", line 22, in <module>
  File "pathlib.py", line 14, in <module>
  File "urllib/parse.py", line 40, in <module>
ModuleNotFoundError: No module named 'ipaddress'
Traceback (most recent call last):
  File "PyInstaller/loader/pyiboot01_bootstrap.py", line 17, in <module>
ModuleNotFoundError: No module named 'pyimod02_importers'
[8650] Failed to execute script 'pyiboot01_bootstrap' due to unhandled exception!
```

</details>

## Installation

### Pip

To install Korbit, you can use pip:

```
pip install korbit-mentor
```

### Binary

#### Linux - MacOS

1. Automatically installation

```sh
curl https://mentor-resources.korbit.ai/cli/installer.sh | bash
```

1. Linux and Macos x86

```sh
wget https://mentor-resources.korbit.ai/cli/korbit-x86_64 -O /usr/bin/local/korbit
```

1. MacOS arm64

```sh
wget https://mentor-resources.korbit.ai/cli/korbit-aarch64 -O /usr/bin/local/korbit
```

#### Windows

```sh
wget https://mentor-resources.korbit.ai/cli/korbit-win.exe -O korbit.exe
```

## Usage

To use Korbit, simply run the `korbit` command followed by the path of the file or folder you want to zip. For example, to zip the current folder, you can run:

```
python -m korbit example/subfolder
```

This will create a zip file containing all the files and folders in the current directory.

## Contributing

Contributions are welcome! If you have any bug reports, feature requests, or suggestions, please open an issue or submit a pull request.

## Contact

If you have any questions or need further assistance, feel free to reach out to us at [support@korbit.ai](mailto:support@korbit.ai).
