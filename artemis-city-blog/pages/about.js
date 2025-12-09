import Head from 'next/head';

export default function About() {
  return (
    <>
      <Head>
        <title>About Artemis City - The Kernel for AI Agents</title>
        <meta name="description" content="Learn about Artemis City's mission to provide a governance layer for production-ready AI agent systems." />
      </Head>

      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-16 animate-fade-in-up">
          <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent mb-6">
            About Artemis City
          </h1>
          <p className="text-xl text-secondary-600 max-w-2xl mx-auto">
            The Kernel for AI Agents
          </p>
        </div>

        <div className="space-y-12">
          <section className="themed-surface rounded-2xl shadow-soft p-8 md:p-12 animate-fade-in-up">
            <h2 className="text-3xl font-bold text-secondary-900 mb-6">Our Philosophy</h2>
            <p className="text-lg text-secondary-700 leading-relaxed mb-4">
              The name Artemis City came from an AI-human collaboration. When asked what to call an agentic operating system, ChatGPT chose &quot;Artemis&quot;—Greek goddess of the hunt, protector, and guide.
            </p>
            <p className="text-lg text-secondary-700 leading-relaxed">
              That moment crystallized our philosophy: <strong>AI and humans collaborate, but humans govern.</strong> We believe that for AI agents to be truly production-ready, they require a deterministic, kernel-driven governance layer, not just hope-driven LLM wrappers.
            </p>
          </section>

          <section className="gradient-surface rounded-2xl shadow-soft p-8 md:p-12 animate-fade-in-up">
            <h2 className="text-3xl font-bold text-secondary-900 mb-6">What We Build</h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="themed-surface rounded-xl p-6 shadow-soft">
                <div className="text-primary-500 text-4xl mb-3">🎯</div>
                <h3 className="text-xl font-semibold text-secondary-900 mb-3">Kernel-Driven Architecture</h3>
                <p className="text-secondary-700">
                  We provide a central kernel that manages routing, state, and governance, ensuring deterministic and reliable multi-agent orchestration.
                </p>
              </div>
              <div className="themed-surface rounded-xl p-6 shadow-soft">
                <div className="text-primary-500 text-4xl mb-3">💾</div>
                <h3 className="text-xl font-semibold text-secondary-900 mb-3">User-Owned Memory</h3>
                <p className="text-secondary-700">
                  Our memory bus gives users full control over their data with Supabase and Obsidian integration, avoiding vendor lock-in.
                </p>
              </div>
              <div className="themed-surface rounded-xl p-6 shadow-soft">
                <div className="text-primary-500 text-4xl mb-3">🛡️</div>
                <h3 className="text-xl font-semibold text-secondary-900 mb-3">Production-Ready Governance</h3>
                <p className="text-secondary-700">
                  We build for reliability with governance primitives like audit trails, tool permissions, and a trust-decay model.
                </p>
              </div>
              <div className="themed-surface rounded-xl p-6 shadow-soft">
                <div className="text-primary-500 text-4xl mb-3">🔌</div>
                <h3 className="text-xl font-semibold text-secondary-900 mb-3">Extensible Plugin Ecosystem</h3>
                <p className="text-secondary-700">
                  Our system is extensible via plugins, with day-one support for major AI models and tools.
                </p>
              </div>
            </div>
          </section>

          <section className="themed-surface rounded-2xl shadow-soft p-8 md:p-12 animate-fade-in-up">
            <h2 className="text-3xl font-bold text-secondary-900 mb-6">Our Principles</h2>
            <ul className="space-y-4 text-lg text-secondary-700">
              <li className="flex items-start">
                <span className="text-primary-500 mr-3 text-2xl">✓</span>
                <span><strong className="text-secondary-900">Determinism:</strong> The kernel decides, not the LLM. Predictable, reliable orchestration.</span>
              </li>
              <li className="flex items-start">
                <span className="text-primary-500 mr-3 text-2xl">✓</span>
                <span><strong className="text-secondary-900">User-Ownership:</strong> Persistent, user-owned memory. No vendor lock-in.</span>
              </li>
              <li className="flex items-start">
                <span className="text-primary-500 mr-3 text-2xl">✓</span>
                <span><strong className="text-secondary-900">Governance:</strong> Production-ready primitives for accountability and control.</span>
              </li>
              <li className="flex items-start">
                <span className="text-primary-500 mr-3 text-2xl">✓</span>
                <span><strong className="text-secondary-900">Openness:</strong> An extensible, open-source kernel with a thriving plugin ecosystem.</span>
              </li>
            </ul>
          </section>
        </div>
      </div>
    </>
  );
}
