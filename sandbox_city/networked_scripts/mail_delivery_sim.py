import time
import random

def simulate_mail_delivery(sender, recipient, message):
    """Simulates a secure mail delivery process."""
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