from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# Start the switch in GNS3 before running this script.
# Enter the connection details of the switch to be verified.
# Use the current GNS3 VM/server IP address and the TELNET
# console port assigned to that switch.
switch = {
    "device_type": "cisco_ios_telnet",
    "host": "<GNS3_VM_IP>",
    "username": "",
    "password": "",
    "secret": "",
    "port": <TELNET_PORT>,
}


# Enter the Cisco IOS show commands required to verify
# the switch configuration.
verification_commands = [
    "show vlan brief",
    "show interfaces status",
    "show interfaces trunk",
    "show ip interface brief",

    # Add other verification commands required by the exercise.
    # "show running-config",
    # "show mac address-table",
]


connection = None

try:
    # Connect to the switch through its GNS3 TELNET console.
    connection = ConnectHandler(**switch)

    # Enter privileged EXEC mode if an enable password is configured.
    if switch["secret"]:
        connection.enable()

    # Run each verification command and display the output.
    for command in verification_commands:
        print(f"\n--- {command} ---")

        output = connection.send_command(command)

        print(output)

    print("\nSwitch verification completed.")


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
    # Close the TELNET connection if it was opened successfully.
    if connection is not None:
        connection.disconnect()