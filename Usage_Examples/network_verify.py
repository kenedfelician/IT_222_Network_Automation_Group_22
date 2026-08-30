from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# Start all network devices in GNS3 before running this script.
# Enter the current GNS3 VM/server IP address and the TELNET
# console port assigned to each device.
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

    # Add SW1 and other devices using their current console ports.
    # {
    #     "name": "SW1",
    #     "device_type": "cisco_ios_telnet",
    #     "host": "192.168.46.128",
    #     "username": "",
    #     "password": "",
    #     "secret": "",
    #     "port": <SW1_TELNET_PORT>,
    # },
]


# Enter the commands required to verify the network.
verification_commands = [
    "show ip interface brief",
    "show ip route",
]


for device in devices:

    connection = None

    device_name = device["name"]

    connection_details = {
        key: value for key, value in device.items()
        if key != "name"
    }

    try:
        # Connect to the current network device.
        print(f"\nConnecting to {device_name}...")
        connection = ConnectHandler(**connection_details)

        # Enter privileged EXEC mode if required.
        if connection_details["secret"]:
            connection.enable()

        # Collect verification information from the device.
        for command in verification_commands:

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
        # Close the connection to the current device.
        if connection is not None:
            connection.disconnect()


print("\nNetwork verification completed.")