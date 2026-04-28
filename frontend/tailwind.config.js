/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          bg: '#FFFDF5',
          green: '#2E7D32',
          'green-light': '#4CAF50',
          'green-dark': '#1B5E20',
          amber: '#FF8F00',
          'amber-light': '#FFB300',
          text: '#1A1A1A',
          muted: '#6B7280',
          card: '#FFFFFF',
          border: '#E5E7EB',
        },
      },
      fontFamily: {
        heading: ['"Baloo 2"', 'cursive'],
        body: ['Inter', 'sans-serif'],
      },
      boxShadow: {
        card: '0 2px 16px 0 rgba(46,125,50,0.07)',
        'card-hover': '0 6px 28px 0 rgba(46,125,50,0.13)',
      },
    },
  },
  plugins: [],
}
