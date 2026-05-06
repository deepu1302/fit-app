/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./fit.html",
    "./backend/**/*.js"
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Nunito', 'sans-serif'],
      },
      colors: {
        'cyan': {
          300: '#67e8f9',
          400: '#22d3ee',
        },
        'blue': {
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
        },
      }
    },
  },
  plugins: [],
}
