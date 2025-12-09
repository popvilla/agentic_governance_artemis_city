/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Allow cross-origin requests from local network devices
  allowedDevOrigins: ['192.168.0.201'],
  // Add any other Next.js specific configurations here
  // For example, image optimization domains, redirects etc.
}

module.exports = nextConfig
// Compare this snippet from Q%7C%3EH_Blog/artemis-city-blog/pages/index.js::
// import Link from 'next/link';
// import { getSortedPostsData } from '../lib/mdx';
//
// export default function Home({ allPostsData }) {
//   return (
//     <div className="max-w-3xl mx-auto">
//       <h1 className="text-5xl font-extrabold text-center mb-10 text-gray-800">Artemis City Blog</h1>
//
//       <section className="mt-8">
//         <h2 className="text-3xl font-bold mb-6 text-gray-700">Recent Posts</h2>
//         <ul className="space-y-8">
//           {allPostsData.map(({ slug, date, title, description }) => (
//             <li key={slug} className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200">
//               <Link href={`/blog/${slug}`} className="block">
//                 <h3 className="text-2xl font-semibold text-blue-700 hover:text-blue-800 transition-colors duration-200">{title}</h3>
//                 <small className="text-gray-500 block mt-1">{new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</small>
//                 <p className="mt-3 text-gray-700">{description}</p>
//                 <span className="inline-block mt-4 text-blue-600 hover:text-blue-700 font-medium">Read More &rarr;</span>
//               </Link>
//             </li>
//           ))}
//         </ul>
//       </section>
//     </div>
//   );
// }
//
// export async function getStaticProps() {
//   const allPostsData = getSortedPostsData();
//   return {
//     props: {
//       allPostsData,
//     },
//   };
// }
