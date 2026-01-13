"""Artemis City Postal Service - Memory delivery system.

This module provides a postal-themed interface for memory operations,
treating the Obsidian vault as the City Archives and memory operations
as mail delivery between agents.
"""

import random
import time
from datetime import datetime
from typing import Dict, List, Optional

from .context_loader import ContextEntry, ContextLoader
from .memory_client import MCPResponse, MemoryClient
from .trust_interface import get_trust_interface


class MailPacket:
    """Represents a mail packet being delivered through the city.

    Attributes:
        sender: Agent sending the mail
        recipient: Target agent or vault location
        subject: Mail subject line
        content: Mail content
        priority: Delivery priority (urgent, normal, low)
        timestamp: When mail was created
        delivery_status: Current status
        tracking_id: Unique tracking identifier
    """

    def __init__(
        self, sender: str, recipient: str, subject: str, content: str, priority: str = "normal"
    ):
        """Initialize a mail packet."""
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.content = content
        self.priority = priority
        self.timestamp = datetime.now()
        self.delivery_status = "created"
        self.tracking_id = f"{sender[:3].upper()}-{int(time.time() * 1000) % 100000}"

    def __str__(self) -> str:
        """Return a string representation of the mail packet."""
        return (
            f"[Mail #{self.tracking_id}]\n"
            f"  From: {self.sender}\n"
            f"  To: {self.recipient}\n"
            f"  Subject: {self.subject}\n"
            f"  Priority: {self.priority}\n"
            f"  Status: {self.delivery_status}"
        )


class PostOffice:
    """Artemis City Post Office - Central mail routing hub.

    The Post Office handles all mail delivery between agents and the
    City Archives (Obsidian vault), maintaining postal records and
    ensuring secure delivery through Pack Rat protocols.
    """

    def __init__(self):
        """Initialize the Post Office."""
        self.memory_client = MemoryClient()
        self.trust_office = get_trust_interface()
        self.context_loader = ContextLoader(self.memory_client)
        self.delivery_log: List[Dict] = []

        print("\n Artemis City Post Office - OPEN")
        print("=" * 60)
        print("  Serving the citizens of Artemis City")
        print("  All mail handled by Pack Rat for secure delivery")
        print("  Archives maintained in the City Library")
        print("=" * 60)

    def send_mail(
        self, sender: str, recipient: str, subject: str, content: str, priority: str = "normal"
    ) -> MailPacket:
        """Send mail through the postal system.

        Args:
            sender: Agent sending the mail
            recipient: Target agent or vault location
            subject: Mail subject
            content: Mail content
            priority: Delivery priority

        Returns:
            MailPacket with delivery status
        """
        packet = MailPacket(sender, recipient, subject, content, priority)

        print("\n NEW MAIL at Post Office")
        print(f"   Tracking ID: {packet.tracking_id}")
        print(f"   From: {sender} → To: {recipient}")
        print(f"   Subject: {subject}")

        # Check sender clearance
        if not self.trust_office.can_perform_operation(sender, 'write'):
            packet.delivery_status = "rejected - insufficient clearance"
            print(f"    REJECTED: {sender} lacks postal clearance")
            self._log_delivery(packet, success=False, reason="No clearance")
            return packet

        # Simulate Pack Rat handling
        print("\n    Pack Rat is securing the mail...")
        time.sleep(random.uniform(0.3, 0.8))

        # Simulate potential delivery issues
        if random.random() < 0.05:  # 5% chance of delay
            print("     Temporary postal delay detected...")
            time.sleep(random.uniform(0.5, 1.0))

        # Deliver to City Archives
        vault_path = f"Postal/Agents/{recipient}/{packet.tracking_id}.md"

        # Create mail note
        mail_content = self._format_mail_note(packet)
        response = self.memory_client.append_context(vault_path, mail_content)

        if response.success:
            packet.delivery_status = "delivered"
            print("    DELIVERED to City Archives")
            print(f"   📍 Location: {vault_path}")

            # Update trust
            self.trust_office.record_success(sender)

            # Tag the mail
            self.memory_client.manage_tags(
                vault_path, 'add', [sender, recipient, 'postal-mail', priority]
            )
        else:
            packet.delivery_status = "failed"
            print(f"    DELIVERY FAILED: {response.error}")
            self.trust_office.record_failure(sender)

        self._log_delivery(packet, response.success)
        return packet

    def check_mailbox(self, agent_name: str, unread_only: bool = True) -> List[ContextEntry]:
        """Check an agent's mailbox in the City Archives.

        Args:
            agent_name: Agent whose mailbox to check
            unread_only: Whether to show only unread mail

        Returns:
            List of mail entries
        """
        print(f"\n📪 Checking mailbox for: {agent_name}")
        print(f"   Location: Postal/Agents/{agent_name}/")

        # Search for mail tagged with agent name
        mail = self.context_loader.search_context(f"#{agent_name} #postal-mail", limit=20)

        if mail:
            print(f"   📨 Found {len(mail)} mail item(s)")
            for i, item in enumerate(mail[:5], 1):
                print(f"      {i}. {item.path}")
        else:
            print("   📭 Mailbox is empty")

        return mail

    def send_to_archives(
        self, sender: str, archive_section: str, title: str, content: str
    ) -> MCPResponse:
        """Send a document to the City Archives for permanent storage.

        Args:
            sender: Agent filing the document
            archive_section: Section of archives (e.g., "Reflections", "Reports")
            title: Document title
            content: Document content

        Returns:
            MCPResponse with delivery status
        """
        print("\n  ARCHIVAL REQUEST")
        print(f"   From: {sender}")
        print(f"   Section: {archive_section}")
        print(f"   Title: {title}")

        # Check clearance
        if not self.trust_office.can_perform_operation(sender, 'write'):
            print("    DENIED: Insufficient archival clearance")
            return MCPResponse(
                success=False, error="Insufficient clearance for archival operations"
            )

        print("\n    Pack Rat is processing archival request...")
        time.sleep(random.uniform(0.4, 0.9))

        # Store in archives
        path = f"Archives/{archive_section}/{sender}_{title}.md"
        response = self.memory_client.store_agent_context(
            sender, content, folder=f"Archives/{archive_section}"
        )

        if response.success:
            print(f"    ARCHIVED at: {path}")
            print("    Available for future reference")
            self.trust_office.record_success(sender)
        else:
            print(f"    ARCHIVAL FAILED: {response.error}")
            self.trust_office.record_failure(sender)

        return response

    def request_from_archives(
        self, requester: str, query: str, section: Optional[str] = None
    ) -> List[ContextEntry]:
        """Request documents from the City Archives.

        Args:
            requester: Agent requesting documents
            query: Search query
            section: Optional specific archive section

        Returns:
            List of matching archive documents
        """
        print("\n📖 ARCHIVE REQUEST")
        print(f"   Requester: {requester}")
        print(f"   Query: '{query}'")
        if section:
            print(f"   Section: {section}")

        # Check read clearance
        if not self.trust_office.can_perform_operation(requester, 'read'):
            print("    DENIED: No archive access clearance")
            return []

        print("\n    City Librarian is searching...")
        time.sleep(random.uniform(0.5, 1.0))

        # Search archives
        search_query = query
        if section:
            search_query = f"#Archives #{section} {query}"

        results = self.context_loader.search_context(search_query, limit=10)

        if results:
            print(f"    Found {len(results)} document(s)")
            for i, doc in enumerate(results[:5], 1):
                print(f"      {i}. {doc.path}")
        else:
            print("   📭 No documents found matching query")

        self.trust_office.record_success(requester)
        return results

    def get_postal_report(self) -> Dict:
        """Generate a postal service activity report.

        Returns:
            Dictionary with postal statistics
        """
        print("\n POSTAL SERVICE REPORT")
        print(f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        total_deliveries = len(self.delivery_log)
        successful = sum(1 for d in self.delivery_log if d['success'])
        failed = total_deliveries - successful

        print(f"   Total Deliveries: {total_deliveries}")
        print(f"    Successful: {successful}")
        print(f"    Failed: {failed}")

        if total_deliveries > 0:
            success_rate = (successful / total_deliveries) * 100
            print(f"   📈 Success Rate: {success_rate:.1f}%")

        # Trust report
        print("\n     CITIZEN CLEARANCE STATUS")
        trust_report = self.trust_office.get_trust_report()
        for level, entities in trust_report['by_level'].items():
            if entities:
                print(f"   {level.upper()}: {len(entities)} citizen(s)")

        print("=" * 60)

        return {
            'total_deliveries': total_deliveries,
            'successful': successful,
            'failed': failed,
            'trust_report': trust_report,
        }

    def _format_mail_note(self, packet: MailPacket) -> str:
        """Format a mail packet as a markdown note.

        Args:
            packet: MailPacket to format

        Returns:
            Formatted markdown content
        """
        return f"""
---
from: {packet.sender}
to: {packet.recipient}
tracking_id: {packet.tracking_id}
priority: {packet.priority}
date: {packet.timestamp.isoformat()}
status: {packet.delivery_status}
---

# Mail: {packet.subject}

**From:** {packet.sender}
**To:** {packet.recipient}
**Date:** {packet.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
**Tracking:** {packet.tracking_id}

---

{packet.content}

---

*Delivered by Pack Rat Postal Service*
*Archives maintained by Artemis City Library*
"""

    def _log_delivery(self, packet: MailPacket, success: bool, reason: Optional[str] = None):
        """Log a delivery attempt."""
        self.delivery_log.append(
            {
                'tracking_id': packet.tracking_id,
                'sender': packet.sender,
                'recipient': packet.recipient,
                'subject': packet.subject,
                'priority': packet.priority,
                'timestamp': packet.timestamp,
                'success': success,
                'reason': reason,
                'status': packet.delivery_status,
            }
        )


# Global Post Office instance
_city_post_office = None


def get_post_office() -> PostOffice:
    """Get or create the City Post Office instance.

    Returns:
        Global PostOffice instance
    """
    global _city_post_office
    if _city_post_office is None:
        _city_post_office = PostOffice()
    return _city_post_office
