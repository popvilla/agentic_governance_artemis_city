/**
 * LLM Controller
 *
 * Handles interactions with LLM providers (Claude, OpenAI, local models).
 */

// Types
interface Message {
  role: 'system' | 'user' | 'assistant';
  content: string;
  name?: string;
}

interface ChatOptions {
  temperature?: number;
  maxTokens?: number;
  topP?: number;
  stopSequences?: string[];
  systemPrompt?: string;
}

interface ChatResponse {
  id: string;
  model: string;
  content: string;
  role: 'assistant';
  finishReason: string;
  usage: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  createdAt: string;
}

interface EmbeddingResponse {
  model: string;
  embedding: number[];
  dimensions: number;
  usage: {
    totalTokens: number;
  };
}

interface StreamChunk {
  id: string;
  delta: string;
  finishReason?: string;
}

interface ModelInfo {
  id: string;
  name: string;
  provider: string;
  contextWindow: number;
  maxOutputTokens: number;
  inputCostPer1k: number;
  outputCostPer1k: number;
  capabilities: string[];
}

interface ProviderConfig {
  name: string;
  enabled: boolean;
  apiKey?: string;
  baseUrl?: string;
  defaultModel?: string;
  options?: Record<string, any>;
}

interface UsageStats {
  totalRequests: number;
  totalTokens: number;
  promptTokens: number;
  completionTokens: number;
  estimatedCost: number;
  byModel: Record<string, { requests: number; tokens: number }>;
  byDay: Record<string, { requests: number; tokens: number }>;
}

// Available models
const MODELS: ModelInfo[] = [
  {
    id: 'claude-3-opus-20240229',
    name: 'Claude 3 Opus',
    provider: 'anthropic',
    contextWindow: 200000,
    maxOutputTokens: 4096,
    inputCostPer1k: 0.015,
    outputCostPer1k: 0.075,
    capabilities: ['chat', 'vision', 'analysis', 'coding']
  },
  {
    id: 'claude-3-sonnet-20240229',
    name: 'Claude 3 Sonnet',
    provider: 'anthropic',
    contextWindow: 200000,
    maxOutputTokens: 4096,
    inputCostPer1k: 0.003,
    outputCostPer1k: 0.015,
    capabilities: ['chat', 'vision', 'analysis', 'coding']
  },
  {
    id: 'claude-3-haiku-20240307',
    name: 'Claude 3 Haiku',
    provider: 'anthropic',
    contextWindow: 200000,
    maxOutputTokens: 4096,
    inputCostPer1k: 0.00025,
    outputCostPer1k: 0.00125,
    capabilities: ['chat', 'vision', 'fast']
  },
  {
    id: 'gpt-4-turbo',
    name: 'GPT-4 Turbo',
    provider: 'openai',
    contextWindow: 128000,
    maxOutputTokens: 4096,
    inputCostPer1k: 0.01,
    outputCostPer1k: 0.03,
    capabilities: ['chat', 'vision', 'function-calling', 'coding']
  },
  {
    id: 'gpt-4o',
    name: 'GPT-4o',
    provider: 'openai',
    contextWindow: 128000,
    maxOutputTokens: 4096,
    inputCostPer1k: 0.005,
    outputCostPer1k: 0.015,
    capabilities: ['chat', 'vision', 'function-calling', 'coding', 'fast']
  },
  {
    id: 'gpt-3.5-turbo',
    name: 'GPT-3.5 Turbo',
    provider: 'openai',
    contextWindow: 16385,
    maxOutputTokens: 4096,
    inputCostPer1k: 0.0005,
    outputCostPer1k: 0.0015,
    capabilities: ['chat', 'function-calling', 'fast']
  },
  {
    id: 'local-llama',
    name: 'Local LLaMA',
    provider: 'local',
    contextWindow: 4096,
    maxOutputTokens: 2048,
    inputCostPer1k: 0,
    outputCostPer1k: 0,
    capabilities: ['chat', 'offline']
  }
];

// Provider configurations
const providers: Map<string, ProviderConfig> = new Map([
  ['anthropic', {
    name: 'Anthropic',
    enabled: true,
    baseUrl: 'https://api.anthropic.com/v1',
    defaultModel: 'claude-3-sonnet-20240229'
  }],
  ['openai', {
    name: 'OpenAI',
    enabled: true,
    baseUrl: 'https://api.openai.com/v1',
    defaultModel: 'gpt-4o'
  }],
  ['local', {
    name: 'Local',
    enabled: false,
    baseUrl: 'http://localhost:11434',
    defaultModel: 'local-llama'
  }]
]);

// Usage tracking
const usageLog: Array<{
  timestamp: string;
  provider: string;
  model: string;
  promptTokens: number;
  completionTokens: number;
}> = [];

export class LLMController {
  private defaultModel = 'claude-3-sonnet-20240229';

  /**
   * Send a chat completion request
   */
  async chat(messages: Message[], model?: string, options: ChatOptions = {}): Promise<ChatResponse> {
    const selectedModel = model || this.defaultModel;
    const modelInfo = MODELS.find(m => m.id === selectedModel);

    if (!modelInfo) {
      throw new Error(`Unknown model: ${selectedModel}`);
    }

    const provider = providers.get(modelInfo.provider);
    if (!provider?.enabled) {
      throw new Error(`Provider ${modelInfo.provider} is not enabled`);
    }

    // Simulate API call (in production, call actual API)
    const response = await this.simulateChat(messages, selectedModel, options);

    // Log usage
    this.logUsage(modelInfo.provider, selectedModel, response.usage.promptTokens, response.usage.completionTokens);

    return response;
  }

  /**
   * Send a text completion request
   */
  async complete(prompt: string, model?: string, options: ChatOptions = {}): Promise<ChatResponse> {
    // Convert to chat format
    const messages: Message[] = [{ role: 'user', content: prompt }];
    return this.chat(messages, model, options);
  }

  /**
   * Generate embeddings
   */
  async embed(text: string | string[], model?: string): Promise<EmbeddingResponse> {
    const texts = Array.isArray(text) ? text : [text];
    const embeddingModel = model || 'text-embedding-3-small';

    // Simulate embedding generation
    const dimensions = 1536;
    const embedding = Array(dimensions).fill(0).map(() => Math.random() * 2 - 1);

    // Normalize
    const magnitude = Math.sqrt(embedding.reduce((sum, val) => sum + val * val, 0));
    const normalized = embedding.map(val => val / magnitude);

    return {
      model: embeddingModel,
      embedding: normalized,
      dimensions,
      usage: {
        totalTokens: texts.join(' ').split(/\s+/).length
      }
    };
  }

  /**
   * Stream chat completion
   */
  async streamChat(
    messages: Message[],
    model?: string,
    options: ChatOptions = {},
    onChunk: (chunk: StreamChunk) => void = () => {}
  ): Promise<void> {
    const selectedModel = model || this.defaultModel;
    const id = `stream-${Date.now()}`;

    // Simulate streaming
    const fullResponse = await this.simulateChat(messages, selectedModel, options);
    const words = fullResponse.content.split(' ');

    for (let i = 0; i < words.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 50));
      onChunk({
        id,
        delta: words[i] + (i < words.length - 1 ? ' ' : ''),
        finishReason: i === words.length - 1 ? 'stop' : undefined
      });
    }
  }

  /**
   * List available models
   */
  async listModels(): Promise<ModelInfo[]> {
    return MODELS.filter(model => {
      const provider = providers.get(model.provider);
      return provider?.enabled;
    });
  }

  /**
   * Get configured providers
   */
  getProviders(): ProviderConfig[] {
    return Array.from(providers.values());
  }

  /**
   * Configure a provider
   */
  async configureProvider(
    providerName: string,
    config: Partial<ProviderConfig>
  ): Promise<ProviderConfig> {
    const existing = providers.get(providerName);

    if (!existing) {
      throw new Error(`Unknown provider: ${providerName}`);
    }

    const updated: ProviderConfig = {
      ...existing,
      ...config,
      name: existing.name // Don't allow name change
    };

    providers.set(providerName, updated);
    return updated;
  }

  /**
   * Process an ATP message through LLM
   */
  async processATP(
    atpMessage: any,
    model?: string,
    agentId?: string
  ): Promise<ChatResponse> {
    // Build system prompt based on ATP header
    const systemPrompt = this.buildATPSystemPrompt(atpMessage, agentId);

    // Extract content from ATP message
    const userContent = typeof atpMessage.payload === 'string'
      ? atpMessage.payload
      : JSON.stringify(atpMessage.payload);

    const messages: Message[] = [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userContent }
    ];

    return this.chat(messages, model, {
      temperature: this.getTemperatureForMode(atpMessage.header?.mode),
      maxTokens: this.getMaxTokensForActionType(atpMessage.header?.actionType)
    });
  }

  /**
   * Get usage statistics
   */
  async getUsage(filters: {
    startDate?: string;
    endDate?: string;
    provider?: string;
  } = {}): Promise<UsageStats> {
    let filtered = [...usageLog];

    if (filters.startDate) {
      const start = new Date(filters.startDate);
      filtered = filtered.filter(log => new Date(log.timestamp) >= start);
    }

    if (filters.endDate) {
      const end = new Date(filters.endDate);
      filtered = filtered.filter(log => new Date(log.timestamp) <= end);
    }

    if (filters.provider) {
      filtered = filtered.filter(log => log.provider === filters.provider);
    }

    // Aggregate stats
    const byModel: Record<string, { requests: number; tokens: number }> = {};
    const byDay: Record<string, { requests: number; tokens: number }> = {};
    let totalPrompt = 0;
    let totalCompletion = 0;
    let totalCost = 0;

    for (const log of filtered) {
      const totalTokens = log.promptTokens + log.completionTokens;
      totalPrompt += log.promptTokens;
      totalCompletion += log.completionTokens;

      // By model
      if (!byModel[log.model]) {
        byModel[log.model] = { requests: 0, tokens: 0 };
      }
      byModel[log.model].requests++;
      byModel[log.model].tokens += totalTokens;

      // By day
      const day = log.timestamp.split('T')[0];
      if (!byDay[day]) {
        byDay[day] = { requests: 0, tokens: 0 };
      }
      byDay[day].requests++;
      byDay[day].tokens += totalTokens;

      // Calculate cost
      const modelInfo = MODELS.find(m => m.id === log.model);
      if (modelInfo) {
        totalCost += (log.promptTokens / 1000) * modelInfo.inputCostPer1k;
        totalCost += (log.completionTokens / 1000) * modelInfo.outputCostPer1k;
      }
    }

    return {
      totalRequests: filtered.length,
      totalTokens: totalPrompt + totalCompletion,
      promptTokens: totalPrompt,
      completionTokens: totalCompletion,
      estimatedCost: Math.round(totalCost * 10000) / 10000,
      byModel,
      byDay
    };
  }

  // Private helper methods

  private async simulateChat(
    messages: Message[],
    model: string,
    options: ChatOptions
  ): Promise<ChatResponse> {
    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 100));

    // Generate mock response based on the last user message
    const lastUserMessage = [...messages].reverse().find(m => m.role === 'user');
    const content = this.generateMockResponse(lastUserMessage?.content || '', model);

    // Estimate tokens (rough approximation)
    const promptText = messages.map(m => m.content).join(' ');
    const promptTokens = Math.ceil(promptText.split(/\s+/).length * 1.3);
    const completionTokens = Math.ceil(content.split(/\s+/).length * 1.3);

    return {
      id: `chat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      model,
      content,
      role: 'assistant',
      finishReason: 'stop',
      usage: {
        promptTokens,
        completionTokens,
        totalTokens: promptTokens + completionTokens
      },
      createdAt: new Date().toISOString()
    };
  }

  private generateMockResponse(input: string, model: string): string {
    // Generate contextual mock response
    const modelName = MODELS.find(m => m.id === model)?.name || model;

    if (input.toLowerCase().includes('hello') || input.toLowerCase().includes('hi')) {
      return `Hello! I'm ${modelName}, ready to assist you with the Artemis City system. How can I help you today?`;
    }

    if (input.toLowerCase().includes('help')) {
      return `I can help you with various tasks in Artemis City:\n- Agent management and coordination\n- Memory and vault operations\n- ATP message processing\n- Trust management and Hebbian learning\nWhat would you like to explore?`;
    }

    if (input.toLowerCase().includes('atp') || input.toLowerCase().includes('artemis')) {
      return `The Artemis Transmission Protocol (ATP) provides structured communication between agents in Artemis City. Each message contains a header (Mode, Context, Priority, ActionType, TargetZone) and a payload. This ensures consistent, traceable agent interactions.`;
    }

    return `[${modelName}] Processed your request: "${input.substring(0, 50)}${input.length > 50 ? '...' : ''}". In a production environment, this would be a real AI response. The Artemis City API is configured and ready to connect to actual LLM providers.`;
  }

  private buildATPSystemPrompt(atpMessage: any, agentId?: string): string {
    const header = atpMessage.header || {};
    const mode = header.mode || 'QUERY';
    const context = header.context || 'General inquiry';
    const priority = header.priority || 'MEDIUM';
    const actionType = header.actionType || 'READ';
    const targetZone = header.targetZone || 'system';

    return `You are an AI assistant operating within the Artemis City agent ecosystem.

## ATP Context
- Mode: ${mode}
- Context: ${context}
- Priority: ${priority}
- Action Type: ${actionType}
- Target Zone: ${targetZone}
${agentId ? `- Requesting Agent: ${agentId}` : ''}

## Response Guidelines
Based on the ATP mode "${mode}":
${mode === 'RESEARCH' ? '- Focus on gathering and synthesizing information\n- Cite sources when available\n- Be thorough but concise' : ''}
${mode === 'EXECUTE' ? '- Provide actionable steps\n- Be precise and direct\n- Include any necessary prerequisites' : ''}
${mode === 'REPORT' ? '- Structure information clearly\n- Include relevant metrics\n- Summarize key findings' : ''}
${mode === 'DELEGATE' ? '- Identify the appropriate sub-tasks\n- Suggest which agents should handle each task\n- Coordinate the overall workflow' : ''}
${mode === 'QUERY' ? '- Answer the question directly\n- Provide relevant context\n- Suggest follow-up actions if appropriate' : ''}

Based on action type "${actionType}":
${actionType === 'CREATE' ? '- Generate new content or structures' : ''}
${actionType === 'READ' ? '- Retrieve and present information' : ''}
${actionType === 'UPDATE' ? '- Modify existing content appropriately' : ''}
${actionType === 'DELETE' ? '- Confirm deletion requirements carefully' : ''}
${actionType === 'SEARCH' ? '- Find relevant matches and rank by relevance' : ''}
${actionType === 'ANALYZE' ? '- Provide deep analysis with insights' : ''}
${actionType === 'SYNC' ? '- Ensure consistency across systems' : ''}
${actionType === 'NOTIFY' ? '- Format for clear notification delivery' : ''}

Respond appropriately for the given context and priority level.`;
  }

  private getTemperatureForMode(mode?: string): number {
    const temps: Record<string, number> = {
      'RESEARCH': 0.3,
      'EXECUTE': 0.1,
      'REPORT': 0.2,
      'DELEGATE': 0.4,
      'QUERY': 0.5
    };
    return temps[mode || 'QUERY'] || 0.5;
  }

  private getMaxTokensForActionType(actionType?: string): number {
    const maxTokens: Record<string, number> = {
      'CREATE': 2048,
      'READ': 1024,
      'UPDATE': 1024,
      'DELETE': 256,
      'SEARCH': 512,
      'ANALYZE': 2048,
      'SYNC': 512,
      'NOTIFY': 256
    };
    return maxTokens[actionType || 'READ'] || 1024;
  }

  private logUsage(provider: string, model: string, promptTokens: number, completionTokens: number): void {
    usageLog.push({
      timestamp: new Date().toISOString(),
      provider,
      model,
      promptTokens,
      completionTokens
    });

    // Keep only last 10000 entries
    if (usageLog.length > 10000) {
      usageLog.splice(0, usageLog.length - 10000);
    }
  }
}
