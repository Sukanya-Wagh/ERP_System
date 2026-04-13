/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'neon-cyan': '#00ffff',
        'neon-purple': '#8b5cf6',
        'neon-green': '#00ff00',
        'neon-yellow': '#ffff00',
        'neon-pink': '#ff00ff',
        'cyber-dark': '#0a0a0a',
        'cyber-gray': '#1a1a1a',
        'cyber-light': '#2a2a2a',
      },
      boxShadow: {
        'neon-cyan': '0 0 20px #00ffff',
        'neon-purple': '0 0 20px #8b5cf6',
        'neon-green': '0 0 20px #00ff00',
        'neon-yellow': '0 0 20px #ffff00',
        'neon-pink': '0 0 20px #ff00ff',
        'glow': '0 0 30px rgba(0, 255, 255, 0.3)',
      },
      animation: {
        'pulse-glow': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [],
}