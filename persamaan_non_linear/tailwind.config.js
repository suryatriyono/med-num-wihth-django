/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './templates/gaus/**/*.html',
    './newton_raphson/templates/**/*.html', // Semua file HTML dalam folder templates
    './newton_raphson/**/*.py', // Semua file Python dalam aplikasi Django
    './secant/templates/**/*.html', // all HTML files in folder templates
    './secant/**/*.py', // all python fiiles in application Django
    './gaus/**/*.py',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
