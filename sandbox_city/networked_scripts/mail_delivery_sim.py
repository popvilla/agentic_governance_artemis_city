import time
import random

def simulate_mail_delivery(sender, recipient, message):
    """Simulates a secure mail delivery process within Sandbox City.

    This function models a mail delivery from a sender to a recipient,
    introducing a variable network delay to simulate transfer time. It also
    incorporates a random chance of failure to represent potential network
    issues or security compromises. The outcome of the simulation is printed
    to the console.

    Args:
        sender (str): The identifier for the agent or user sending the message.
        recipient (str): The identifier for the agent or user receiving the
                         message.
        message (str): The content of the message being sent.

    Returns:
        bool: True if the message is delivered successfully, False if the
              delivery fails.
    """
    print(f"\n--- Mail Delivery Simulation ---")
    print(f"Sender: {sender}, Recipient: {recipient}")
    print(f"Message: '{message}'")
    print("Pack Rat is initiating secure transfer...")
    time.sleep(random.uniform(0.5, 1.5))

    if random.random() < 0.1: # 10% chance of failure
        print("Transfer failed: Data integrity compromised or recipient unreachable.")
        return False
    else:
        print("Transfer successful: Message delivered securely.")
        return True

if __name__ == "__main__":
    print("Running Mail Delivery Simulation (Sandbox City - Post Office)")
    simulate_mail_delivery("Agent_A", "Agent_B", "Urgent operational update.")
    simulate_mail_delivery("Human_User", "Artemis", "Query about recent policy change.")