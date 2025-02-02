# Getting Started With Python Development in RPI Project

So you've followed the [Getting Started](GettingStarted.md) guide, and you can now open VSCode in the main SpectraSolis HASP-2025 workspace. Now we are ready to get started writing code!

## Open the RPI DevContainer
Go ahead and open VSCode into your HASP-2025 workspace, if it is not already open. (open the ~/development/HASP-2025 in your VSCode editor). 

Next, ensure Docker Desktop is running. This will allow VScode to open the configured devContainers in the project.

In VScode, press the command shortcut Ctrl+Shift+P, search up and select the command "Dev Containers: Reopen in Container" 

Select the RPI container, and wait for vscode to reopen your environment. 

## Explore your environment
You now have a fully featured Python Development Environment at your fingertips. Here we will point out a few important features

- [Python Language Extensions](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)
- [Python Unittest](https://code.visualstudio.com/docs/python/testing)

The Language Extension adds python language support to VSCode, allowing you to develop in the Python language. 

The Dubugger adds a fully featured Python Debugger, allowing you to add breakpoints and debug your code line-by-line

### Python Unittest
The Python Language Extension also adds support for creating Unit Tests for your code. I strongly recommend you go to the [Python Unittest](https://code.visualstudio.com/docs/python/testing) 
Tutorial page and learning how this feature works. 

Python Unit testing for the RPI project is set up in the rpi/HASP_25_RPI/test folder. Any python file you 
create in this folder with the word "test" in its name will be registered in the Testing tab at the left of your VSCode IDE.

Please review any existing tests for examples on how to create and run Python Unit Tests. 

### Unit Tests are Required
Please Note that ___all code contributions___ should have an associated test. Code contributions which cannot be 
tested will undergo extra scrutiny, and must have an integration test plan.

### Building C/Cpp for Python bindings
Currently I am looking at phasing out the C library. I don't think it's necessary as we may just "extern c" any c code in CPP.

granted you have a written a pybind11 binding file for C++, or have used the keyword "EXPORT" to export your C functions, you may build the python project with the following steps:

1) load up RPI dev container
2) use CMake extension to execute the configure and build commands
3) in terminal, execute "pip install ." command in root workspace folder to use scikit-build to build the module binary
4) import the lib in python file C++ example: CRC.py, C example: bind_test.py
5) run python program


### Developing C/CPP in propeller container
C/CPP code can be developed in the propeller container. I would recommend developing c/cpp in propeller, then determining if and how it needs to be bound into python.

Code which is meant to be run on the Propeller should conform to C99 standard, as this is the standard which our compiler for the Propeller (flexcc) can compile. flexcc can also compile basic CPP structures and functionality such as code-in-structs and classes. This is why we utilize a CPP compiler for testing our library. You can find more details on flexcc [Here](https://github.com/totalspectrum/spin2cpp/blob/master/doc/general.md)