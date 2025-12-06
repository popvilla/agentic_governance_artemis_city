import Head from 'next/head';
import Link from 'next/link';
import { getSortedPostsData } from '../lib/post';
import PostCard from '../components/PostCard';

export async function getStaticProps() {
  const allPostsData = getSortedPostsData();
  return {
    props: {
      allPostsData: allPostsData.slice(0, 6),
    },
  };
}

export default function Home({ allPostsData }) {
  return (
    <>
      <Head>
        <title>Artemis City - The Kernel for AI Agents</title>
        <meta name="description" content="Deterministic, kernel-driven orchestration for multi-agent systems. A governance layer that makes AI agents production-ready." />
      </Head>

      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-500/10 via-transparent to-accent-500/10 -z-10" />
        <div className="text-center py-20 animate-fade-in-up">
          <div className="inline-block mb-6 px-4 py-2 bg-primary-100 text-primary-700 rounded-full text-sm font-semibold">
            The Kernel for AI Agents
          </div>
          <h1 className="text-6xl md:text-7xl font-extrabold mb-6">
            <span className="block text-gradient">Artemis City</span>
          </h1>
          <p className="text-xl md:text-2xl text-secondary-600 max-w-3xl mx-auto mb-10 leading-relaxed">
            Deterministic, kernel-driven orchestration for multi-agent systems. Not another LLM wrapper—a governance layer that makes agents production-ready.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <a href="https://github.com/popvilla/Artemis-City" className="btn-primary">
              Get Started
            </a>
            <Link href="/blog" className="btn-secondary">
              Read the Docs
            </Link>
          </div>
        </div>
      </section>

      <section className="py-16 themed-surface rounded-3xl shadow-soft mb-16 animate-fade-in">
        <div className="grid md:grid-cols-3 gap-8 text-center">
          <div className="p-6">
            <div className="text-5xl mb-4">🎯</div>
            <h3 className="text-xl font-bold text-secondary-900 mb-2">Kernel-Driven Routing</h3>
            <p className="text-secondary-600">
              YAML-defined routing logic. The kernel decides, not the LLM.
            </p>
          </div>
          <div className="p-6">
            <div className="text-5xl mb-4">💾</div>
            <h3 className="text-xl font-bold text-secondary-900 mb-2">Persistent Memory</h3>
            <p className="text-secondary-600">
              User-owned memory layer (Supabase + Obsidian). No vendor lock-in.
            </p>
          </div>
          <div className="p-6">
            <div className="text-5xl mb-4">🛡️</div>
            <h3 className="text-xl font-bold text-secondary-900 mb-2">Governance Primitives</h3>
            <p className="text-secondary-600">
              Audit trails, tool permissions, and a trust-decay model for accountability.
            </p>
          </div>
        </div>
      </section>

      <section id="latest-posts" className="scroll-mt-20">
        <div className="flex justify-between items-center mb-10">
          <h2 className="text-4xl font-bold text-secondary-900">Latest Updates</h2>
          <Link href="/blog" className="text-primary-600 hover:text-primary-700 font-semibold flex items-center gap-2 transition-colors">
            View All Posts
            <span>→</span>
          </Link>
        </div>

        {allPostsData.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 animate-fade-in">
            {allPostsData.map(({ slug, frontmatter }) => (
              <PostCard key={slug} post={{ slug, frontmatter }} />
            ))}
          </div>
        ) : (
          <div className="text-center py-20 themed-surface rounded-2xl shadow-soft">
            <div className="text-6xl mb-4">📝</div>
            <h3 className="text-2xl font-semibold text-secondary-700 mb-2">No posts yet</h3>
            <p className="text-secondary-500">Check back soon for exciting updates!</p>
          </div>
        )}
      </section>
    </>
  );
}
