import React, { useState, useEffect, useCallback } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from "recharts";
import { Zap, Shield, Send, Play, ChevronRight, Terminal, Users, Brain, Package, Settings, CheckCircle, AlertTriangle, Clock, Sparkles } from "lucide-react";

// ============================================================================
// ATP INTERACTIVE PROTOTYPE - Artemis Transmission Protocol
// A demo for stakeholders, developers, and live message building
// ============================================================================

// ATP Constants
const ATP_MODES = ["Build", "Review", "Organize", "Capture", "Synthesize", "Commit"];
const ATP_PRIORITIES = ["Critical", "High", "Normal", "Low"];
const ATP_ACTION_TYPES = ["Summarize", "Scaffold", "Execute", "Reflect"];

// Agent Definitions
const AGENTS = {
  artemis: {
    name: "Artemis",
    role: "Governance Agent",
    icon: Shield,
    color: "#00ffcc",
    keywords: ["artemis", "governance", "policy", "audit", "dispute", "review"],
    description: "System overseer, governance, dispute resolution"
  },
  copilot: {
    name: "Copilot",
    role: "Elastic Augmentation",
    icon: Brain,
    color: "#ff6b6b",
    keywords: ["help", "assist", "explain", "augment", "clarify", "suggest"],
    description: "Real-time assistant, contextual information"
  },
  packrat: {
    name: "Pack Rat",
    role: "Secure Courier",
    icon: Package,
    color: "#ffd93d",
    keywords: ["transfer", "send", "receive", "courier", "data", "secure"],
    description: "Secure data transfer between components"
  },
  daemon: {
    name: "Codex Daemon",
    role: "System Anchor",
    icon: Settings,
    color: "#6c5ce7",
    keywords: ["memory", "system", "daemon", "config", "status", "health"],
    description: "System status, memory interface, config"
  }
};

// Trust Decay Simulation Data Generator
const generateTrustData = (initialTrust = 100, events = []) => {
  const data = [];
  let trust = initialTrust;
  const decayRate = 0.02;

  for (let day = 0; day <= 30; day++) {
    // Natural decay
    trust = Math.max(0, trust * (1 - decayRate));

    // Apply events
    const event = events.find(e => e.day === day);
    if (event) {
      trust = Math.min(100, Math.max(0, trust + event.impact));
    }

    data.push({
      day,
      trust: Math.round(trust * 10) / 10,
      event: event?.label || null
    });
  }
  return data;
};

// ============================================================================
// COMPONENTS
// ============================================================================

// Animated Background
const CyberBackground = () => (
  <div className="fixed inset-0 overflow-hidden pointer-events-none">
    <div className="absolute inset-0 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950" />
    <div className="absolute inset-0 opacity-30">
      {[...Array(20)].map((_, i) => (
        <div
          key={i}
          className="absolute h-px bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent"
          style={{
            top: `${(i * 5) + Math.random() * 5}%`,
            left: 0,
            right: 0,
            animation: `pulse ${2 + Math.random() * 3}s ease-in-out infinite`,
            animationDelay: `${Math.random() * 2}s`
          }}
        />
      ))}
    </div>
    <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl" />
    <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl" />
  </div>
);

// Glowing Card Component
const GlowCard = ({ children, className = "", glowColor = "cyan" }) => {
  const glowClasses = {
    cyan: "shadow-cyan-500/20 hover:shadow-cyan-500/40 border-cyan-500/30",
    purple: "shadow-purple-500/20 hover:shadow-purple-500/40 border-purple-500/30",
    green: "shadow-green-500/20 hover:shadow-green-500/40 border-green-500/30",
    amber: "shadow-amber-500/20 hover:shadow-amber-500/40 border-amber-500/30"
  };

  return (
    <div className={`bg-slate-900/80 backdrop-blur-xl border rounded-lg shadow-lg transition-all duration-300 ${glowClasses[glowColor]} ${className}`}>
      {children}
    </div>
  );
};

// Navigation Tabs
const NavTabs = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: "builder", label: "Message Builder", icon: Terminal },
    { id: "routing", label: "Agent Routing", icon: Users },
    { id: "trust", label: "Trust Decay", icon: Shield },
    { id: "workflow", label: "Full Workflow", icon: Play }
  ];

  return (
    <div className="flex gap-2 mb-8 flex-wrap">
      {tabs.map(tab => {
        const Icon = tab.icon;
        return (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-mono text-sm transition-all duration-300 ${
              activeTab === tab.id
                ? "bg-cyan-500/20 text-cyan-400 border border-cyan-500/50"
                : "bg-slate-800/50 text-slate-400 border border-slate-700/50 hover:border-slate-600"
            }`}
          >
            <Icon size={16} />
            {tab.label}
          </button>
        );
      })}
    </div>
  );
};

// ATP Tag Selector
const TagSelector = ({ label, options, value, onChange, color = "cyan" }) => {
  const colorClasses = {
    cyan: "border-cyan-500/50 text-cyan-400",
    purple: "border-purple-500/50 text-purple-400",
    green: "border-green-500/50 text-green-400",
    amber: "border-amber-500/50 text-amber-400"
  };

  return (
    <div className="space-y-2">
      <label className="text-xs font-mono text-slate-500 uppercase tracking-wider">{label}</label>
      <div className="flex flex-wrap gap-2">
        {options.map(opt => (
          <button
            key={opt}
            onClick={() => onChange(opt)}
            className={`px-3 py-1.5 rounded text-xs font-mono transition-all duration-200 ${
              value === opt
                ? `${colorClasses[color]} bg-slate-800 border`
                : "text-slate-500 bg-slate-800/50 border border-slate-700/50 hover:border-slate-600"
            }`}
          >
            {opt}
          </button>
        ))}
      </div>
    </div>
  );
};

// Message Builder Section
const MessageBuilder = ({ message, setMessage, onSend }) => {
  const [isValid, setIsValid] = useState(false);

  useEffect(() => {
    // Validate: needs at least Mode and some context
    setIsValid(message.mode && message.context.trim().length > 0);
  }, [message]);

  const generatedMessage = `#Mode: ${message.mode || "___"} #Context: ${message.context || "___"} #Priority: ${message.priority || "Normal"} #ActionType: ${message.actionType || "Execute"}${message.targetZone ? ` #TargetZone: ${message.targetZone}` : ""}${message.specialNotes ? ` #SpecialNotes: ${message.specialNotes}` : ""}`;

  return (
    <GlowCard className="p-6" glowColor="cyan">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-cyan-500/10">
          <Terminal className="text-cyan-400" size={20} />
        </div>
        <div>
          <h2 className="text-lg font-semibold text-white">ATP Message Builder</h2>
          <p className="text-xs text-slate-500">Compose structured commands for the Artemis system</p>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-5">
          <TagSelector
            label="#Mode"
            options={ATP_MODES}
            value={message.mode}
            onChange={v => setMessage({...message, mode: v})}
            color="cyan"
          />

          <TagSelector
            label="#Priority"
            options={ATP_PRIORITIES}
            value={message.priority}
            onChange={v => setMessage({...message, priority: v})}
            color="amber"
          />

          <TagSelector
            label="#ActionType"
            options={ATP_ACTION_TYPES}
            value={message.actionType}
            onChange={v => setMessage({...message, actionType: v})}
            color="purple"
          />

          <div className="space-y-2">
            <label className="text-xs font-mono text-slate-500 uppercase tracking-wider">#Context</label>
            <input
              type="text"
              value={message.context}
              onChange={e => setMessage({...message, context: e.target.value})}
              placeholder="Brief mission goal or purpose..."
              className="w-full px-4 py-2 rounded-lg bg-slate-800/50 border border-slate-700/50 text-white placeholder-slate-600 focus:border-cyan-500/50 focus:outline-none font-mono text-sm"
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-mono text-slate-500 uppercase tracking-wider">#TargetZone (optional)</label>
            <input
              type="text"
              value={message.targetZone}
              onChange={e => setMessage({...message, targetZone: e.target.value})}
              placeholder="e.g., /agents/artemis/"
              className="w-full px-4 py-2 rounded-lg bg-slate-800/50 border border-slate-700/50 text-white placeholder-slate-600 focus:border-cyan-500/50 focus:outline-none font-mono text-sm"
            />
          </div>
        </div>

        <div className="space-y-4">
          <div className="space-y-2">
            <label className="text-xs font-mono text-slate-500 uppercase tracking-wider">Generated ATP Message</label>
            <div className="p-4 rounded-lg bg-slate-950 border border-slate-700/50 font-mono text-sm min-h-[120px]">
              <span className="text-cyan-400">#Mode:</span> <span className="text-white">{message.mode || "___"}</span>{" "}
              <span className="text-green-400">#Context:</span> <span className="text-white">{message.context || "___"}</span>{" "}
              <span className="text-amber-400">#Priority:</span> <span className="text-white">{message.priority || "Normal"}</span>{" "}
              <span className="text-purple-400">#ActionType:</span> <span className="text-white">{message.actionType || "Execute"}</span>
              {message.targetZone && (
                <><br/><span className="text-pink-400">#TargetZone:</span> <span className="text-white">{message.targetZone}</span></>
              )}
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className={`flex items-center gap-2 px-3 py-1.5 rounded text-xs font-mono ${
              isValid ? "bg-green-500/10 text-green-400" : "bg-amber-500/10 text-amber-400"
            }`}>
              {isValid ? <CheckCircle size={14} /> : <AlertTriangle size={14} />}
              {isValid ? "Valid ATP Message" : "Incomplete Message"}
            </div>
          </div>

          <button
            onClick={() => isValid && onSend(message)}
            disabled={!isValid}
            className={`w-full flex items-center justify-center gap-2 px-6 py-3 rounded-lg font-mono text-sm transition-all duration-300 ${
              isValid
                ? "bg-gradient-to-r from-cyan-500 to-cyan-600 text-white hover:from-cyan-400 hover:to-cyan-500 shadow-lg shadow-cyan-500/25"
                : "bg-slate-800 text-slate-600 cursor-not-allowed"
            }`}
          >
            <Send size={16} />
            Send to Artemis System
          </button>
        </div>
      </div>
    </GlowCard>
  );
};

// Agent Routing Visualization
const AgentRouting = ({ message }) => {
  const [routedAgent, setRoutedAgent] = useState(null);
  const [isRouting, setIsRouting] = useState(false);

  const simulateRouting = useCallback(() => {
    setIsRouting(true);
    setRoutedAgent(null);

    // Simulate routing delay
    setTimeout(() => {
      // Find matching agent based on context keywords
      const contextLower = message.context.toLowerCase();
      let matched = null;

      for (const [key, agent] of Object.entries(AGENTS)) {
        if (agent.keywords.some(kw => contextLower.includes(kw))) {
          matched = key;
          break;
        }
      }

      // Default to artemis for governance/review modes
      if (!matched && (message.mode === "Review" || message.mode === "Commit")) {
        matched = "artemis";
      }

      // Default to copilot for general tasks
      if (!matched) {
        matched = "copilot";
      }

      setRoutedAgent(matched);
      setIsRouting(false);
    }, 1500);
  }, [message]);

  return (
    <GlowCard className="p-6" glowColor="purple">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-purple-500/10">
          <Users className="text-purple-400" size={20} />
        </div>
        <div>
          <h2 className="text-lg font-semibold text-white">Agent Routing Simulation</h2>
          <p className="text-xs text-slate-500">See how ATP messages route to specialized agents</p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-6">
        {Object.entries(AGENTS).map(([key, agent]) => {
          const Icon = agent.icon;
          const isActive = routedAgent === key;
          return (
            <div
              key={key}
              className={`p-4 rounded-lg border transition-all duration-500 ${
                isActive
                  ? "border-2 scale-105 shadow-lg"
                  : "border-slate-700/50 bg-slate-800/30"
              }`}
              style={{
                borderColor: isActive ? agent.color : undefined,
                boxShadow: isActive ? `0 0 30px ${agent.color}40` : undefined
              }}
            >
              <div className="flex items-center gap-3 mb-2">
                <div
                  className="p-2 rounded-lg"
                  style={{ backgroundColor: `${agent.color}20` }}
                >
                  <Icon size={18} style={{ color: agent.color }} />
                </div>
                <div>
                  <div className="font-semibold text-white text-sm">{agent.name}</div>
                  <div className="text-xs text-slate-500">{agent.role}</div>
                </div>
              </div>
              <p className="text-xs text-slate-400 mb-2">{agent.description}</p>
              <div className="flex flex-wrap gap-1">
                {agent.keywords.slice(0, 3).map(kw => (
                  <span key={kw} className="px-1.5 py-0.5 rounded text-[10px] bg-slate-700/50 text-slate-400 font-mono">
                    {kw}
                  </span>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      <div className="flex items-center gap-4">
        <button
          onClick={simulateRouting}
          disabled={isRouting || !message.context}
          className={`flex items-center gap-2 px-6 py-3 rounded-lg font-mono text-sm transition-all duration-300 ${
            isRouting || !message.context
              ? "bg-slate-800 text-slate-600 cursor-not-allowed"
              : "bg-gradient-to-r from-purple-500 to-purple-600 text-white hover:from-purple-400 hover:to-purple-500 shadow-lg shadow-purple-500/25"
          }`}
        >
          {isRouting ? (
            <>
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Routing...
            </>
          ) : (
            <>
              <Zap size={16} />
              Simulate Routing
            </>
          )}
        </button>

        {routedAgent && (
          <div className="flex items-center gap-2 text-sm">
            <ChevronRight className="text-slate-600" size={16} />
            <span className="text-slate-400">Routed to:</span>
            <span className="font-semibold" style={{ color: AGENTS[routedAgent].color }}>
              {AGENTS[routedAgent].name}
            </span>
          </div>
        )}
      </div>
    </GlowCard>
  );
};

// Trust Decay Visualization
const TrustDecay = () => {
  const [scenario, setScenario] = useState("default");

  const scenarios = {
    default: {
      label: "Natural Decay",
      initial: 100,
      events: []
    },
    positive: {
      label: "Positive Reinforcement",
      initial: 60,
      events: [
        { day: 5, impact: 15, label: "Successful task" },
        { day: 12, impact: 20, label: "Protocol adherence" },
        { day: 20, impact: 10, label: "Validation passed" }
      ]
    },
    negative: {
      label: "Trust Violation",
      initial: 90,
      events: [
        { day: 8, impact: -25, label: "Policy violation" },
        { day: 15, impact: -15, label: "Inconsistency detected" }
      ]
    },
    recovery: {
      label: "Recovery Pattern",
      initial: 40,
      events: [
        { day: 3, impact: 10, label: "Corrective action" },
        { day: 8, impact: 15, label: "Audit passed" },
        { day: 15, impact: 20, label: "Sustained compliance" },
        { day: 22, impact: 10, label: "Trust restored" }
      ]
    }
  };

  const data = generateTrustData(scenarios[scenario].initial, scenarios[scenario].events);

  const getTrustLevel = (trust) => {
    if (trust >= 80) return { label: "High Trust", color: "#00ffcc" };
    if (trust >= 50) return { label: "Moderate Trust", color: "#ffd93d" };
    if (trust >= 25) return { label: "Low Trust", color: "#ff9f43" };
    return { label: "Critical", color: "#ff6b6b" };
  };

  const currentTrust = data[data.length - 1].trust;
  const trustLevel = getTrustLevel(currentTrust);

  return (
    <GlowCard className="p-6" glowColor="green">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-green-500/10">
            <Shield className="text-green-400" size={20} />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-white">Trust Decay Model</h2>
            <p className="text-xs text-slate-500">Dynamic trust evaluation over time</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500 font-mono">Final Score:</span>
          <span className="text-2xl font-bold" style={{ color: trustLevel.color }}>
            {currentTrust}
          </span>
          <span className="px-2 py-1 rounded text-xs font-mono" style={{ backgroundColor: `${trustLevel.color}20`, color: trustLevel.color }}>
            {trustLevel.label}
          </span>
        </div>
      </div>

      <div className="flex gap-2 mb-6 flex-wrap">
        {Object.entries(scenarios).map(([key, s]) => (
          <button
            key={key}
            onClick={() => setScenario(key)}
            className={`px-3 py-1.5 rounded text-xs font-mono transition-all duration-200 ${
              scenario === key
                ? "bg-green-500/20 text-green-400 border border-green-500/50"
                : "text-slate-500 bg-slate-800/50 border border-slate-700/50 hover:border-slate-600"
            }`}
          >
            {s.label}
          </button>
        ))}
      </div>

      <div className="h-64 mb-4">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <defs>
              <linearGradient id="trustGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#00ffcc" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#00ffcc" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis
              dataKey="day"
              stroke="#64748b"
              fontSize={10}
              tickLine={false}
              label={{ value: 'Days', position: 'bottom', fill: '#64748b', fontSize: 10 }}
            />
            <YAxis
              stroke="#64748b"
              fontSize={10}
              tickLine={false}
              domain={[0, 100]}
              label={{ value: 'Trust Score', angle: -90, position: 'insideLeft', fill: '#64748b', fontSize: 10 }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #334155',
                borderRadius: '8px',
                fontSize: '12px'
              }}
              formatter={(value, name) => [`${value}%`, 'Trust Score']}
              labelFormatter={(label) => `Day ${label}`}
            />
            <Area
              type="monotone"
              dataKey="trust"
              stroke="#00ffcc"
              strokeWidth={2}
              fill="url(#trustGradient)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {scenarios[scenario].events.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {scenarios[scenario].events.map((event, i) => (
            <div key={i} className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800/50 text-xs font-mono">
              <Clock size={12} className="text-slate-500" />
              <span className="text-slate-400">Day {event.day}:</span>
              <span className={event.impact > 0 ? "text-green-400" : "text-red-400"}>
                {event.impact > 0 ? "+" : ""}{event.impact}
              </span>
              <span className="text-slate-500">{event.label}</span>
            </div>
          ))}
        </div>
      )}
    </GlowCard>
  );
};

// Full Workflow Demo
const WorkflowDemo = () => {
  const [step, setStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  const steps = [
    {
      title: "1. User Composes ATP Message",
      description: "Developer structures their intent using ATP signal tags",
      code: '#Mode: Build #Context: Add dark mode toggle #Priority: High #ActionType: Execute',
      highlight: "cyan"
    },
    {
      title: "2. ATP Parser Validates",
      description: "System parses and validates the structured message",
      code: `{
  mode: "Build",
  context: "Add dark mode toggle",
  priority: "High",
  actionType: "Execute",
  isValid: true
}`,
      highlight: "green"
    },
    {
      title: "3. Agent Router Matches",
      description: "Keywords route to the appropriate agent (Copilot)",
      code: `Router.match("dark mode toggle")
→ Keywords: ["help", "augment", "clarify"]
→ Matched: Copilot (Elastic Augmentation)`,
      highlight: "purple"
    },
    {
      title: "4. Agent Processes Request",
      description: "Copilot agent executes within defined scope",
      code: `Copilot.handle({
  action: "scaffold",
  target: "dark_mode_toggle",
  context: session.current
})`,
      highlight: "amber"
    },
    {
      title: "5. Response with Trust Update",
      description: "System returns result and updates trust score",
      code: `{
  status: "success",
  output: "Dark mode component scaffolded",
  trustDelta: +5,
  auditLog: "copilot_action_12847"
}`,
      highlight: "cyan"
    }
  ];

  useEffect(() => {
    if (isPlaying) {
      const timer = setTimeout(() => {
        if (step < steps.length - 1) {
          setStep(step + 1);
        } else {
          setIsPlaying(false);
        }
      }, 2500);
      return () => clearTimeout(timer);
    }
  }, [isPlaying, step]);

  const highlightColors = {
    cyan: "border-cyan-500/50 bg-cyan-500/5",
    green: "border-green-500/50 bg-green-500/5",
    purple: "border-purple-500/50 bg-purple-500/5",
    amber: "border-amber-500/50 bg-amber-500/5"
  };

  return (
    <GlowCard className="p-6" glowColor="amber">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-amber-500/10">
            <Play className="text-amber-400" size={20} />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-white">Full Workflow Demo</h2>
            <p className="text-xs text-slate-500">End-to-end ATP message lifecycle</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => { setStep(0); setIsPlaying(true); }}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-amber-500 to-amber-600 text-white font-mono text-sm hover:from-amber-400 hover:to-amber-500 shadow-lg shadow-amber-500/25"
          >
            <Play size={14} />
            {isPlaying ? "Playing..." : "Play Demo"}
          </button>
        </div>
      </div>

      {/* Progress bar */}
      <div className="flex gap-2 mb-6">
        {steps.map((_, i) => (
          <div
            key={i}
            className={`h-1 flex-1 rounded-full transition-all duration-300 ${
              i <= step ? "bg-amber-500" : "bg-slate-700"
            }`}
          />
        ))}
      </div>

      {/* Current Step */}
      <div className={`p-6 rounded-lg border-2 transition-all duration-500 ${highlightColors[steps[step].highlight]}`}>
        <div className="flex items-center gap-2 mb-3">
          <Sparkles className="text-amber-400" size={16} />
          <h3 className="font-semibold text-white">{steps[step].title}</h3>
        </div>
        <p className="text-sm text-slate-400 mb-4">{steps[step].description}</p>
        <pre className="p-4 rounded-lg bg-slate-950 border border-slate-700/50 font-mono text-sm text-slate-300 overflow-x-auto">
          {steps[step].code}
        </pre>
      </div>

      {/* Step Navigation */}
      <div className="flex justify-between mt-6">
        <button
          onClick={() => setStep(Math.max(0, step - 1))}
          disabled={step === 0}
          className={`px-4 py-2 rounded-lg font-mono text-sm transition-all ${
            step === 0
              ? "text-slate-600 cursor-not-allowed"
              : "text-slate-400 hover:text-white hover:bg-slate-800"
          }`}
        >
          ← Previous
        </button>
        <button
          onClick={() => setStep(Math.min(steps.length - 1, step + 1))}
          disabled={step === steps.length - 1}
          className={`px-4 py-2 rounded-lg font-mono text-sm transition-all ${
            step === steps.length - 1
              ? "text-slate-600 cursor-not-allowed"
              : "text-slate-400 hover:text-white hover:bg-slate-800"
          }`}
        >
          Next →
        </button>
      </div>
    </GlowCard>
  );
};

// Hero Section
const Hero = () => (
  <div className="text-center mb-12">
    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cyan-500/10 border border-cyan-500/30 mb-6">
      <Zap className="text-cyan-400" size={16} />
      <span className="text-cyan-400 font-mono text-sm">Artemis City v0.1.0</span>
    </div>
    <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
      Artemis Transmission
      <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400"> Protocol</span>
    </h1>
    <p className="text-lg text-slate-400 max-w-2xl mx-auto">
      Structured communication for agentic systems. Balance trust, entropy, and collaboration
      to achieve <span className="text-cyan-400 font-semibold">net good over noise</span>.
    </p>
  </div>
);

// Main App Component
export default function ATPPrototype() {
  const [activeTab, setActiveTab] = useState("builder");
  const [message, setMessage] = useState({
    mode: "Build",
    context: "",
    priority: "Normal",
    actionType: "Execute",
    targetZone: "",
    specialNotes: ""
  });

  const handleSend = (msg) => {
    console.log("ATP Message sent:", msg);
    setActiveTab("routing");
  };

  return (
    <div className="min-h-screen relative">
      <CyberBackground />

      <div className="relative z-10 max-w-6xl mx-auto px-4 py-12">
        <Hero />

        <NavTabs activeTab={activeTab} setActiveTab={setActiveTab} />

        <div className="space-y-6">
          {activeTab === "builder" && (
            <MessageBuilder message={message} setMessage={setMessage} onSend={handleSend} />
          )}

          {activeTab === "routing" && (
            <AgentRouting message={message} />
          )}

          {activeTab === "trust" && (
            <TrustDecay />
          )}

          {activeTab === "workflow" && (
            <WorkflowDemo />
          )}
        </div>

        {/* Footer */}
        <div className="mt-12 text-center text-xs text-slate-600 font-mono">
          <p>Authored by Prinston (Apollo) Palmer • Systems Architect</p>
          <p>With Claude (Anthropic) • AI Development Partner</p>
        </div>
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 0.3; }
          50% { opacity: 0.6; }
        }
      `}</style>
    </div>
  );
}
