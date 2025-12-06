import Head from 'next/head';
import { getPostData, getAllPostSlugs } from '../../lib/post';
import { MDXRemote } from 'next-mdx-remote';
import { serialize } from 'next-mdx-remote/serialize';
import MDXComponents from '../../components/MDXComponents';

export async function getStaticPaths() {
  const paths = getAllPostSlugs();
  return {
    paths,
    fallback: false, // Set to true if you want to use incremental static regeneration (ISR)
  };
}

export async function getStaticProps({ params }) {
  const postData = await getPostData(params.slug);
  const mdxSource = await serialize(postData.content, {
    mdxOptions: {
      remarkPlugins: [], // Add remark plugins here if needed, e.g., remark-gfm
      rehypePlugins: [], // Add rehype plugins here if needed
    },
    scope: postData.frontmatter,
  });

  return {
    props: {
      postData: {
        ...postData,
        content: mdxSource,
      },
    },
  };
}

export default function Post({ postData }) {
  return (
    <>
      <Head>
        <title>{postData.frontmatter.title} | Artemis City Blog</title>
        <meta name="description" content={postData.frontmatter.description || postData.frontmatter.title} />
      </Head>
      <article className="themed-surface p-8 rounded-2xl shadow-soft">
        <header className="mb-8 border-b border-secondary-200 pb-6">
          <h1 className="text-5xl font-extrabold text-secondary-900 mb-3 leading-tight">
            {postData.frontmatter.title}
          </h1>
          <p className="text-secondary-600 text-lg">
            Published on{' '}
            {new Date(postData.frontmatter.date).toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </p>
        </header>

        <div className="prose prose-lg max-w-none prose-blue">
          <MDXRemote {...postData.content} components={MDXComponents} />
        </div>
      </article>
    </>
  );
}
