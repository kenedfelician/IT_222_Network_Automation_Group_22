from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# Usage example: verify one router and one switch at network level.
# Replace the IP address and TELNET ports if the GNS3 environment differs.
devices = [
    {
        "name": "R1",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.46.128",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5000,
    },
    {
        "name": "SW1",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.46.128",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5001,
    },
]


# Each inner list begins with the device name, followed by the commands
# appropriate for that device. This prevents router-only commands from
# being sent to the switch and switch-only commands from being sent to R1.
verification_commands = [
    [
        "R1",
        "show ip interface brief",
        "show ip route",
        "show ip protocols",
    ],
    [
        "SW1",
        "show vlan brief",
        "show interfaces trunk",
        "show interfaces status",
        "show mac address-table",
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
