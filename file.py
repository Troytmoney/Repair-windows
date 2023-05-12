import os
import platform
import winreg
import requests


def get_user_choice(message, options):
    while True:
        print(message)
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")
        choice = input("Enter your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]


def scan_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.exists(file_path):
                print(f"Replacing missing file: {file_path}")
                download_and_replace(file_path)


def scan_registry(registry_key, subkey):
    try:
        key = winreg.OpenKey(registry_key, subkey, 0, winreg.KEY_READ)
        num_values = winreg.QueryInfoKey(key)[1]

        for i in range(num_values):
            value_name, value_data, value_type = winreg.EnumValue(key, i)
            if value_type == winreg.REG_SZ:
                if not os.path.exists(value_data):
                    print(f"Replacing missing file: {value_data}")
                    download_and_replace(value_data)

    except WindowsError:
        pass


def download_and_replace(file_path):
    # Adjust the download URL based on the file path and Windows version
    windows_version = get_windows_version()

    # Replace the following URL placeholders with appropriate download URLs for different Windows versions
    source_url = {
        "Windows XP": "http://example.com/files/win_xp/",
        "Windows 7": "http://example.com/files/win_7/",
        "Windows 10": "http://example.com/files/win_10/",
    }

    if windows_version in source_url:
        file_name = os.path.basename(file_path)
        download_url = source_url[windows_version] + file_name

        response = requests.get(download_url)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
                print(f"Downloaded and replaced: {file_path}")
        else:
            print(f"Failed to download: {file_path}")
    else:
        print(f"Unsupported Windows version: {windows_version}")


def get_windows_version():
    return platform.release()


# User choices
replace_missing_files = get_user_choice("Do you want to replace missing files in the Windows folder and registry?",
                                       ["Yes", "No"])
replace_modified_files = get_user_choice("Do you want to replace modified Windows files not changed by the OS?",
                                         ["Yes", "No"])
hard_drive_choice = get_user_choice("Select the target hard drive:",
                                    ["Current Drive", "VMware Virtual Machine", "VirtualBox Machine", "Hyper-V Machine"])

if hard_drive_choice == "Current Drive":
    folder_to_scan = r"C:\Windows\System32"
elif hard_drive_choice == "VMware Virtual Machine":
    vm_name = input("Enter the VMware virtual machine name: ")
    folder_to_scan = r"C:\Path\to\VMware\Virtual\Machines\%s" % vm_name
elif hard_drive_choice == "VirtualBox Machine":
    vm_name = input("Enter the VirtualBox virtual machine name: ")
    folder_to_scan = r"C:\Path\to\VirtualBox\VMs\%s" % vm_name

elif hard_drive_choice == "Hyper-V Machine":
    vm_name = input("Enter the Hyper-V virtual machine name: ")
    folder_to_scan = r"C:\Path\to\Hyper-V\Virtual\Machines\%s" % vm_name
else:
    print("Invalid hard drive choice.")
    exit()

# Choose the Windows version
windows_version = get_user_choice("Select the Windows version:",
                                 ["Windows XP", "Windows 7", "Windows 10"])

# Perform the scanning and replacement
if replace_missing_files == "Yes":
    scan_folder(folder_to_scan)

if replace_modified_files == "Yes":
    registry_key_to_scan = winreg.HKEY_LOCAL_MACHINE
    registry_subkey_to_scan = r"Software\Microsoft\Windows\CurrentVersion"
    scan_registry(registry_key_to_scan, registry_subkey_to_scan)

# Inform the user about completion
print("File scanning and replacement completed.")
