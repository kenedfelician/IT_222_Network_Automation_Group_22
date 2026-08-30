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


# SW2 has no management SVI/IP address configured (not required by
# this scenario), so it cannot originate ping tests itself. Instead,
# these tests confirm that DataEntry-PC1/PC2 and Systems-PC1/PC2
# (Site B) have been learned on the correct VLAN, proving VLAN
# segmentation is working correctly at Site B.
testing_commands = [

    # Confirm hosts connected on VLAN 38 (DataEntry) were learned.
    "show mac address-table vlan 38",

    # Confirm hosts connected on VLAN 48 (Systems) were learned.
    "show mac address-table vlan 48",

    # Confirm the access ports are up/up and in the correct VLAN.
    "show interfaces status",
]


connection = None

try:
    connection = ConnectHandler(**switch)

    if switch["secret"]:
        connection.enable()

    for command in testing_commands:
        print(f"\n--- Testing: {command} ---")

        output = connection.send_command(
            command,
            read_timeout=30
        )

        print(output)

    print("\nSwitch testing completed.")


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
