import Link from 'next/link';
import { useRouter } from 'next/router';
import { useTheme } from './ThemeProvider';

export default function Layout({ children }) {
  const router = useRouter();
  const { isGlass, toggleTheme } = useTheme();

  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'Blog', href: '/blog' },
    { name: 'About', href: '/about' },
    { name: 'Contact', href: '/contact' },
  ];

  const isActive = (path) => {
    if (path === '/') {
      return router.pathname === '/';
    }
    return router.pathname.startsWith(path);
  };

  const containerClass = isGlass
    ? 'min-h-screen relative overflow-hidden flex flex-col bg-slate-950 text-slate-100'
    : 'min-h-screen flex flex-col bg-gradient-to-br from-secondary-50 via-white to-primary-50';

  return (
    <div className={containerClass}>

      {isGlass && (
        <div className="pointer-events-none absolute inset-0 -z-10 overflow-hidden">
          <div className="absolute -left-24 top-6 w-80 h-80 rounded-full bg-cyan-500/20 blur-3xl" />
          <div className="absolute right-[-10%] top-1/3 w-96 h-96 rounded-full bg-fuchsia-500/25 blur-[140px]" />
          <div className="absolute left-1/3 bottom-[-10%] w-[28rem] h-[28rem] rounded-full bg-blue-500/30 blur-[120px]" />
        </div>
      )}

      <header
        className={`sticky top-0 z-50 border-b backdrop-blur-md ${
          isGlass
            ? 'bg-slate-900/70 border-cyan-400/20 shadow-[0_20px_60px_-25px_rgba(56,189,248,0.45)]'
            : 'bg-white/80 border-secondary-200 shadow-soft'
        }`}
      >
        <nav className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-10">
            <Link href="/" className="group flex items-center space-x-2">
              <div
                className={`text-3xl font-bold bg-clip-text text-transparent transition-all duration-300 ${
                  isGlass
                    ? 'bg-gradient-to-r from-cyan-300 via-blue-300 to-fuchsia-400 drop-shadow-[0_0_18px_rgba(34,211,238,0.45)]'
                    : 'bg-gradient-to-r from-primary-600 to-primary-400 group-hover:from-primary-500 group-hover:to-primary-300'
                }`}
              >
                Artemis City
              </div>
            </Link>

            <div className="flex items-center space-x-1 rounded-full bg-white/0">
              {navigation.map((item) => {
                const active = isActive(item.href);
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                      active
                        ? isGlass
                          ? 'bg-white/10 text-cyan-100 border border-cyan-400/40 shadow-glow'
                          : 'bg-primary-500 text-white shadow-md'
                        : isGlass
                          ? 'text-slate-200 hover:text-white hover:bg-white/10 border border-transparent'
                          : 'text-secondary-600 hover:bg-secondary-100 hover:text-primary-600'
                    }`}
                  >
                    {item.name}
                  </Link>
                );
              })}
            </div>
          </div>

          <button
            type="button"
            onClick={toggleTheme}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold transition-all duration-300 ${
              isGlass
                ? 'bg-white/10 text-cyan-100 border border-cyan-400/40 shadow-[0_0_0_1px_rgba(56,189,248,0.35)] hover:bg-white/15'
                : 'bg-secondary-100 text-secondary-700 hover:bg-secondary-200'
            }`}
            aria-label="Toggle theme"
          >
            <span className="text-lg">{isGlass ? '🤖' : '🌤️'}</span>
            <span className="text-sm uppercase tracking-wide">{isGlass ? 'Glass Robo' : 'Default'}</span>
          </button>
        </nav>
      </header>

      <main className="flex-grow container mx-auto px-6 py-12">
        {children}
      </main>

      <footer
        className={`py-12 border-t ${
          isGlass
            ? 'bg-slate-900/70 text-slate-100 border-cyan-500/15 backdrop-blur-xl'
            : 'bg-gradient-to-r from-secondary-900 to-secondary-800 text-secondary-200 border-secondary-700'
        }`}
      >
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            <div>
              <h3 className="text-xl font-bold text-white mb-4">Artemis City</h3>
              <p className="text-secondary-300 text-sm">
                The Kernel for AI Agents.
              </p>
            </div>
            <div>
              <h4 className="text-lg font-semibold text-white mb-4">Quick Links</h4>
              <ul className="space-y-2 text-sm">
                {navigation.map((item) => (
                  <li key={item.name}>
                    <Link href={item.href} className="hover:text-primary-400 transition-colors">
                      {item.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="text-lg font-semibold text-white mb-4">Community</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="https://discord.gg/artemis-city" target="_blank" rel="noopener noreferrer" className="hover:text-primary-400 transition-colors">Discord</a></li>
                <li><a href="https://github.com/popvilla/Artemis-City" target="_blank" rel="noopener noreferrer" className="hover:text-primary-400 transition-colors">GitHub</a></li>
                <li><a href="https://twitter.com/artemis_city" target="_blank" rel="noopener noreferrer" className="hover:text-primary-400 transition-colors">Twitter</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-secondary-700 pt-8 text-center text-sm text-secondary-400">
            &copy; {new Date().getFullYear()} Artemis City. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
