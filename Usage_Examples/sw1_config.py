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


# Enter the Cisco IOS commands required to configure SW1
# according to the provided network.
commands = [
    "hostname SW1",

    # Create VLAN 10 and assign a name.
    "vlan 10",
    "name SALES",

    # Configure the required access port for VLAN 10.
    "interface GigabitEthernet0/1",
    "switchport mode access",
    "switchport access vlan 10",
    "no shutdown",

    # Configure the management interface for SW1.
    # Replace the IP address and subnet mask with those
    # provided in the network.
    "interface vlan 10",
    "ip address <SW1_MANAGEMENT_IP> <SUBNET_MASK>",
    "no shutdown",

    # Configure the management default gateway.
    # Replace with the gateway provided in the network.
    "ip default-gateway <DEFAULT_GATEWAY>",
]


connection = None

try:
    # Connect to SW1 through its GNS3 TELNET console.
    connection = ConnectHandler(**switch)

    # Enter privileged EXEC mode if an enable password is configured.
    if switch["secret"]:
        connection.enable()

    # Send the configuration commands to SW1.
    output = connection.send_config_set(commands)
    print(output)

    # Save the SW1 configuration.
    connection.save_config()

    print("\nSW1 configuration completed successfully.")


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