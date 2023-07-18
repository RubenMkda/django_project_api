/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./api_django/templates/**/*.{html,js}"],
  theme: {
    extend: {
      flex: {
        '3': '0 0 33.3333333%'
      }
    },
  },
  plugins: [],
}

