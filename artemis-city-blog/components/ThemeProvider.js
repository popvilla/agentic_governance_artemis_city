import { createContext, useContext, useEffect, useMemo, useState } from 'react';

const ThemeContext = createContext({
  theme: 'default',
  isGlass: false,
  setTheme: () => {},
  toggleTheme: () => {},
});

const STORAGE_KEY = 'artemis-theme';
const THEMES = {
  DEFAULT: 'default',
  GLASS: 'glass',
};

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(THEMES.DEFAULT);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const storedTheme = window.localStorage.getItem(STORAGE_KEY);
    if (storedTheme === THEMES.GLASS || storedTheme === THEMES.DEFAULT) {
      setTheme(storedTheme);
    }
  }, []);

  useEffect(() => {
    if (typeof document === 'undefined') return;
    const nextClass = theme === THEMES.GLASS ? 'theme-glass' : 'theme-default';
    document.body.classList.remove('theme-glass', 'theme-default');
    document.body.classList.add(nextClass);
    if (typeof window !== 'undefined') {
      window.localStorage.setItem(STORAGE_KEY, theme);
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === THEMES.GLASS ? THEMES.DEFAULT : THEMES.GLASS));
  };

  const value = useMemo(
    () => ({
      theme,
      isGlass: theme === THEMES.GLASS,
      setTheme,
      toggleTheme,
    }),
    [theme],
  );

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  return useContext(ThemeContext);
}
