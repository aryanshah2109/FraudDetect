/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'display': ['Syne', 'sans-serif'],
        'mono': ['Space Mono', 'monospace'],
      },
      colors: {
        'void': '#080c10',
        'surface': '#0d1117',
        'panel': '#111820',
        'border': '#1e2a38',
        'accent': '#00d4ff',
        'accent-dim': '#0099bb',
        'danger': '#ff3d5a',
        'danger-dim': '#cc1f3a',
        'safe': '#00e5a0',
        'safe-dim': '#00a870',
        'warn': '#ffaa00',
        'text-primary': '#e8f0fe',
        'text-secondary': '#7a92aa',
        'text-muted': '#3d5266',
      },
      boxShadow: {
        'accent': '0 0 20px rgba(0, 212, 255, 0.15)',
        'danger': '0 0 20px rgba(255, 61, 90, 0.2)',
        'safe': '0 0 20px rgba(0, 229, 160, 0.2)',
        'panel': '0 4px 24px rgba(0, 0, 0, 0.4)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'scan': 'scan 2s ease-in-out infinite',
        'flicker': 'flicker 4s linear infinite',
      },
      keyframes: {
        scan: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.4' },
        },
        flicker: {
          '0%, 100%': { opacity: '1' },
          '92%': { opacity: '1' },
          '93%': { opacity: '0.8' },
          '94%': { opacity: '1' },
          '96%': { opacity: '0.9' },
          '97%': { opacity: '1' },
        }
      }
    },
  },
  plugins: [],
}
