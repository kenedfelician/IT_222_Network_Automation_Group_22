from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# Start all four devices in GNS3 before running this script.
# Assignment 22 - Data Processing Office (DataEntry VLAN 38, Systems VLAN 48)
devices = [
    {
        "name": "R1",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.15.128",
        "username": "admin22",       # set by r1/r2/sw1/sw2 _config.py
        "password": "Admin@2226",    # set by r1/r2/sw1/sw2 _config.py
        "secret": "Enable@2226",     # set by r1/r2/sw1/sw2 _config.py
        "port": 5005,   # R1 GNS3 TELNET console port
    },
    {
        "name": "R2",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.15.128",
        "username": "admin22",       # set by r1/r2/sw1/sw2 _config.py
        "password": "Admin@2226",    # set by r1/r2/sw1/sw2 _config.py
        "secret": "Enable@2226",     # set by r1/r2/sw1/sw2 _config.py
        "port": 5007,   # R2 GNS3 TELNET console port
    },
    {
        "name": "SW1",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.15.128",
        "username": "admin22",       # set by r1/r2/sw1/sw2 _config.py
        "password": "Admin@2226",    # set by r1/r2/sw1/sw2 _config.py
        "secret": "Enable@2226",     # set by r1/r2/sw1/sw2 _config.py
        "port": 5019,   # SW1 GNS3 TELNET console port (verify in GNS3 Topology Summary)
    },
    {
        "name": "SW2",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.15.128",
        "username": "admin22",       # set by r1/r2/sw1/sw2 _config.py
        "password": "Admin@2026",    # set by r1/r2/sw1/sw2 _config.py
        "secret": "Enable@2226",     # set by r1/r2/sw1/sw2 _config.py
        "port": 5022,   # SW2 GNS3 TELNET console port (verify in GNS3 Topology Summary)
    },
]


# Verification commands per device. Together, these prove that the
# complete Data Processing Office network has been correctly
# integrated: VLANs exist, trunks carry both VLANs, router
# subinterfaces are operational, and OSPF has formed neighbours
# and learned routes between Site A and Site B.
verification_commands = [
    [
        "R1",
        "show ip interface brief",
        "show ip route",
        "show ip protocols",
        "show ip ospf neighbor",
    ],
    [
        "R2",
        "show ip interface brief",
        "show ip route",
        "show ip protocols",
        "show ip ospf neighbor",
    ],
    [
        "SW1",
        "show vlan brief",
        "show interfaces trunk",
        "show interfaces status",
    ],
    [
        "SW2",
        "show vlan brief",
        "show interfaces trunk",
        "show interfaces status",
    ],
]


for device in devices:

    connection = None

    device_name = device["name"]

    # Remove the name field because Netmiko does not use it.
    connection_details = {
        key: value
        for key, value in device.items()
        if key != "name"
    }

    # Find the verification-command list for the current device.
    commands_for_device = []
    for command_group in verification_commands:
        if command_group[0] == device_name:
            commands_for_device = command_group[1:]
            break

    if not commands_for_device:
        print(f"\n{device_name}: No verification commands have been assigned.")
        continue

    try:
        print(f"\nConnecting to {device_name}...")
        connection = ConnectHandler(**connection_details)

        if connection_details["secret"]:
            connection.enable()

        for command in commands_for_device:

            print(f"\n--- {device_name}: {command} ---")

            output = connection.send_command(command)

            print(output)

    except NetmikoTimeoutException:
        print(
            f"{device_name}: Connection timed out. Check the GNS3 VM IP address, "
            "TELNET console port, GNS3 VM, and device state."
        )

    except NetmikoAuthenticationException:
        print(
            f"{device_name}: Authentication failed. Check the username, "
            "password, and enable password."
        )

    except Exception as error:
        print(f"{device_name}: Unexpected error: {error}")

    finally:
        if connection is not None:
            connection.disconnect()


print("\nNetwork verification completed.")
