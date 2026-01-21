/**
 * Trust Controller
 *
 * Handles business logic for trust management and Hebbian learning.
 */

type TrustLevel = 'FULL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'UNTRUSTED';

interface TrustScore {
  entityId: string;
  entityType: 'agent' | 'user' | 'service' | 'external';
  score: number;
  level: TrustLevel;
  successCount: number;
  failureCount: number;
  lastInteraction: string;
  createdAt: string;
  updatedAt: string;
}

interface HebbianWeight {
  agent1: string;
  agent2: string;
  weight: number;
  interactions: number;
  lastUpdated: string;
}

interface TrustReport {
  totalEntities: number;
  byLevel: Record<TrustLevel, number>;
  byType: Record<string, number>;
  averageScore: number;
  recentChanges: TrustScore[];
  hebbianConnections: number;
}

// Trust level thresholds
const TRUST_THRESHOLDS = {
  FULL: 0.9,
  HIGH: 0.7,
  MEDIUM: 0.5,
  LOW: 0.3,
  UNTRUSTED: 0
};

// Operations allowed at each trust level
const TRUST_OPERATIONS: Record<TrustLevel, string[]> = {
  FULL: ['read', 'write', 'delete', 'search', 'tag', 'update', 'frontmatter'],
  HIGH: ['read', 'write', 'search', 'tag', 'update', 'frontmatter'],
  MEDIUM: ['read', 'write', 'search', 'tag'],
  LOW: ['read', 'search'],
  UNTRUSTED: []
};

// In-memory stores
const trustStore: Map<string, TrustScore> = new Map();
const hebbianWeights: Map<string, HebbianWeight> = new Map();

// Initialize default trust scores for known agents
const defaultTrustScores: TrustScore[] = [
  {
    entityId: 'artemis',
    entityType: 'agent',
    score: 0.95,
    level: 'FULL',
    successCount: 1000,
    failureCount: 5,
    lastInteraction: new Date().toISOString(),
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  {
    entityId: 'packrat',
    entityType: 'agent',
    score: 0.85,
    level: 'HIGH',
    successCount: 800,
    failureCount: 20,
    lastInteraction: new Date().toISOString(),
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  {
    entityId: 'copilot',
    entityType: 'agent',
    score: 0.80,
    level: 'HIGH',
    successCount: 500,
    failureCount: 25,
    lastInteraction: new Date().toISOString(),
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  {
    entityId: 'daemon',
    entityType: 'agent',
    score: 0.85,
    level: 'HIGH',
    successCount: 600,
    failureCount: 15,
    lastInteraction: new Date().toISOString(),
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
];

// Initialize stores
defaultTrustScores.forEach(ts => trustStore.set(ts.entityId, ts));

// Initialize Hebbian connections
const defaultHebbianWeights: HebbianWeight[] = [
  { agent1: 'artemis', agent2: 'packrat', weight: 0.8, interactions: 500, lastUpdated: new Date().toISOString() },
  { agent1: 'artemis', agent2: 'copilot', weight: 0.75, interactions: 400, lastUpdated: new Date().toISOString() },
  { agent1: 'artemis', agent2: 'daemon', weight: 0.7, interactions: 300, lastUpdated: new Date().toISOString() },
  { agent1: 'packrat', agent2: 'copilot', weight: 0.6, interactions: 200, lastUpdated: new Date().toISOString() },
  { agent1: 'packrat', agent2: 'daemon', weight: 0.5, interactions: 150, lastUpdated: new Date().toISOString() },
  { agent1: 'copilot', agent2: 'daemon', weight: 0.4, interactions: 100, lastUpdated: new Date().toISOString() }
];

defaultHebbianWeights.forEach(hw => {
  const key = `${hw.agent1}-${hw.agent2}`;
  hebbianWeights.set(key, hw);
});

export class TrustController {
  /**
   * Get trust score for an entity
   */
  async getTrustScore(entityId: string): Promise<TrustScore | null> {
    return trustStore.get(entityId) || null;
  }

  /**
   * Set trust score for an entity
   */
  async setTrustScore(entityId: string, score: number, entityType: string = 'agent'): Promise<TrustScore> {
    const existing = trustStore.get(entityId);
    const now = new Date().toISOString();

    const trustScore: TrustScore = {
      entityId,
      entityType: entityType as TrustScore['entityType'],
      score: Math.max(0, Math.min(1, score)),
      level: this.scoreToLevel(score),
      successCount: existing?.successCount || 0,
      failureCount: existing?.failureCount || 0,
      lastInteraction: now,
      createdAt: existing?.createdAt || now,
      updatedAt: now
    };

    trustStore.set(entityId, trustScore);
    return trustScore;
  }

  /**
   * Record a successful operation
   */
  async recordSuccess(entityId: string, amount: number = 0.02): Promise<number | null> {
    const trust = trustStore.get(entityId);
    if (!trust) return null;

    trust.score = Math.min(1, trust.score + amount);
    trust.level = this.scoreToLevel(trust.score);
    trust.successCount++;
    trust.lastInteraction = new Date().toISOString();
    trust.updatedAt = new Date().toISOString();

    trustStore.set(entityId, trust);
    return trust.score;
  }

  /**
   * Record a failed operation
   */
  async recordFailure(entityId: string, amount: number = 0.05): Promise<number | null> {
    const trust = trustStore.get(entityId);
    if (!trust) return null;

    trust.score = Math.max(0, trust.score - amount);
    trust.level = this.scoreToLevel(trust.score);
    trust.failureCount++;
    trust.lastInteraction = new Date().toISOString();
    trust.updatedAt = new Date().toISOString();

    trustStore.set(entityId, trust);
    return trust.score;
  }

  /**
   * Get permissions for an entity
   */
  async getPermissions(entityId: string): Promise<{ entityId: string; level: TrustLevel; operations: string[] }> {
    const trust = trustStore.get(entityId);
    const level = trust?.level || 'UNTRUSTED';

    return {
      entityId,
      level,
      operations: TRUST_OPERATIONS[level]
    };
  }

  /**
   * Check if entity can perform operation
   */
  async canPerformOperation(entityId: string, operation: string): Promise<boolean> {
    const trust = trustStore.get(entityId);
    if (!trust) return false;

    return TRUST_OPERATIONS[trust.level].includes(operation);
  }

  /**
   * Get Hebbian weights
   */
  async getHebbianWeights(): Promise<HebbianWeight[]> {
    return Array.from(hebbianWeights.values());
  }

  /**
   * Update Hebbian weight between two agents
   */
  async updateHebbianWeight(agent1: string, agent2: string, delta: number): Promise<number> {
    // Ensure consistent key ordering
    const [a1, a2] = [agent1, agent2].sort();
    const key = `${a1}-${a2}`;

    const existing = hebbianWeights.get(key);
    const now = new Date().toISOString();

    if (existing) {
      existing.weight = Math.max(0, Math.min(1, existing.weight + delta));
      existing.interactions++;
      existing.lastUpdated = now;
      hebbianWeights.set(key, existing);
      return existing.weight;
    } else {
      const newWeight: HebbianWeight = {
        agent1: a1,
        agent2: a2,
        weight: Math.max(0, Math.min(1, 0.5 + delta)),
        interactions: 1,
        lastUpdated: now
      };
      hebbianWeights.set(key, newWeight);
      return newWeight.weight;
    }
  }

  /**
   * Get comprehensive trust report
   */
  async getTrustReport(): Promise<TrustReport> {
    const entities = Array.from(trustStore.values());

    // Count by level
    const byLevel: Record<TrustLevel, number> = {
      FULL: 0,
      HIGH: 0,
      MEDIUM: 0,
      LOW: 0,
      UNTRUSTED: 0
    };

    // Count by type
    const byType: Record<string, number> = {};

    let totalScore = 0;

    entities.forEach(entity => {
      byLevel[entity.level]++;
      byType[entity.entityType] = (byType[entity.entityType] || 0) + 1;
      totalScore += entity.score;
    });

    // Get recent changes (sorted by updatedAt)
    const recentChanges = entities
      .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime())
      .slice(0, 5);

    return {
      totalEntities: entities.length,
      byLevel,
      byType,
      averageScore: entities.length > 0 ? totalScore / entities.length : 0,
      recentChanges,
      hebbianConnections: hebbianWeights.size
    };
  }

  /**
   * Apply trust decay (called periodically)
   */
  async applyDecay(decayRate: number = 0.01): Promise<number> {
    let affected = 0;
    const now = new Date();

    for (const [entityId, trust] of trustStore) {
      const lastInteraction = new Date(trust.lastInteraction);
      const daysSinceInteraction = (now.getTime() - lastInteraction.getTime()) / (1000 * 60 * 60 * 24);

      if (daysSinceInteraction > 1) {
        const decay = decayRate * Math.floor(daysSinceInteraction);
        trust.score = Math.max(0.3, trust.score - decay); // Don't decay below LOW
        trust.level = this.scoreToLevel(trust.score);
        trust.updatedAt = now.toISOString();
        trustStore.set(entityId, trust);
        affected++;
      }
    }

    return affected;
  }

  /**
   * Get trust level definitions
   */
  getTrustLevels(): { name: TrustLevel; minScore: number; operations: string[] }[] {
    return [
      { name: 'FULL', minScore: TRUST_THRESHOLDS.FULL, operations: TRUST_OPERATIONS.FULL },
      { name: 'HIGH', minScore: TRUST_THRESHOLDS.HIGH, operations: TRUST_OPERATIONS.HIGH },
      { name: 'MEDIUM', minScore: TRUST_THRESHOLDS.MEDIUM, operations: TRUST_OPERATIONS.MEDIUM },
      { name: 'LOW', minScore: TRUST_THRESHOLDS.LOW, operations: TRUST_OPERATIONS.LOW },
      { name: 'UNTRUSTED', minScore: TRUST_THRESHOLDS.UNTRUSTED, operations: TRUST_OPERATIONS.UNTRUSTED }
    ];
  }

  // Helper methods
  private scoreToLevel(score: number): TrustLevel {
    if (score >= TRUST_THRESHOLDS.FULL) return 'FULL';
    if (score >= TRUST_THRESHOLDS.HIGH) return 'HIGH';
    if (score >= TRUST_THRESHOLDS.MEDIUM) return 'MEDIUM';
    if (score >= TRUST_THRESHOLDS.LOW) return 'LOW';
    return 'UNTRUSTED';
  }
}
