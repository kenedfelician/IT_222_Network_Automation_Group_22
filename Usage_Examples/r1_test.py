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


# Enter the network tests to be performed from R1.
testing_commands = [

    # Replace <DESTINATION_IP> with a reachable IP address
    # in the network connected through Cloud1.
    "ping 192.168.46.130",

    # Add other tests when required.
    # "traceroute <DESTINATION_IP>",
]


connection = None

try:
    # Connect to R1 through the GNS3 TELNET console.
    connection = ConnectHandler(**router)

    # Enter privileged EXEC mode if an enable password is configured.
    if router["secret"]:
        connection.enable()

    # Run each network test and display the result.
    for command in testing_commands:
        print(f"\n--- Testing: {command} ---")

        output = connection.send_command(
            command,
            read_timeout=30
        )

        print(output)

    print("\nR1 network testing completed.")


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