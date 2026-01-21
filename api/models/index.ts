/**
 * API Models Index
 *
 * Type definitions and interfaces for the API.
 */

// ============================================
// Agent Models
// ============================================

export interface Agent {
  id: string;
  name: string;
  role: string;
  status: AgentStatus;
  trustLevel: number;
  capabilities: string[];
  zones: string[];
  metadata: Record<string, any>;
  createdAt: string;
  updatedAt: string;
}

export type AgentStatus = 'active' | 'suspended' | 'inactive';

export interface AgentCard extends Agent {
  trustBadge: string;
  statusEmoji: string;
  formattedCapabilities: string;
  formattedZones: string;
}

export interface CreateAgentRequest {
  name: string;
  role?: string;
  trustLevel?: number;
  capabilities?: string[];
  zones?: string[];
  metadata?: Record<string, any>;
}

export interface UpdateAgentRequest {
  name?: string;
  role?: string;
  trustLevel?: number;
  capabilities?: string[];
  zones?: string[];
  metadata?: Record<string, any>;
  status?: AgentStatus;
}

// ============================================
// Memory Models
// ============================================

export interface MemoryEntry {
  path: string;
  content: string;
  metadata: MemoryMetadata;
  createdAt: string;
  updatedAt: string;
}

export interface MemoryMetadata {
  type?: string;
  tags?: string[];
  title?: string;
  author?: string;
  inlineTags?: string[];
  [key: string]: any;
}

export interface SearchResult {
  path: string;
  matches: string[];
  score: number;
}

export interface SearchOptions {
  path?: string;
  tags?: string[];
  limit?: number;
  offset?: number;
}

export interface ContextData {
  recentFiles: string[];
  activeTopics: string[];
  sessionContext: Record<string, any>;
}

export interface VaultStats {
  totalFiles: number;
  totalSize: number;
  averageSize: number;
  byType: Record<string, number>;
  recentActivity: string[];
}

// ============================================
// ATP Models
// ============================================

export type ATPMode = 'RESEARCH' | 'EXECUTE' | 'REPORT' | 'DELEGATE' | 'QUERY';
export type ATPPriority = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'BACKGROUND';
export type ATPActionType = 'CREATE' | 'READ' | 'UPDATE' | 'DELETE' | 'SEARCH' | 'ANALYZE' | 'SYNC' | 'NOTIFY';

export interface ATPHeader {
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

export interface ATPMessage {
  header: ATPHeader;
  payload: any;
  metadata?: Record<string, any>;
}

export interface ATPResponse {
  success: boolean;
  messageId: string;
  response?: any;
  error?: string;
  processingTime?: number;
}

export interface ATPValidationResult {
  valid: boolean;
  error?: string;
  warnings?: string[];
}

// ============================================
// Trust Models
// ============================================

export type TrustLevel = 'FULL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'UNTRUSTED';

export interface TrustScore {
  entityId: string;
  entityType: TrustEntityType;
  score: number;
  level: TrustLevel;
  successCount: number;
  failureCount: number;
  lastInteraction: string;
  createdAt: string;
  updatedAt: string;
}

export type TrustEntityType = 'agent' | 'user' | 'service' | 'external';

export interface TrustPermissions {
  entityId: string;
  level: TrustLevel;
  operations: string[];
}

export interface HebbianWeight {
  agent1: string;
  agent2: string;
  weight: number;
  interactions: number;
  lastUpdated: string;
}

export interface TrustReport {
  totalEntities: number;
  byLevel: Record<TrustLevel, number>;
  byType: Record<string, number>;
  averageScore: number;
  recentChanges: TrustScore[];
  hebbianConnections: number;
}

export interface TrustLevelDefinition {
  name: TrustLevel;
  minScore: number;
  operations: string[];
}

// ============================================
// API Response Models
// ============================================

export interface APISuccessResponse<T> {
  success: true;
  data: T;
  message?: string;
  meta?: Record<string, any>;
}

export interface APIErrorResponse {
  success: false;
  error: {
    message: string;
    code: string;
    statusCode: number;
    details?: any;
    timestamp: string;
    path?: string;
  };
}

export type APIResponse<T> = APISuccessResponse<T> | APIErrorResponse;

export interface PaginatedResponse<T> {
  success: true;
  data: T[];
  pagination: {
    currentPage: number;
    totalPages: number;
    totalItems: number;
    itemsPerPage: number;
    hasNextPage: boolean;
    hasPrevPage: boolean;
  };
}

// ============================================
// Health Models
// ============================================

export interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  version: string;
  uptime: number;
  timestamp: string;
  checks: HealthCheck[];
}

export interface HealthCheck {
  name: string;
  status: 'pass' | 'warn' | 'fail';
  message?: string;
  duration?: number;
}

// ============================================
// Request Context
// ============================================

export interface RequestContext {
  requestId: string;
  userId?: string;
  role?: string;
  permissions?: string[];
  timestamp: string;
}
