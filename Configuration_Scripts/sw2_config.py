from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# Start the switch in GNS3 before running this script.
# Connection details for SW2 (Site B switch) - Assignment 22: Data Processing Office
switch = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.15.128",     # GNS3 VM/server IP address
    "username": "admin22",        # Already configured on SW2 from an earlier run.
    "password": "Admin@2026",     # Leave these three BLANK only on a brand-new
    "secret": "Enable@2226",      # device with no login yet.
    "port": 5022,                 # SW2 GNS3 TELNET console port (verify in GNS3 Topology Summary)
    "fast_cli": False,            # slower, more careful read/write timing -
                                   # needed because this GNS3 host is under
                                   # heavy load, which was causing garbled/
                                   # partial reads and prompt-detection errors
    "global_delay_factor": 4,     # multiplies Netmiko's internal wait times
                                   # to match a slow console (raised from 2)
    "read_timeout_override": 60,  # forces ALL reads - including Netmiko's own
                                   # startup steps like "terminal width 511" -
                                   # to use this timeout, not just the ones we
                                   # set explicitly on send_config_set below
}


# SW2 separates DataEntry (VLAN 38) and Systems (VLAN 48) traffic at Site B,
# carries both VLANs to R2 over an 802.1Q trunk, and connects the DataEntry
# and Systems PCs (two per VLAN) on dedicated access ports.
commands = [

    # Enter the required switch hostname.
    "hostname SW2",

    # --- Local login username + enable secret (fixes "no password
    #     configured" issue). Same credentials are already filled
    #     into sw2_verify.py, sw2_test.py, network_verify.py and
    #     network_test.py so they keep working after this runs. ---
    "username admin22 privilege 15 secret Admin@2226",
    "enable secret Enable@2226",
    "service password-encryption",
    "line console 0",
    "login local",
    "exec-timeout 30 0",
    "logging synchronous",
    "exit",
    "line vty 0 4",
    "login local",
    "transport input telnet",
    "exit",

    # Create the DataEntry VLAN.
    "vlan 38",
    "name DataEntry",

    # Create the Systems VLAN.
    "vlan 48",
    "name Systems",
    "exit",

    # Configure the trunk port toward R2 (carries VLAN 38 and 48).
    # NOTE: This switch node is a 16-port IOSvL2 image, so its ports
    # are GigabitEthernet (Gi0/0-Gi3/3), not FastEthernet - the
    # original FastEthernet0/1-0/5 lines did not exist on this
    # device, which is why the config was failing. Per this switch's
    # own GNS3 console banner, Gi1/0 is the link toward R2 (landing
    # on R2's Gi0/1).
    # Some switch platforms (e.g. Catalyst 2950) do not support the
    # "switchport trunk encapsulation" command because they only
    # support 802.1Q. If this line causes an error on your switch,
    # simply delete/comment it out and re-run the script.
    "interface GigabitEthernet1/0",
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk allowed vlan 38,48",
    "no shutdown",

    # Configure the access port for DataEntry-PC2 (VLAN 38).
    "interface GigabitEthernet0/0",
    "switchport mode access",
    "switchport access vlan 38",
    "no shutdown",

    # Configure the access port for Systems-PC2 (VLAN 48).
    "interface GigabitEthernet0/1",
    "switchport mode access",
    "switchport access vlan 48",
    "no shutdown",

    # Configure the access port for DataEntry-PC3 (VLAN 38).
    "interface GigabitEthernet0/2",
    "switchport mode access",
    "switchport access vlan 38",
    "no shutdown",

    # Configure the access port for Systems-PC4 (VLAN 48).
    "interface GigabitEthernet0/3",
    "switchport mode access",
    "switchport access vlan 48",
    "no shutdown",
]


connection = None

try:
    # Connect to the switch through its GNS3 TELNET console.
    connection = ConnectHandler(**switch)

    # Enter privileged EXEC mode if an enable password is configured.
    if switch["secret"]:
        connection.enable()

    # Send the switch configuration commands.
    # cmd_verify=False skips per-line echo verification (which was
    # failing on R1/R2 due to a slow/laggy console) and just waits
    # for the whole block to finish. read_timeout=60 gives it room.
    output = connection.send_config_set(commands, read_timeout=60, cmd_verify=False)
    print(output)

    # Save the completed configuration.
    connection.save_config()

    print("\nSwitch configuration completed successfully.")


except NetmikoTimeoutException:
    print(
        "Connection timed out. Check the GNS3 VM IP address, "
        "TELNET console port, GNS3 VM, and switch state."
    )


except NetmikoAuthenticationException:
    print(
        "Authentication failed. Check the username, password, "
        "and enable password."
    )


except Exception as error:
    print(f"Unexpected error: {error}")


finally:
    # Close the TELNET connection if it was opened successfully.
    if connection is not None:
        connection.disconnect()