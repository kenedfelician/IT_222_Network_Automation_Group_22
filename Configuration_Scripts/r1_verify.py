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


# Verification commands: confirm subinterfaces, VLAN routing,
# OSPF neighbour formation, and learned routes for the
# Data Processing Office (Site A) network.
# NOTE: "show interfaces trunk" was removed - it's a switch
# command and always returns "% Invalid input detected" on a
# router. The subinterfaces (Gi0/0.38, Gi0/0.48) are already
# verified by "show ip interface brief" below.
verification_commands = [
    "show ip interface brief",     # Verify Gi0/0.38, Gi0/0.48, Gi0/1 states & addresses
    "show running-config",         # Verify the applied router configuration
    "show ip route",               # Verify local + learned OSPF routes (Site B networks)
    "show ip protocols",           # Verify OSPF process 1 is running
    "show ip ospf neighbor",       # Verify OSPF neighbour adjacency with R2
]


connection = None


try:
    connection = ConnectHandler(**router)

    if router["secret"]:
        connection.enable()

    for command in verification_commands:
        print(f"\n--- {command} ---")
        # read_timeout=60 gives long outputs (like show running-config)
        # enough time to finish printing before Netmiko gives up waiting
        # for the "R1#" prompt to reappear.
        output = connection.send_command(command, read_timeout=60)
        print(output)

    print("\nVerification completed successfully.")


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