import Head from 'next/head';
import { useState } from 'react';

export default function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
  });
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
    setTimeout(() => {
      setFormData({ name: '', email: '', subject: '', message: '' });
      setSubmitted(false);
    }, 3000);
  };

  return (
    <>
      <Head>
        <title>Community | Artemis City</title>
        <meta name="description" content="Join the Artemis City community on Discord, GitHub, and Twitter to ask questions, share projects, and stay updated." />
      </Head>

      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-16 animate-fade-in-up">
          <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent mb-6">
            Join the Community
          </h1>
          <p className="text-xl text-secondary-600 max-w-2xl mx-auto">
            Connect with us and other developers building the future of AI orchestration.
          </p>
        </div>

        <div className="space-y-8">
          <div className="themed-surface rounded-2xl shadow-soft p-8 md:p-12 animate-fade-in-up transition-transform transform hover:-translate-y-1 hover:shadow-lg">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Discord</h2>
            <p className="text-lg text-secondary-700 leading-relaxed mb-6">
              Join our active community on Discord for real-time discussions, support, and collaboration. It&#39;s the best place to ask questions and share your projects.
            </p>
            <a 
              href="https://discord.gg/artemis-city" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="btn-primary"
            >
              Join the Discord Server
            </a>
          </div>

          <div className="themed-surface rounded-2xl shadow-soft p-8 md:p-12 animate-fade-in-up transition-transform transform hover:-translate-y-1 hover:shadow-lg">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">GitHub Discussions</h2>
            <p className="text-lg text-secondary-700 leading-relaxed mb-6">
              For more structured conversations, bug reports, or feature requests, head over to our GitHub Discussions. Search for existing topics or start a new one.
            </p>
            <a 
              href="https://github.com/popvilla/Artemis-City/discussions" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="btn-secondary"
            >
              Go to GitHub Discussions
            </a>
          </div>

          <div className="themed-surface rounded-2xl shadow-soft p-8 md:p-12 animate-fade-in-up transition-transform transform hover:-translate-y-1 hover:shadow-lg">
            <h2 className="text-3xl font-bold text-secondary-900 mb-4">Twitter / X</h2>
            <p className="text-lg text-secondary-700 leading-relaxed mb-6">
              Follow us on Twitter for the latest project updates, announcements, and news from the world of AI and agentic systems.
            </p>
            <a 
              href="https://twitter.com/artemis_city" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="btn-secondary"
            >
              Follow @artemis_city
            </a>
          </div>
        </div>
      </div>
    </>
  );
}
