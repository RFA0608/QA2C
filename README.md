# QA2C
QA2C provides the drive code for encrypted control for the Quanser Aero 2 model.
The code transforms dynamic controllers through various methods and then drives the system through homomorphic encryption.
The cryptographic libraries for computational homomorphic use [OpenFHE-python](https://github.com/openfheorg/openfhe-python).
The code use Quanser's Aero 2 model [Aero 2](https://github.com/quanser/Quanser_Academic_Resources/tree/dev-windows) Python API. 
**Share implementation concept with [QQS3C](https://github.com/RFA0608/QQS3C)**

--- 

## Implementation direction
The code was implemented through data communication with the Quanser API via TCP/IP in order to use openFHE-python that can be run in a Linux environment(**v15 release later version doesn't work, please use v14 release version of openfhe-python**), since the Quanser hardware API is provided only for Python and runs in a Windows environment. 

``` mermaid
graph LR
    subgraph Windows_Host [Windows Host: Plant]
        A[Quanser Hardware / QLab] <--> B[Python API / C++ SDK]
        B <--> C{TCP Server}
    end

    subgraph WSL_Guest [WSL / Remote: Controller]
        D{TCP Client} <--> E[Encrypted Controller]
        E --- F[SEAL / OpenFHE / Lattigo]
    end

    C <--> |TCP/IP| D
```

---

## Features
The code implements controller versions in Python.
The interfacing code for the Python simulator and the actual hardware, corresponding to each controller, can be found in the "interface/plant" directory.
The actual device consists of a single file, "plant.py" in "interface/plant/py/hardware".

### Controller description
This code Just simple example of encrypted controller with full state feedback.

## How to use
It explains the preparations before use, how to use the Ouanser Interactive Labs, and how to use the actual hardware.
You can follow same instructions [QQS3C](https://github.com/RFA0608/QQS3C).

# Demonstration
1. Quanser Interactive Labs Test:
https://youtu.be/sjIdI3azCwo

> **[INFO] Security**
> 
> - "ctrl_fs_enc.py" satisfy 128-bit lambda security.

# Contact
If you need help or explanation while using this library, please send me an email below and I will respond.

- jeongmingyu@cdslst.kr (Mingyu Jeong)
- leesangwon@cdslst.kr (Sangwon Lee)
- leedonghyun@cdslst.kr (Donghyun Lee)

Provided by SEOULTECH CDSL.

# Licenses & Acknowledgements
This project utilizes code from several open-source projects. We express our gratitude to their developers. The licenses for these dependencies are listed below.

* **Quanser Academic Resources**
    * Licensed unser the [BSD 3-Clause License](https://github.com/quanser/Quanser_Academic_Resources/blob/dev-windows/LICENSE)
      
* **Lattigo (v6)**
    * Licensed under the [Apache License 2.0](https://github.com/tuneinsight/lattigo/blob/main/LICENSE)

* **Microsoft SEAL**
    * Licensed under the [MIT License](https://github.com/microsoft/SEAL/blob/main/LICENSE)

* **CDSL-EncryptedControl**
    * Licensed under the [MIT License](https://github.com/CDSL-EncryptedControl/CDSL/blob/main/LICENSE)

* **OpenFHE (Python)**
    * Licensed under the [BSD 2-Clause License](https://github.com/openfheorg/openfhe-python/blob/main/LICENSE)

* **Numpy**
    * Licensed under the [BSD 3-Clause License](https://github.com/numpy/numpy/blob/main/LICENSE.txt)

* **Matplotlib**
    * Licensed under the [PSF-style License](https://github.com/matplotlib/matplotlib/blob/main/LICENSE/LICENSE)

* **Python Control Systems Library (python-control)**
    * Licensed under the [BSD 3-Clause License](https://github.com/python-control/python-control/blob/main/LICENSE)
