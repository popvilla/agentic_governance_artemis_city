"""Secure mail delivery simulation for Sandbox City.

This module provides a simulation of the Pack Rat postal system,
demonstrating secure message transfer between agents within the
Artemis City sandbox environment. It includes realistic timing
delays and occasional transfer failures to simulate real-world
conditions.

The simulation is used for testing and demonstrating the postal
system before integration with the actual memory layer.
"""

import random
import time


def simulate_mail_delivery(sender, recipient, message):
    """Simulate a secure mail delivery process within Sandbox City.

    Demonstrates the Pack Rat secure transfer protocol with realistic
    timing and a small failure rate to test error handling.

    Args:
        sender: Name of the sending agent or user.
        recipient: Name of the receiving agent or user.
        message: Content of the message being delivered.

    Returns:
        bool: True if delivery was successful, False if transfer failed
            due to data integrity issues or unreachable recipient.
    """
    print("\n--- Mail Delivery Simulation ---")
    print(f"Sender: {sender}, Recipient: {recipient}")
    print(f"Message: '{message}'")
    print("Pack Rat is initiating secure transfer...")
    time.sleep(random.uniform(0.5, 1.5))

    if random.random() < 0.1:  # 10% chance of failure
        print("Transfer failed: Data integrity compromised or recipient unreachable.")
        return False
    else:
        print("Transfer successful: Message delivered securely.")
        return True


if __name__ == "__main__":
    print("Running Mail Delivery Simulation (Sandbox City - Post Office)")
    simulate_mail_delivery("Agent_A", "Agent_B", "Urgent operational update.")
    simulate_mail_delivery("Human_User", "Artemis", "Query about recent policy change.")
