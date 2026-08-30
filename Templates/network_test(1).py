from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# Usage example: perform network-level tests from one router and one switch.
# Replace the IP address, TELNET ports, and test destinations to match the
# current GNS3 topology. The switch tests assume that SW1 has a management
# SVI/IP address and a configured default gateway.
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


# Each inner list identifies the source device followed by the tests that
# are meaningful from that device. Students should replace these examples
# with tests derived from their assigned scenario.
testing_commands = [
    [
        "R1",
        "ping 10.1.1.2",
        "ping 192.168.30.10",
        "traceroute 192.168.30.10",
    ],
    [
        "SW1",
        "ping 192.168.10.1",
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
