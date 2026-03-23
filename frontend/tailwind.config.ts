import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Professional Monochrome Theme
        primary: {
          50: '#f8f9fa',
          100: '#f1f3f5',
          200: '#e9ecef',
          300: '#dee2e6',
          400: '#ced4da',
          500: '#adb5bd',
          600: '#868e96',
          700: '#495057',
          800: '#343a40',
          900: '#212529',
          950: '#0d0f12',
        },
        accent: {
          light: '#ffffff',
          DEFAULT: '#000000',
          dark: '#0a0a0a',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'monospace'],
      },
      boxShadow: {
        'mono': '0 2px 8px rgba(0, 0, 0, 0.08)',
        'mono-lg': '0 4px 16px rgba(0, 0, 0, 0.12)',
        'mono-xl': '0 8px 32px rgba(0, 0, 0, 0.16)',
      },
      borderRadius: {
        'mono': '2px',
      },
    },
  },
  plugins: [],
};
export default config;
