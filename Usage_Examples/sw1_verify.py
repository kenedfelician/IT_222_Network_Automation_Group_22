from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# Start SW1 in GNS3 before running this script.
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


# Enter the show commands required to verify SW1.
verification_commands = [
    "show vlan brief",
    "show interfaces status",
    "show ip interface brief",

    # Include this when trunk links are configured.
    # "show interfaces trunk",

    # Include this when required by the exercise.
    # "show running-config",
]


connection = None

try:
    # Connect to SW1 through its GNS3 TELNET console.
    connection = ConnectHandler(**switch)

    # Enter privileged EXEC mode if required.
    if switch["secret"]:
        connection.enable()

    # Run each verification command.
    for command in verification_commands:
        print(f"\n--- {command} ---")

        output = connection.send_command(command)

        print(output)

    print("\nSW1 verification completed.")


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