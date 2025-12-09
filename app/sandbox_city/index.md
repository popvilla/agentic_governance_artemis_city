# Sandbox City: Map of the Town

> **Purpose:** This document serves as a high-level guide to **Sandbox City**, a simulated environment used for testing and visualizing agent interactions. It maps the city's "zones" to their corresponding system functions, providing a narrative framework to make complex operations more understandable.

Sandbox City is a metaphorical and functional environment designed for agent immersion, simulation, and testing. It provides a narrative layer over system functions, making complex interactions more intuitive and observable.

## Overview:
This index serves as a map, detailing the various "zones" and their corresponding semantic and functional roles within the Agentic Codex. Each zone represents a specific area of system functionality or data handling.

## Semantic Zones (Examples):
*   **Post Office (Secure Load Zone)**: Where Pack Rat handles secure data transfers. Represents encrypted communication channels and data staging areas.
*   **Town Hall (Governance Hub)**: Where Artemis conducts audits and enforces policies. Represents the core governance and policy enforcement modules.
*   **Library (Memory Archives)**: The primary interface to the memory stack, managed by Codex Daemon. Represents persistent data storage and retrieval systems.
*   **Workshop (Agent Development & Testing)**: A controlled environment for new agent onboarding and validation simulations.
*   **Public Square (Interface Layer)**: Where the Codex CLI and other human interfaces reside. Represents user interaction points.
*   **Watchtower (Monitoring & Logging)**: System health checks and anomaly detection.

## Town Logic Metaphor:
The "town logic" supports agent immersion by providing a relatable narrative. Agents interact with "buildings" or "citizens" (other agents/modules) according to their roles within the city, making their functions and interdependencies clearer. This also aids in visualizing data flow and operational states.

## Linked Scripts:
*   `networked_scripts/mail_delivery_sim.py`: Simulates the Post Office operations.
*   `networked_scripts/system_health_check.sh`: Monitors the overall health of the Town Hall and other critical infrastructure.