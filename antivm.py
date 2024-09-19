import os
import psutil
import uuid
import platform

class VMDetection:

    def detect_sandbox(self):
        sandbox_artifacts = [
            # Windows artifacts
            "C:\\windows\\system32\\drivers\\sbiedrv.sys",
            "C:\\windows\\system32\\drivers\\VBoxMouse.sys",
            "C:\\windows\\system32\\drivers\\VBoxGuest.sys",
            "C:\\windows\\system32\\drivers\\VBoxSF.sys",
            "C:\\windows\\system32\\vboxdisp.dll",
            "C:\\windows\\system32\\vboxhook.dll",
            "C:\\windows\\system32\\vboxmrxnp.dll",
            "C:\\windows\\system32\\vboxogl.dll",
            "C:\\windows\\system32\\vboxoglarrayspu.dll",
            "C:\\windows\\system32\\vboxoglcrutil.dll",
            "C:\\windows\\system32\\vboxoglerrorspu.dll",
            "C:\\windows\\system32\\vboxoglfeedbackspu.dll",
            "C:\\windows\\system32\\vboxoglpackspu.dll",
            "C:\\windows\\system32\\vboxoglpassthroughspu.dll",
            "C:\\windows\\system32\\vboxservice.exe",
            "C:\\windows\\system32\\vboxtray.exe",
            "C:\\windows\\system32\\vmacthlp.exe",
            "C:\\windows\\system32\\vmtools.dll",
            "C:\\windows\\system32\\vmtray.exe",
            "C:\\windows\\system32\\vmusrvc.exe",
            "C:\\windows\\system32\\vmvss.dll",
            "C:\\windows\\system32\\xenguestagent.exe",
            "C:\\windows\\system32\\xenservice.exe",
            "C:\\windows\\system32\\drivers\\NPF.sys",
            "C:\\windows\\system32\\drivers\\vmusbmouse.sys",
            "C:\\windows\\system32\\drivers\\vmmouse.sys",
            "C:\\windows\\system32\\drivers\\vmxnet.sys",
            "C:\\windows\\system32\\drivers\\vmscsi.sys",
            "C:\\windows\\system32\\drivers\\vmhgfs.sys",
            "C:\\windows\\system32\\drivers\\VBoxDrv.sys",
            "C:\\windows\\system32\\drivers\\VBoxUSBMon.sys",
            "C:\\windows\\system32\\drivers\\VBoxNetAdp.sys",
            "C:\\windows\\system32\\drivers\\VBoxNetFlt.sys",
            # Linux artifacts
            "/usr/bin/vmtoolsd",
            "/usr/bin/VBoxService",
            "/usr/bin/qemu-ga",
            "/usr/sbin/virt-what",
            "/usr/bin/vboxclient",
            "/usr/bin/xenstore-ls",
            "/usr/sbin/xenstored",
            "/usr/libexec/qemu-kvm",
            "/proc/scsi/scsi",  # Virtual devices in Linux
            "/proc/modules",  # Kernel modules to check for vm-related modules
            "/sys/devices/virtual/dmi/id/product_name",
            "/sys/devices/virtual/dmi/id/product_version",
            "/etc/rc.d/init.d/virtualbox-guest-additions"
        ]
        for artifact in sandbox_artifacts:
            if os.path.exists(artifact):
                return True
        return False

    def check_vm_processes(self):
        vm_processes = ['vmtoolsd', 'vboxservice', 'vboxtray', 'qemu-ga']
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] in vm_processes:
                return True
        return False

    def check_mac(self):
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                        for elements in range(0, 2*6, 8)][::-1])
        vm_mac_prefixes = [
            '00:05:69',  # VMware
            '00:0C:29',  # VMware
            '00:50:56',  # VMware
            '08:00:27',  # VirtualBox
            '52:54:00',  # QEMU
        ]
        for prefix in vm_mac_prefixes:
            if mac.startswith(prefix):
                return True
        return False

    def check_dmi(self):
        if platform.system() == "Linux":
            if os.path.exists('/sys/class/dmi/id/product_name'):
                with open('/sys/class/dmi/id/product_name') as f:
                    product_name = f.read().strip()
                    if any(vm in product_name for vm in ['VirtualBox', 'VMware', 'QEMU']):
                        return True
        elif platform.system() == "Windows":
            output = os.popen("systeminfo").read()
            if any(vm in output for vm in ['VirtualBox', 'VMware', 'QEMU']):
                return True
        return False

    def check_cpu_count(self):
        if os.cpu_count() <= 2:
            return True
        return False

    def is_vm(self):
        if (self.detect_sandbox() or
            self.check_vm_processes() or
            self.check_mac() or
            self.check_dmi() or
            self.check_cpu_count()):
            return True
        return False


# example usage
vm_detection = VMDetection()

if vm_detection.is_vm():
    print("Virtual machine detected!")
else:
    print("No virtual machine detected.")
