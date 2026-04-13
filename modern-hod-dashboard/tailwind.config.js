/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Dark Neon Cyber Theme
        'cyber-dark': '#0a0a0f',
        'cyber-darker': '#050508',
        'cyber-card': '#121218',
        'cyber-surface': '#1a1a24',
        'cyber-border': '#2a2a3a',
        
        // Neon Colors
        'neon-cyan': '#00f5ff',
        'neon-teal': '#00d4aa',
        'neon-purple': '#8b5cf6',
        'neon-yellow': '#ffd700',
        'neon-pink': '#ff00ff',
        'neon-green': '#00ff9d',
        
        // Text Colors
        'text-primary': '#e5e7eb',
        'text-secondary': '#9ca3af',
        'text-muted': '#6b7280',
        
        // Status Colors
        'success': '#00ff9d',
        'warning': '#ffd700',
        'error': '#ff3864',
        'info': '#00f5ff',
      },
      fontFamily: {
        'cyber': ['Orbitron', 'monospace'],
        'modern': ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'neon-cyan': '0 0 20px rgba(0, 245, 255, 0.5)',
        'neon-purple': '0 0 20px rgba(139, 92, 246, 0.5)',
        'neon-yellow': '0 0 20px rgba(255, 215, 0, 0.5)',
        'neon-teal': '0 0 20px rgba(0, 212, 170, 0.5)',
        'glow': '0 0 30px rgba(0, 245, 255, 0.3)',
        'glow-lg': '0 0 40px rgba(0, 245, 255, 0.4)',
      },
      animation: {
        'pulse-glow': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-in': 'slideIn 0.3s ease-out',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideIn: {
          '0%': { transform: 'translateX(-10px)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        glow: {
          '0%': { boxShadow: '0 0 20px rgba(0, 245, 255, 0.5)' },
          '100%': { boxShadow: '0 0 30px rgba(0, 245, 255, 0.8)' },
        },
      },
      backdropBlur: {
        'xs': '2px',
      },
    },
  },
  plugins: [],
}