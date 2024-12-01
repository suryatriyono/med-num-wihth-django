/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './regula_falsi/templates/**/*.html', // Semua file HTML dalam folder templates
    './regula_falsi/**/*.py', // Semua file Python dalam aplikasi Django
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
