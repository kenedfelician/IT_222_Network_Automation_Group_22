from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# Start the switch in GNS3 before running this script.
# Enter the connection details of the switch to be configured.
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


# Enter the Cisco IOS commands required to configure the switch
# according to the provided network topology.
commands = [

    # Enter the required switch hostname.
    "hostname <SWITCH_NAME>",

    # Create the required VLAN.
    "vlan <VLAN_ID>",
    "name <VLAN_NAME>",

    # Configure the required access port.
    "interface <ACCESS_PORT>",
    "switchport mode access",
    "switchport access vlan <VLAN_ID>",
    "no shutdown",

    # Configure a trunk port when required.
    # "interface <TRUNK_PORT>",
    # "switchport mode trunk",
    # "no shutdown",

    # Configure a management SVI when required.
    # "interface vlan <MANAGEMENT_VLAN_ID>",
    # "ip address <MANAGEMENT_IP> <SUBNET_MASK>",
    # "no shutdown",

    # Configure the default gateway for switch management.
    # "ip default-gateway <DEFAULT_GATEWAY>",
]


connection = None

try:
    # Connect to the switch through its GNS3 TELNET console.
    connection = ConnectHandler(**switch)

    # Enter privileged EXEC mode if an enable password is configured.
    if switch["secret"]:
        connection.enable()

    # Send the switch configuration commands.
    output = connection.send_config_set(commands)
    print(output)

    # Save the completed configuration.
    connection.save_config()

    print("\nSwitch configuration completed successfully.")


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