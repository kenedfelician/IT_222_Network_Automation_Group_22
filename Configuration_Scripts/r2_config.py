from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# Connection details for R2 (Site B router) - Assignment 22: Data Processing Office
router = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.15.128",     # GNS3 VM/server IP address
    "username": "admin22",               # Leave blank for the FIRST run (device has
    "password": "Admin@2226",               # no login yet). This script itself creates
    "secret": "Enable@2226",                 # username admin22 / Admin@2226 / Enable@2226
                                   # below. If you run this script again AFTER
                                   # that (e.g. to re-apply config), fill these
                                   # three fields in with those same values first.
    "port": 5007,                 # R2 GNS3 TELNET console port
}

# Start the router in GNS3 before running this script.
# R2 provides router-on-a-stick inter-VLAN routing for Site B
# (VLAN 38 = DataEntry, VLAN 48 = Systems) and the routed OSPF
# link to R1 (Site A).
commands = [
    "hostname R2",

    # --- Local login username + enable secret (fixes "no password
    #     configured" issue). These same credentials are already
    #     filled into r2_verify.py, r2_test.py, network_verify.py
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

    # --- Trunk parent interface (connects to SW2 Gi1/0) ---
    # NOTE: on this GNS3 topology R2's cabling is the mirror of R1:
    # the trunk to SW2 lands on Gi0/1 (confirmed from SW2's own
    # console banner: "Gi1/0 connected to R2 on port Gi0/1"), and
    # the routed link to R1 is on Gi0/0. This is swapped vs. R1,
    # where the trunk is on Gi0/0 and the R2 link is on Gi0/1 --
    # double-check this against your own topology before running.
    "interface GigabitEthernet0/1",
    "no shutdown",

    # --- Subinterface for VLAN 38 - DataEntry (Site B) ---
    "interface GigabitEthernet0/1.38",
    "encapsulation dot1Q 38",
    "ip address 192.168.138.1 255.255.255.0",

    # --- Subinterface for VLAN 48 - Systems (Site B) ---
    "interface GigabitEthernet0/1.48",
    "encapsulation dot1Q 48",
    "ip address 192.168.148.1 255.255.255.0",

    # --- Routed point-to-point link to R1 ---
    "interface GigabitEthernet0/0",
    "ip address 10.22.22.2 255.255.255.252",
    "no shutdown",

    # --- OSPF Process 1, Area 0 ---
    "router ospf 1",
    "network 192.168.138.0 0.0.0.255 area 0",
    "network 192.168.148.0 0.0.0.255 area 0",
    "network 10.22.22.0 0.0.0.3 area 0",
]


connection = None


try:
    connection = ConnectHandler(**router)

    if router["secret"]:
        connection.enable()

    output = connection.send_config_set(commands)
    print(output)

    verification = connection.send_command(
        "show ip interface brief"
    )

    print("\n--- Verification ---")
    print(verification)

    connection.save_config()

    print("\nConfiguration completed successfully.")


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