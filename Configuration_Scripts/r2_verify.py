from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# Start the router in GNS3 before running this script.
# Connection details for R2 (Site B router) - Assignment 22
router = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.15.128",     # GNS3 VM/server IP address
    "username": "admin22",        # set by *_config.py
    "password": "Admin@2226",     # set by *_config.py
    "secret": "Enable@2226",      # set by *_config.py
    "port": 5007,                 # R2 GNS3 TELNET console port
    "fast_cli": False,            # slower, more careful read/write timing -
                                   # needed because this GNS3 host is under
                                   # heavy load, which was causing garbled/
                                   # partial reads and prompt-detection errors
    "global_delay_factor": 2,     # doubles Netmiko's internal wait times
                                   # between sends to match a slow console
}


# Verification commands: confirm subinterfaces, VLAN routing,
# OSPF neighbour formation, and learned routes for the
# Data Processing Office (Site B) network.
# NOTE: "show interfaces trunk" was removed - it's a switch
# command and always returns "% Invalid input detected" on a
# router. The subinterfaces (Gi0/1.38, Gi0/1.48) are already
# verified by "show ip interface brief" below.
verification_commands = [
    "show ip interface brief",     # Verify Gi0/1.38, Gi0/1.48, Gi0/0 states & addresses
    "show running-config",         # Verify the applied router configuration
    "show ip route",               # Verify local + learned OSPF routes (Site A networks)
    "show ip protocols",           # Verify OSPF process 1 is running
    "show ip ospf neighbor",       # Verify OSPF neighbour adjacency with R1
]


connection = None


try:
    connection = ConnectHandler(**router)

    if router["secret"]:
        connection.enable()

    for command in verification_commands:
        print(f"\n--- {command} ---")
        # expect_string pins the exact prompt to wait for, instead of
        # Netmiko guessing from possibly partial/garbled buffered output.
        # read_timeout=120 gives long outputs (like show running-config)
        # plenty of time to finish before giving up.
        output = connection.send_command(
            command, expect_string=r"R2#", read_timeout=120
        )
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