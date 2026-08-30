from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# Enter the connection details of the router you want to configure.
# Use the current GNS3 VM/server IP address and the TELNET console
# port assigned to that router in GNS3.
router = {
    "device_type": "cisco_ios_telnet",
    "host": "<GNS3_VM_IP>",       # Replace with the current GNS3 VM/server IP address
    "username": "",               # Enter username only if required
    "password": "",               # Enter password only if required
    "secret": "",                 # Enter enable password only if required
    "port": <TELNET_PORT>,        # Replace with this router's GNS3 TELNET console port
}

# Start the router in GNS3 before running this script.
# Enter the Cisco IOS commands required to configure the router
# according to the provided network topology and addressing information.
commands = [
    "hostname <ROUTER_NAME>",

    "interface <INTERFACE_NAME>",             # Replace with the required router interface
    "ip address <IP_ADDRESS> <SUBNET_MASK>",  # Replace with the assigned IP address and mask
    "no shutdown",

    # Add other commands required by the provided network

    # "ip route <DESTINATION_NETWORK> <SUBNET_MASK> <NEXT_HOP_IP>",

    # "router ospf <PROCESS_ID>",
    # "network <NETWORK_ADDRESS> <WILDCARD_MASK> area <AREA_ID>",
]


# Create a variable that will store the router connection after
# Netmiko successfully connects to the device.
connection = None


try:
    # Establish a TELNET console connection to the router using
    # the GNS3 VM/server IP address and console port entered above.
    connection = ConnectHandler(**router)


    # Enter privileged EXEC mode if an enable password was supplied.
    if router["secret"]:
        connection.enable()


    # Send all Cisco IOS configuration commands listed in commands.
    output = connection.send_config_set(commands)
    print(output)


    # Enter the show command that should be used to verify
    # that the required network configuration was applied correctly.
    verification = connection.send_command(
        "show ip interface brief"
    )

    print("\n--- Verification ---")
    print(verification)


    # Save the completed router configuration.
    connection.save_config()

    print("\nConfiguration completed successfully.")


# Handle cases where Netmiko cannot reach the GNS3 console.
except NetmikoTimeoutException:
    print(
        "Connection timed out. Check the GNS3 VM IP address, "
        "TELNET console port, GNS3 VM, and router state."
    )


# Handle cases where the supplied login or enable credentials are incorrect.
except NetmikoAuthenticationException:
    print(
        "Authentication failed. Check the username, password, "
        "and enable password."
    )


# Display any other error that occurs while running the program.
except Exception as error:
    print(f"Unexpected error: {error}")


finally:
    # Close the TELNET session if a connection was successfully opened.
    if connection is not None:
        connection.disconnect()