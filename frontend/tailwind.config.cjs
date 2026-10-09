/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      boxShadow: {
        glow: '0 0 0 1px rgba(99,102,241,0.3), 0 18px 40px rgba(79, 70, 229, 0.28)',
      },
    },
  },
  plugins: [],
}

