/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'bg-main': '#0a0a0f',
        'bg-side': '#11111d',
        'card-bg': 'rgba(26, 26, 46, 0.7)',
        'accent': '#8b5cf6',
        'accent-hover': '#7c3aed',
        'text-primary': '#f1f1f7',
        'text-secondary': '#94a3b8',
        'success': '#10b981',
      },
      backgroundImage: {
        'gradient-accent': 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
        'gradient-dark': 'linear-gradient(135deg, rgba(26, 26, 46, 0.5), rgba(11, 11, 29, 0.5))',
      }
    },
  },
  plugins: [],
}
