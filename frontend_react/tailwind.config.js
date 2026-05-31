/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f5f3f0',
          100: '#ebe4df',
          200: '#d7c9bf',
          300: '#c3ad9f',
          400: '#a6845f',
          500: '#8b5a2b',
          600: '#704a22',
          700: '#55391a',
          800: '#3a2812',
          900: '#1f170a',
        },
        secondary: {
          50: '#ecf0f9',
          100: '#d9e2f3',
          200: '#b3c5e7',
          300: '#8da7db',
          400: '#6789cf',
          500: '#4166c3',
          600: '#2d4a9f',
          700: '#1e3a7b',
          800: '#142a57',
          900: '#0a1a33',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'soft': '0 2px 8px rgba(0, 0, 0, 0.1)',
        'medium': '0 4px 12px rgba(0, 0, 0, 0.15)',
        'lg': '0 10px 25px rgba(0, 0, 0, 0.2)',
      }
    },
  },
  plugins: [],
}
