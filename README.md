# Anti-VM Detection Script

This Python script is designed to detect if the current environment is a virtual machine or sandbox. It checks for various system artifacts, running processes, MAC addresses, and CPU details that are typically found in virtualized environments such as VirtualBox, VMware, and QEMU.

## Features

- **Sandbox Detection**: Checks for common artifacts related to sandboxes and virtual environments on Windows and Linux.
- **Process Scanning**: Identifies VM-related processes such as `vmtoolsd`, `vboxservice`, and `qemu-ga`.
- **MAC Address Check**: Detects known MAC address prefixes used by virtualization software.
- **DMI Check**: Inspects DMI information to identify VirtualBox, VMware, or QEMU instances.
- **CPU Count Check**: Flags environments with two or fewer CPUs, which is common in VM setups.

## How It Works

The script runs several checks:
1. **Sandbox Artifacts**: It looks for specific files that indicate the presence of a virtual machine.
2. **VM Processes**: Scans running processes for known VM-related names.
3. **MAC Address**: Compares the system's MAC address to known VM vendor prefixes.
4. **DMI Data**: Checks system information like `product_name` to see if it contains VM indicators.
5. **CPU Count**: Flags systems with fewer than 3 CPUs.

If any of these checks return a positive result, the script will conclude that it is running in a virtual machine.

## Usage

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/antivm-detection.git
    cd antivm-detection
    ```

2. Install the required dependencies:
    ```bash
    pip install psutil
    ```

3. Run the script:
    ```bash
    python antivm.py
    ```

The script will output:
- `Virtual machine detected!` if a VM or sandbox is detected.
- `No virtual machine detected.` if no VM characteristics are found.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributions

Feel free to submit issues or pull requests if you encounter any problems or have suggestions for improvement.

