from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# Start the router in GNS3 before running this script.
# Enter the connection details of the router to be verified.
# Use the current GNS3 VM/server IP address and the TELNET
# console port assigned to that router.
router = {
    "device_type": "cisco_ios_telnet",
    "host": "<GNS3_VM_IP>",       # Replace with the current GNS3 VM/server IP address
    "username": "",               # Enter username only if required
    "password": "",               # Enter password only if required
    "secret": "",                 # Enter enable password only if required
    "port": <TELNET_PORT>,        # Replace with this router's GNS3 TELNET console port
}


# Enter the Cisco IOS show commands required to verify the
# configuration specified in the provided network exercise.
verification_commands = [
    "show ip interface brief",     # Verify interface IP addresses and interface states
    "show running-config",         # Verify the applied router configuration

    # Add other verification commands required by the exercise.

    # "show ip route",             # Verify routes in the routing table
    # "show ip protocols",         # Verify the configured routing protocol
    # "show access-lists",         # Verify configured ACLs
]


# Create a variable that will store the router connection.
connection = None


try:
    # Establish a TELNET console connection to the router.
    connection = ConnectHandler(**router)


    # Enter privileged EXEC mode if an enable password was supplied.
    if router["secret"]:
        connection.enable()


    # Run each verification command and display its output.
    for command in verification_commands:

        print(f"\n--- {command} ---")

        output = connection.send_command(command)

        print(output)


    print("\nVerification completed successfully.")


# Handle cases where Netmiko cannot reach the GNS3 console.
except NetmikoTimeoutException:
    print(
        "Connection timed out. Check the GNS3 VM IP address, "
        "TELNET console port, GNS3 VM, and router state."
    )


# Handle cases where the supplied credentials are incorrect.
except NetmikoAuthenticationException:
    print(
        "Authentication failed. Check the username, password, "
        "and enable password."
    )


# Display any other error that occurs during verification.
except Exception as error:
    print(f"Unexpected error: {error}")


finally:
    # Close the TELNET session if a connection was successfully opened.
    if connection is not None:
        connection.disconnect()