from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# Start all network devices in GNS3 before running this script.
# Enter the connection details for devices from which the
# end-to-end network tests will be performed.
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

    # Add another test-source device when required.
]


# Enter destination IP addresses from the current network topology.
# These should test communication beyond the local device.
testing_commands = [
    "ping <DESTINATION_IP>",

    # Add other end-to-end tests when required.
    # "ping <REMOTE_NETWORK_DEVICE_IP>",
    # "traceroute <DESTINATION_IP>",
]


for device in devices:

    connection = None

    device_name = device["name"]

    connection_details = {
        key: value for key, value in device.items()
        if key != "name"
    }

    try:
        # Connect to the device from which the tests will originate.
        print(f"\nConnecting to {device_name}...")
        connection = ConnectHandler(**connection_details)

        # Enter privileged EXEC mode if required.
        if connection_details["secret"]:
            connection.enable()

        # Perform each end-to-end network test.
        for command in testing_commands:

            print(f"\n--- {device_name}: Testing {command} ---")

            output = connection.send_command(
                command,
                read_timeout=30
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
        # Close the connection to the current test-source device.
        if connection is not None:
            connection.disconnect()


print("\nNetwork testing completed.")