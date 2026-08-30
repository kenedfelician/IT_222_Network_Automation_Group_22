from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# Start the required devices in GNS3 before running this script.
# Use only devices that are suitable sources for the required tests.
# Replace the host address and TELNET console ports with current GNS3 values.
devices = [
    {
        "name": "R1",
        "device_type": "cisco_ios_telnet",
        "host": "<GNS3_VM_IP>",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5000,  # Replace with the current R1 TELNET console port.
    },
    {
        "name": "SW1",
        "device_type": "cisco_ios_telnet",
        "host": "<GNS3_VM_IP>",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5001,  # Replace with the current SW1 TELNET console port.
    },
]


# Use a list of lists so that tests can be assigned to specific devices.
# The first item in each inner list is the source device. The remaining
# items are scenario-specific tests to run from that device.
#
# A Layer-2 switch can originate IP tests only when it has a management
# SVI/IP configuration and a reachable gateway. Remove its test group when
# the assigned scenario does not configure switch management addressing.
testing_commands = [
    [
        "R1",
        "ping <R2_OR_REMOTE_DESTINATION_IP>",
        # Add other router-originated tests required by the scenario.
        # "ping <REMOTE_HOST_IP>",
        # "traceroute <REMOTE_HOST_IP>",
    ],
    [
        "SW1",
        "ping <SW1_DEFAULT_GATEWAY_IP>",
        # Add another switch-originated test only when appropriate.
        # "ping <REMOTE_MANAGEMENT_IP>",
    ],
]


# Connect to each selected source device and run only its assigned tests.
for device in devices:

    connection = None

    device_name = device["name"]

    # Remove the name field because Netmiko does not use it.
    connection_details = {
        key: value
        for key, value in device.items()
        if key != "name"
    }

    # Find the testing-command list for the current source device.
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

        # Enter privileged EXEC mode if an enable password is provided.
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
