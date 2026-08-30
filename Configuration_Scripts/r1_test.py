from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# Start the router in GNS3 before running this script.
# Connection details for R1 (Site A router) - Assignment 22
router = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.15.128",     # GNS3 VM/server IP address
    "username": "admin22",       # set by *_config.py
    "password": "Admin@2226",    # set by *_config.py
    "secret": "Enable@2226",     # set by *_config.py
    "port": 5005,                 # R1 GNS3 TELNET console port
}


# Network tests from R1: confirm the routed link to R2 is up,
# and that OSPF has learned the Site B (DataEntry/Systems)
# gateway networks, proving inter-site connectivity for the
# Data Processing Office scenario.
testing_commands = [

    # Test the directly connected routed link to R2.
    "ping 10.22.22.2",

    # Test reachability to Site B DataEntry gateway (learned via OSPF).
    "ping 192.168.138.1",

    # Test reachability to Site B Systems gateway (learned via OSPF).
    "ping 192.168.148.1",

    # Confirm the path taken to Site B follows the R1-R2 routed link.
    "traceroute 192.168.138.1",
]


connection = None


try:
    connection = ConnectHandler(**router)

    if router["secret"]:
        connection.enable()

    for command in testing_commands:
        print(f"\n--- Testing: {command} ---")
        output = connection.send_command(
            command,
            read_timeout=30
        )
        print(output)

    print("\nNetwork testing completed.")


except NetmikoTimeoutException:
    print(
        "Connection timed out. Check the GNS3 VM IP address, "
        "TELNET console port, GNS3 VM, and router state."
    )


except NetmikoAuthenticationException:
    print(
        "Authentication failed. Check the username, password, "
        "and enable password."
    )


except Exception as error:
    print(f"Unexpected error: {error}")


finally:
    if connection is not None:
        connection.disconnect()
