# GPU_Utils
Help you find free gpu and analyze gpu usage when using a gpu server shared with others.

People usually used a gpu server shared with others, it is annoying to set free gpu every time, and it is difficult to know who is using the gpu and how much memory they used. You can use this tool to show some basic information about the gpu server.

## Install
## From Pip
```bash
pip install gpustatus
```
### From Source
```bash
git clone https://github.com/coding-famer/GPU_Utils
cd GPU_Utils
python setup.py install
```
Or install with editable mode (i.e. changes to the source code will be reflected in the installed package immediately):
```bash
git clone https://github.com/coding-famer/GPU_Utils
cd GPU_Utils
pip install -e .
```

## Usage
```bash
$ gpustatus --show-all
$ gpustatus --show-by-user [username]
$ gpustatus --show-by-gpu [gpu_id]
```