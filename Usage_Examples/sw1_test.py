from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# Enter the GNS3 VM/server IP address and the TELNET
# console port assigned to SW1.
switch = {
    "device_type": "cisco_ios_telnet",
    "host": "<GNS3_VM_IP>",
    "username": "",
    "password": "",
    "secret": "",
    "port": <TELNET_PORT>,
}

# Start SW1 in GNS3 before running this script.
# Enter the tests required for SW1.
testing_commands = [

    # Check whether SW1 has learned MAC addresses.
    "show mac address-table",

    # Test connectivity from the SW1 management interface.
    # Replace with an IP address from the provided network.
    "ping <DESTINATION_IP>",

    # A common test is to ping the management default gateway.
    # "ping <DEFAULT_GATEWAY>",
]


connection = None

try:
    # Connect to SW1 through its GNS3 TELNET console.
    connection = ConnectHandler(**switch)

    # Enter privileged EXEC mode if required.
    if switch["secret"]:
        connection.enable()

    # Run each network test.
    for command in testing_commands:
        print(f"\n--- Testing: {command} ---")

        output = connection.send_command(
            command,
            read_timeout=30
        )

        print(output)

    print("\nSW1 network testing completed.")


except NetmikoTimeoutException:
    print(
        "Connection timed out. Check the GNS3 VM IP address, "
        "SW1 TELNET console port, GNS3 VM, and switch state."
    )


except NetmikoAuthenticationException:
    print(
        "Authentication failed. Check the username, password, "
        "and enable password."
    )


except Exception as error:
    print(f"Unexpected error: {error}")


finally:
    # Close the TELNET session.
    if connection is not None:
        connection.disconnect()