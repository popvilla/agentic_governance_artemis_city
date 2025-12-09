import Link from 'next/link';

export default function PostCard({ post }) {
  return (
    <Link href={`/blog/${post.slug}`}>
      <div className="group themed-surface rounded-2xl shadow-soft hover:shadow-xl transition-all duration-300 overflow-hidden flex flex-col h-full border hover:border-primary-200 hover:-translate-y-1">
        <div className="accent-bar h-2 transition-all duration-300 group-hover:brightness-110" />

        <div className="p-6 flex-grow flex flex-col">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-xs font-semibold text-primary-600 bg-primary-50 px-3 py-1 rounded-full">
              {post.frontmatter.author || 'Artemis City'}
            </span>
            <span className="text-xs text-secondary-400">•</span>
            <time className="text-xs text-secondary-500">
              {new Date(post.frontmatter.date).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
              })}
            </time>
          </div>

          <h2 className="text-2xl font-bold text-secondary-900 mb-3 leading-tight group-hover:text-primary-600 transition-colors">
            {post.frontmatter.title}
          </h2>

          <p className="text-secondary-600 flex-grow mb-4 line-clamp-3">
            {post.frontmatter.description || 'No description available.'}
          </p>

          <div className="flex items-center text-primary-600 font-semibold group-hover:gap-2 transition-all">
            <span>Read More</span>
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </div>
        </div>
      </div>
    </Link>
  );
}
