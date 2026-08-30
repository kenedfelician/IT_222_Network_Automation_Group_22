from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# Connection details for R1 (Site A router) - Assignment 22: Data Processing Office
router = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.15.128",     # GNS3 VM/server IP address
    "username": "admin22",               # Leave blank for the FIRST run (device has
    "password": "Admin@2226",               # no login yet). This script itself creates
    "secret": "Enable@2226",                 # username admin22 / Admin@2226 / Enable@2226
                                   # below. If you run this script again AFTER
                                   # that (e.g. to re-apply config), fill these
                                   # three fields in with those same values first.
    "port": 5005,                 # R1 GNS3 TELNET console port
}

# Start the router in GNS3 before running this script.
# R1 provides router-on-a-stick inter-VLAN routing for Site A
# (VLAN 38 = DataEntry, VLAN 48 = Systems) and the routed OSPF
# link to R2 (Site B).
commands = [
    "hostname R1",

    # --- Local login username + enable secret (fixes "no password
    #     configured" issue). These same credentials are already
    #     filled into r1_verify.py, r1_test.py, network_verify.py
    #     and network_test.py so they keep working after this runs. ---
    "username admin22 privilege 15 secret Admin@2226",
    "enable secret Enable@2226",
    "service password-encryption",
    "line console 0",
    "login local",
    "exec-timeout 30 0",
    "logging synchronous",
    "exit",
    "line vty 0 4",
    "login local",
    "transport input telnet",
    "exit",

    # --- Trunk parent interface (connects to SW1 Gi0/1) ---
    "interface GigabitEthernet0/0",
    "no shutdown",

    # --- Subinterface for VLAN 38 - DataEntry (Site A) ---
    "interface GigabitEthernet0/0.38",
    "encapsulation dot1Q 38",
    "ip address 192.168.38.1 255.255.255.0",

    # --- Subinterface for VLAN 48 - Systems (Site A) ---
    "interface GigabitEthernet0/0.48",
    "encapsulation dot1Q 48",
    "ip address 192.168.48.1 255.255.255.0",

    # --- Routed point-to-point link to R2 ---
    "interface GigabitEthernet0/1",
    "ip address 10.22.22.1 255.255.255.252",
    "no shutdown",

    # --- OSPF Process 1, Area 0 ---
    "router ospf 1",
    "network 192.168.38.0 0.0.0.255 area 0",
    "network 192.168.48.0 0.0.0.255 area 0",
    "network 10.22.22.0 0.0.0.3 area 0",
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

    # Verify that the required network configuration was applied correctly.
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