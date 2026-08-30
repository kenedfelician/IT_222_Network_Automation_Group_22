from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# Start all four devices in GNS3 before running this script.
# Assignment 22 - Data Processing Office (DataEntry VLAN 38, Systems VLAN 48)
# Only R1 and R2 are used as test sources because SW1/SW2 have no
# management SVI/IP address configured in this scenario.
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
]


# Scenario-based end-to-end tests. These prove that DataEntry
# personnel and Systems administrators can communicate between
# Site A and Site B, which is the operational requirement of the
# Data Processing Office scenario.
testing_commands = [
    [
        "R1",
        # R1 -> R2 routed link
        "ping 10.22.22.2",
        # R1 -> Site B DataEntry gateway (proves OSPF-learned DataEntry reachability)
        "ping 192.168.138.1",
        # R1 -> Site B Systems gateway (proves OSPF-learned Systems reachability)
        "ping 192.168.148.1",
        # Confirm the path to Site B follows the R1-R2 routed link
        "traceroute 192.168.138.1",
    ],
    [
        "R2",
        # R2 -> R1 routed link
        "ping 10.22.22.1",
        # R2 -> Site A DataEntry gateway
        "ping 192.168.38.1",
        # R2 -> Site A Systems gateway
        "ping 192.168.48.1",
        # Confirm the path to Site A follows the R2-R1 routed link
        "traceroute 192.168.38.1",
    ],
]


for device in devices:

    connection = None

    device_name = device["name"]

    connection_details = {
        key: value
        for key, value in device.items()
        if key != "name"
    }

    commands_for_device = []
    for command_group in testing_commands:
        if command_group[0] == device_name:
            commands_for_device = command_group[1:]
            break

    if not commands_for_device:
        print(f"\n{device_name}: No network tests have been assigned.")
        continue

    try:
        print(f"\nConnecting to {device_name}...")
        connection = ConnectHandler(**connection_details)

        if connection_details["secret"]:
            connection.enable()

        for command in commands_for_device:

            print(f"\n--- {device_name}: Testing {command} ---")

            output = connection.send_command(
                command,
                read_timeout=30,
            )

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


print("\nNetwork testing completed.")
