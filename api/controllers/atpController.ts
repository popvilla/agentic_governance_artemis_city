/**
 * ATP Controller
 *
 * Handles business logic for Artemis Transmission Protocol operations.
 */

// ATP Message Types
type ATPMode = 'RESEARCH' | 'EXECUTE' | 'REPORT' | 'DELEGATE' | 'QUERY';
type ATPPriority = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'BACKGROUND';
type ATPActionType = 'CREATE' | 'READ' | 'UPDATE' | 'DELETE' | 'SEARCH' | 'ANALYZE' | 'SYNC' | 'NOTIFY';

interface ATPHeader {
  mode: ATPMode;
  context: string;
  priority: ATPPriority;
  actionType: ATPActionType;
  targetZone: string;
  specialNotes?: string;
  timestamp: string;
  messageId: string;
  senderId: string;
  receiverId?: string;
}

interface ATPMessage {
  header: ATPHeader;
  payload: any;
  metadata?: Record<string, any>;
}

interface ATPResponse {
  success: boolean;
  messageId: string;
  response?: any;
  error?: string;
  processingTime?: number;
}

// Message queue for async processing
const messageQueue: ATPMessage[] = [];
const messageHistory: Map<string, ATPMessage> = new Map();
const responseHistory: Map<string, ATPResponse> = new Map();

// Valid values for validation
const VALID_MODES: ATPMode[] = ['RESEARCH', 'EXECUTE', 'REPORT', 'DELEGATE', 'QUERY'];
const VALID_PRIORITIES: ATPPriority[] = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'BACKGROUND'];
const VALID_ACTION_TYPES: ATPActionType[] = ['CREATE', 'READ', 'UPDATE', 'DELETE', 'SEARCH', 'ANALYZE', 'SYNC', 'NOTIFY'];

export class ATPController {
  /**
   * Send an ATP message
   */
  async sendMessage(message: Partial<ATPMessage>): Promise<ATPResponse> {
    const startTime = Date.now();

    // Validate and complete the message
    const validation = this.validateMessage(message);
    if (!validation.valid) {
      return {
        success: false,
        messageId: '',
        error: validation.error
      };
    }

    // Generate message ID
    const messageId = this.generateMessageId();

    // Build complete message
    const completeMessage: ATPMessage = {
      header: {
        mode: message.header?.mode || 'QUERY',
        context: message.header?.context || 'general',
        priority: message.header?.priority || 'MEDIUM',
        actionType: message.header?.actionType || 'READ',
        targetZone: message.header?.targetZone || 'system',
        specialNotes: message.header?.specialNotes,
        timestamp: new Date().toISOString(),
        messageId,
        senderId: message.header?.senderId || 'api',
        receiverId: message.header?.receiverId
      },
      payload: message.payload || {},
      metadata: message.metadata || {}
    };

    // Store message
    messageHistory.set(messageId, completeMessage);

    // Route message
    const routeResult = await this.routeMessage(completeMessage);

    const response: ATPResponse = {
      success: true,
      messageId,
      response: routeResult,
      processingTime: Date.now() - startTime
    };

    responseHistory.set(messageId, response);
    return response;
  }

  /**
   * Route a message to appropriate handler
   */
  async routeMessage(message: ATPMessage): Promise<any> {
    const { mode, actionType, targetZone, receiverId } = message.header;

    // Determine routing based on mode and target
    const routingInfo = {
      routed: true,
      destination: receiverId || this.determineDestination(targetZone),
      mode,
      actionType,
      timestamp: new Date().toISOString()
    };

    // Add to queue for processing
    messageQueue.push(message);

    // Simulate processing based on action type
    switch (actionType) {
      case 'CREATE':
        return { ...routingInfo, action: 'Creating resource', status: 'queued' };
      case 'READ':
        return { ...routingInfo, action: 'Reading resource', status: 'processing' };
      case 'UPDATE':
        return { ...routingInfo, action: 'Updating resource', status: 'queued' };
      case 'DELETE':
        return { ...routingInfo, action: 'Deleting resource', status: 'queued' };
      case 'SEARCH':
        return { ...routingInfo, action: 'Searching', status: 'processing' };
      case 'ANALYZE':
        return { ...routingInfo, action: 'Analyzing', status: 'processing' };
      case 'SYNC':
        return { ...routingInfo, action: 'Synchronizing', status: 'queued' };
      case 'NOTIFY':
        return { ...routingInfo, action: 'Sending notification', status: 'sent' };
      default:
        return { ...routingInfo, action: 'Unknown action', status: 'pending' };
    }
  }

  /**
   * Validate an ATP message
   */
  validateMessage(message: Partial<ATPMessage>): { valid: boolean; error?: string; warnings?: string[] } {
    const warnings: string[] = [];

    // Check required header fields
    if (!message.header) {
      return { valid: false, error: 'Message header is required' };
    }

    const { mode, priority, actionType, targetZone, senderId } = message.header;

    // Validate mode
    if (mode && !VALID_MODES.includes(mode)) {
      return { valid: false, error: `Invalid mode: ${mode}. Valid modes: ${VALID_MODES.join(', ')}` };
    }

    // Validate priority
    if (priority && !VALID_PRIORITIES.includes(priority)) {
      return { valid: false, error: `Invalid priority: ${priority}. Valid priorities: ${VALID_PRIORITIES.join(', ')}` };
    }

    // Validate action type
    if (actionType && !VALID_ACTION_TYPES.includes(actionType)) {
      return { valid: false, error: `Invalid actionType: ${actionType}. Valid types: ${VALID_ACTION_TYPES.join(', ')}` };
    }

    // Warnings for missing optional fields
    if (!targetZone) {
      warnings.push('No targetZone specified, defaulting to "system"');
    }

    if (!senderId) {
      warnings.push('No senderId specified, defaulting to "api"');
    }

    return { valid: true, warnings: warnings.length > 0 ? warnings : undefined };
  }

  /**
   * Format a message for display
   */
  formatMessage(message: ATPMessage): string {
    const { header, payload } = message;

    const lines = [
      '╔══════════════════════════════════════════════════════════════╗',
      '║                    ATP TRANSMISSION                          ║',
      '╠══════════════════════════════════════════════════════════════╣',
      `║ Mode:       ${header.mode.padEnd(48)}║`,
      `║ Context:    ${header.context.padEnd(48)}║`,
      `║ Priority:   ${header.priority.padEnd(48)}║`,
      `║ Action:     ${header.actionType.padEnd(48)}║`,
      `║ Target:     ${header.targetZone.padEnd(48)}║`,
      `║ From:       ${header.senderId.padEnd(48)}║`,
      `║ To:         ${(header.receiverId || 'broadcast').padEnd(48)}║`,
      `║ Time:       ${header.timestamp.padEnd(48)}║`,
      `║ ID:         ${header.messageId.padEnd(48)}║`,
    ];

    if (header.specialNotes) {
      lines.push('╠══════════════════════════════════════════════════════════════╣');
      lines.push(`║ Notes: ${header.specialNotes.slice(0, 52).padEnd(52)}║`);
    }

    lines.push('╠══════════════════════════════════════════════════════════════╣');
    lines.push('║ PAYLOAD                                                      ║');
    lines.push('╠══════════════════════════════════════════════════════════════╣');

    const payloadStr = JSON.stringify(payload, null, 2);
    const payloadLines = payloadStr.split('\n').slice(0, 5);
    payloadLines.forEach(line => {
      lines.push(`║ ${line.slice(0, 60).padEnd(60)}║`);
    });
    if (payloadStr.split('\n').length > 5) {
      lines.push('║ ...                                                          ║');
    }

    lines.push('╚══════════════════════════════════════════════════════════════╝');

    return lines.join('\n');
  }

  /**
   * Get available modes
   */
  getModes(): { name: ATPMode; description: string }[] {
    return [
      { name: 'RESEARCH', description: 'Information gathering and analysis' },
      { name: 'EXECUTE', description: 'Perform a specific action' },
      { name: 'REPORT', description: 'Generate status or progress report' },
      { name: 'DELEGATE', description: 'Assign task to another agent' },
      { name: 'QUERY', description: 'Ask a question or request data' }
    ];
  }

  /**
   * Get available priorities
   */
  getPriorities(): { name: ATPPriority; description: string; color: string }[] {
    return [
      { name: 'CRITICAL', description: 'Immediate attention required', color: 'red' },
      { name: 'HIGH', description: 'Process as soon as possible', color: 'orange' },
      { name: 'MEDIUM', description: 'Normal processing priority', color: 'yellow' },
      { name: 'LOW', description: 'Can wait for other tasks', color: 'blue' },
      { name: 'BACKGROUND', description: 'Process when idle', color: 'gray' }
    ];
  }

  /**
   * Get available action types
   */
  getActionTypes(): { name: ATPActionType; description: string }[] {
    return [
      { name: 'CREATE', description: 'Create a new resource' },
      { name: 'READ', description: 'Read/retrieve a resource' },
      { name: 'UPDATE', description: 'Update an existing resource' },
      { name: 'DELETE', description: 'Delete a resource' },
      { name: 'SEARCH', description: 'Search for resources' },
      { name: 'ANALYZE', description: 'Analyze data or content' },
      { name: 'SYNC', description: 'Synchronize resources' },
      { name: 'NOTIFY', description: 'Send a notification' }
    ];
  }

  /**
   * Get message by ID
   */
  getMessage(messageId: string): ATPMessage | null {
    return messageHistory.get(messageId) || null;
  }

  /**
   * Get response by message ID
   */
  getResponse(messageId: string): ATPResponse | null {
    return responseHistory.get(messageId) || null;
  }

  /**
   * Get message queue status
   */
  getQueueStatus(): { pending: number; recent: ATPMessage[] } {
    return {
      pending: messageQueue.length,
      recent: messageQueue.slice(-5)
    };
  }

  // Helper methods
  private generateMessageId(): string {
    return `atp-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
  }

  private determineDestination(targetZone: string): string {
    const zoneToAgent: Record<string, string> = {
      'vault': 'packrat',
      'memory': 'packrat',
      'user': 'copilot',
      'interface': 'copilot',
      'system': 'daemon',
      'background': 'daemon',
      'all': 'artemis',
      'orchestration': 'artemis'
    };

    return zoneToAgent[targetZone] || 'artemis';
  }
}
