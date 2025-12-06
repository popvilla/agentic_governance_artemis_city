import Head from 'next/head';
import { getSortedPostsData } from '../lib/post';
import PostCard from '../components/PostCard';

export async function getStaticProps() {
  const allPostsData = getSortedPostsData();
  return {
    props: {
      allPostsData,
    },
  };
}

export default function Blog({ allPostsData }) {
  return (
    <>
      <Head>
        <title>Blog | Artemis City</title>
        <meta name="description" content="Read the latest updates, insights, and stories from Artemis City." />
      </Head>

      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12 animate-fade-in-up">
          <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent mb-6">
            Blog & Updates
          </h1>
          <p className="text-xl text-secondary-600 max-w-2xl mx-auto">
            Stay informed with the latest news, insights, and stories from Artemis City
          </p>
        </div>

        {allPostsData.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 animate-fade-in">
            {allPostsData.map(({ slug, frontmatter }) => (
              <PostCard key={slug} post={{ slug, frontmatter }} />
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">📝</div>
            <h2 className="text-2xl font-semibold text-secondary-700 mb-2">No posts yet</h2>
            <p className="text-secondary-500">Check back soon for updates!</p>
          </div>
        )}
      </div>
    </>
  );
}
