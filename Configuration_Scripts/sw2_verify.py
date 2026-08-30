from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# Start the switch in GNS3 before running this script.
# Connection details for SW2 (Site B switch) - Assignment 22
switch = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.15.128",     # GNS3 VM/server IP address
    "username": "admin22",       # set by *_config.py
    "password": "Admin@2226",    # set by *_config.py
    "secret": "Enable@2226",     # set by *_config.py
    "port": 5022,                  # SW2 GNS3 TELNET console port (verify in GNS3 Topology Summary)
}


# Verification commands: confirm VLAN 38 (DataEntry) and VLAN 48
# (Systems) exist, the access ports are assigned correctly, and
# the trunk toward R2 is carrying both VLANs.
verification_commands = [
    "show vlan brief",
    "show interfaces status",
    "show interfaces trunk",
    "show mac address-table",
]


connection = None

try:
    connection = ConnectHandler(**switch)

    if switch["secret"]:
        connection.enable()

    for command in verification_commands:
        print(f"\n--- {command} ---")

        output = connection.send_command(command)

        print(output)

    print("\nSwitch verification completed.")


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
    if connection is not None:
        connection.disconnect()
