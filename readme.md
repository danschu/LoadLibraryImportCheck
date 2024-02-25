### Basics

Sometimes a Windows-Library (*.dll or *.pyd) can not be loaded, because some other libraries are missing. Then the error "```ImportError: DLL load failed```" is shown. A Windows-Library (or Windows-Program) can load other Windows-Library dynamically (with ```LoadLibraryA/W``` from ```kernel32.dll```) or statically with the ```PE import directory table```.

For static linked libraries windows will only show an error message, but no further information (eg. which library could not be loaded).

The Idea of the program is:

1. Load the Library with `win32api.LoadLibrary` and check if it can be loaded:
   1. If it was loaded --> finish
   2. If it was not loaded --> 
      1. Loop through all static referenced libraries in the import directories of the library and try loading them indiviually (start at the beginning)



### Usage

If you want to inspect a library, then run:

```
python checkdll <path_to_dll> [--full_inspect]
```

#### Example (1)
##### Call:

```
python checkdll "cudnn_adv_infer64_8.dll" --full_inspect
```

##### Output:

```
Handle (0x7ffa1b0d0000): api-ms-win-core-rtlsupport-l1-1-0.dll in 'C:\Windows\SYSTEM32'
Handle (0x7ffa18760000): KERNELBASE.dll in 'C:\Windows\System32'
Handle (0x7ffa19540000): KERNEL32.dll in 'C:\Windows\System32'
Handle (0x7ff927b30000): cudnn_ops_infer64_8.dll in 'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin'
Handle (0x7ff8b9a30000): cudnn_adv_infer64_8.dll in 'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin'
Errors detected: 0
```
#### Example (2)

##### Call:
```
python checkdll "gpujpeg.cp39-win_amd64.pyd" --full_inspect
```

```gpujpeg.cp39-win_amd64.pyd``` loads ```gpujpeg.dll```, which was missing:

##### Output:

```
Handle (NONE): gpujpeg.dll
Handle (0x7ffa1b0d0000): ntdll.dll in 'C:\Windows\SYSTEM32'
Handle (0x7ffa18760000): api-ms-win-core-console-l1-1-0.dll in 'C:\Windows\System32'
Handle (0x7ffa19540000): api-ms-win-core-processthreads-l1-1-0.dll in 'C:\Windows\System32'
Handle (0x7ffa19490000): msvcrt.dll in 'C:\Windows\System32'
Handle (0x7ffa0f0e0000): VERSION.dll in 'C:\Windows\SYSTEM32'
Handle (0x7ffa19820000): RPCRT4.dll in 'C:\Windows\System32'
Handle (0x7ffa19070000): WS2_32.dll in 'C:\Windows\System32'
Handle (0x7ffa18b40000): bcrypt.dll in 'C:\Windows\System32'
Handle (0x7ffa1a520000): api-ms-win-eventing-controller-l1-1-0.dll in 'C:\Windows\System32'
Handle (0x7ffa19740000): ADVAPI32.dll in 'C:\Windows\System32'
Handle (0x7ffa18520000): api-ms-win-crt-runtime-l1-1-0.dll in 'C:\Windows\System32'
Handle (0x7ffa0b240000): VCRUNTIME140.dll in 'C:\Users\xxxx\AppData\Local\Programs\Python\Python39'
Handle (0x7ff9cf460000): python39.dll in 'C:\Users\xxxx\AppData\Local\Programs\Python\Python39'
Handle (0x7ff9fdea0000): VCRUNTIME140_1.dll in 'C:\Users\xxxx\AppData\Local\Programs\Python\Python39'
Handle (NONE): gpujpeg.cp39-win_amd64.pyd
Errors detected: 2
```

#### Fix:
Add the directory containing the ```gpujpeg.dll``` to python:
```python
import os
os.add_dll_library("path to gpujpeg.dll")
```

or add this directory to the windows environent variable ```PATH```.