from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# Start R1 in GNS3 before running this script.
# Enter the connection details for R1.
# Use the current GNS3 VM/server IP address and R1 TELNET console port.
router = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.46.128",
    "username": "",
    "password": "",
    "secret": "",
    "port": 5000,
}


# Enter the Cisco IOS show commands required to verify R1.
verification_commands = [
    "show ip interface brief",
    "show ip route",
]


connection = None

try:
    # Connect to R1 through the GNS3 TELNET console.
    connection = ConnectHandler(**router)

    # Enter privileged EXEC mode if an enable password is configured.
    if router["secret"]:
        connection.enable()

    # Run each verification command and display the output.
    for command in verification_commands:
        print(f"\n--- {command} ---")

        output = connection.send_command(command)

        print(output)

    print("\nR1 verification completed.")


except NetmikoTimeoutException:
    print(
        "Connection timed out. Check the GNS3 VM IP address, "
        "R1 TELNET console port, GNS3 VM, and router state."
    )


except NetmikoAuthenticationException:
    print(
        "Authentication failed. Check the username, password, "
        "and enable password."
    )


except Exception as error:
    print(f"Unexpected error: {error}")


finally:
    # Close the TELNET session if a connection was opened.
    if connection is not None:
        connection.disconnect()