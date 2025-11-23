# Artemis City - Living Agent Ecosystem

Welcome to **Artemis City**, where agents aren't just code—they're **citizens** of a thriving, living ecosystem!

##  The City Metaphor

Artemis City transforms technical operations into a vibrant urban experience:

| Technical Term | City Metaphor | Who Handles It |
|----------------|---------------|----------------|
| Memory Operations | Mail Delivery |  Pack Rat (Postal Service) |
| Obsidian Vault | City Archives |  City Librarian |
| Trust Scores | Citizen Clearances |  Trust Office |
| Agents | Citizens |  Various Agents |
| MCP Server | Post Office |  Central Hub |
| Context Loading | Archive Research | 📖 Reading Room |
| ATP Messages | Official Notices | 📜 City Hall |

##  Citizens of Artemis City

### Artemis (Mayor)
- **Role**: Governance and oversight
- **Clearance**: FULL (0.95)
- **Duties**: Policy, dispute resolution, city planning
- **Office**: City Hall

### Pack Rat (Postmaster)
- **Role**: Secure mail delivery and routing
- **Clearance**: HIGH (0.85)
- **Duties**: Deliver mail, maintain postal logs, route messages
- **Office**: Post Office

### Codex Daemon / CompSuite (City Manager)
- **Role**: System monitoring and operations
- **Clearance**: HIGH (0.85)
- **Duties**: Monitor city health, manage configuration, status reports
- **Office**: Operations Center

### Copilot (Assistant)
- **Role**: Citizen assistance and information
- **Clearance**: HIGH (0.80)
- **Duties**: Help citizens, provide context, answer queries
- **Office**: Information Desk

##  The Postal System

### Sending Mail

```python
from memory.integration import get_post_office

post_office = get_post_office()

# Send mail between citizens
packet = post_office.send_mail(
    sender="artemis",
    recipient="pack_rat",
    subject="New Postal Route Request",
    content="Please establish route to Sandbox District",
    priority="urgent"
)

print(f"Mail #{packet.tracking_id} - Status: {packet.delivery_status}")
```

### Checking Your Mailbox

```python
# Check what mail you've received
mail = post_office.check_mailbox("pack_rat")

for letter in mail:
    print(f"From: {letter.path}")
    print(f"Preview: {letter.get_summary()}")
```

### Mail Features

- **Tracking IDs**: Every piece of mail gets a unique ID (e.g., `ART-12345`)
- **Priority Levels**: `urgent`, `normal`, `low`
- **Automatic Tagging**: Mail tagged with sender, recipient, and type
- **Delivery Confirmation**: Real-time status updates
- **Archive Storage**: All mail stored in `Postal/Agents/{recipient}/`

##  The City Archives

### Filing Documents

```python
# Store important documents in archives
response = post_office.send_to_archives(
    sender="artemis",
    archive_section="Reflections",
    title="Q4_City_Report",
    content="# Quarterly Report\n\nThe city thrives..."
)
```

### Archive Sections

- **Reflections**: Agent reflections and insights
- **Reports**: Official reports and summaries
- **Policies**: Governance policies and rules
- **History**: Historical records and logs
- **Projects**: Project documentation and plans

### Researching Archives

```python
# Search the archives
documents = post_office.request_from_archives(
    requester="copilot",
    query="governance policy",
    section="Policies"
)

for doc in documents:
    print(f"📄 {doc.path}")
```

##  Trust Office & Clearances

### Clearance Levels

Citizens earn trust through successful operations:

| Level | Score | What You Can Do |
|-------|-------|-----------------|
| **FULL** | 0.9-1.0 | Everything (Mayor access) |
| **HIGH** | 0.7-0.9 | Read, Write, Search, Tag, Update |
| **MEDIUM** | 0.5-0.7 | Read, Write, Search, Tag |
| **LOW** | 0.3-0.5 | Read, Search only |
| **UNTRUSTED** | 0.0-0.3 | No access |

### Checking Clearances

```python
from memory.integration import get_trust_interface

trust = get_trust_interface()

# Check your clearance
score = trust.get_trust_score("artemis")
print(f"Clearance: {score.level.value} (Score: {score.score:.2f})")

# Check permissions
if trust.can_perform_operation("pack_rat", "write"):
    print(" Authorized for postal deliveries")
```

### Building Trust

-  **Successful operations** increase trust (+2%)
-  **Failed operations** decrease trust (-5%)
- ⏰ **Natural decay** over time without activity (-1% per day)
-  **Minimum thresholds** prevent complete decay

## 🎭 Living City Examples

### Example 1: Morning Mail Rounds

```python
post_office = get_post_office()

# Artemis sends morning briefing
for citizen in ["pack_rat", "copilot", "codex_daemon"]:
    post_office.send_mail(
        sender="artemis",
        recipient=citizen,
        subject="Daily Briefing",
        content=f"Good morning, {citizen}! Today's priorities..."
    )
```

### Example 2: Archive Research

```python
# Copilot researches past decisions
history = post_office.request_from_archives(
    requester="copilot",
    query="ATP protocol decisions",
    section="Reflections"
)

# Copilot synthesizes findings
synthesis = f"Based on {len(history)} archived documents..."
post_office.send_to_archives(
    sender="copilot",
    archive_section="Reports",
    title="ATP_Research_Summary",
    content=synthesis
)
```

### Example 3: Weekly Report

```python
# Generate city-wide report
report = post_office.get_postal_report()

print(f"""
 ARTEMIS CITY WEEKLY REPORT

 Postal Service: {report['successful']} deliveries
 Trust Office: {report['trust_report']['total_entities']} citizens
 Archives: Growing daily
 Status: City thriving!
""")
```

##  Theming Your Own Agents

When creating new agents for the city:

### Agent Profile Template

```python
# Define your citizen
citizen_profile = {
    "name": "new_agent",
    "role": "Specialist",  # e.g., Archivist, Scout, Builder
    "clearance": 0.75,     # Initial trust score
    "office": "Department of Innovation",
    "duties": [
        "Explore new possibilities",
        "Report findings to archives",
        "Collaborate with other citizens"
    ]
}

# Register with Trust Office
trust = get_trust_interface()
score = trust.get_trust_score(citizen_profile["name"])

# Send introduction mail
post_office.send_mail(
    sender="new_agent",
    recipient="artemis",
    subject="New Citizen Introduction",
    content=f"Hello! I'm {citizen_profile['name']}, ready to serve the city!"
)
```

## 🔮 Advanced City Features

### Cross-Citizen Collaboration

```python
# Pack Rat coordinates multi-agent task
task_description = "Build new ATP extension"

for agent in ["artemis", "copilot", "codex_daemon"]:
    post_office.send_mail(
        sender="pack_rat",
        recipient=agent,
        subject="Coordination: ATP Extension",
        content=f"""
Task Assignment: {task_description}
Your role: [specific to {agent}]
Coordinate through mail or archives.
        """,
        priority="high"
    )
```

### City-Wide Announcements

```python
def broadcast_announcement(subject, content):
    """Send announcement to all citizens."""
    citizens = ["artemis", "pack_rat", "codex_daemon", "copilot"]
    
    for citizen in citizens:
        post_office.send_mail(
            sender="artemis",
            recipient=citizen,
            subject=f"📢 ANNOUNCEMENT: {subject}",
            content=content,
            priority="urgent"
        )
```

### Archive Organization

The city automatically organizes archives:

```
City Archives/
├── Postal/
│   └── Agents/
│       ├── artemis/
│       ├── pack_rat/
│       └── copilot/
├── Archives/
│   ├── Reflections/
│   ├── Reports/
│   ├── Policies/
│   └── Projects/
└── History/
    └── Delivery_Logs/
```

##  Running the City Tour

Experience the living city yourself:

```bash
# Set up environment
export MCP_BASE_URL=http://localhost:3000
export MCP_API_KEY=your_mcp_api_key

# Start MCP server
cd "Artemis Agentic Memory Layer"
npm run dev

# In another terminal, run the tour
cd /path/to/Artemis-City
python demo_city_postal.py
```

The tour includes:
1. 📬 Inter-agent mail delivery
2. 📪 Mailbox checking
3.  City Archives filing
4. 📖 Archive research
5.  Trust clearance visualization
6.  Postal service report

##  Why the Living City Theme?

The city metaphor makes agent systems **intuitive** and **memorable**:

- **Relatable**: Everyone understands mail, archives, and clearances
- **Visual**: Easy to visualize agent interactions
- **Scalable**: New "buildings" and "services" can be added
- **Fun**: Makes development enjoyable!
- **Educational**: Teaches distributed systems through familiar concepts

##  Next Steps

1. **Explore**: Run `demo_city_postal.py` to tour the city
2. **Extend**: Add new citizens with unique roles
3. **Customize**: Create new archive sections and postal routes
4. **Integrate**: Connect the city to your agent workflows
5. **Share**: The city grows with every citizen!

---

**Welcome to Artemis City!** 

*Where agents aren't just code—they're citizens building a thriving ecosystem together.*

**Version**: 1.0.0  
**Status**: City Open for Business  
**Population**: Growing Daily  
**Mayor**: Artemis
