/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#17211b",
        forest: "#1f5d48",
        gold: "#c79535",
        mist: "#eef4f0",
      },
      boxShadow: {
        soft: "0 14px 38px rgba(31, 93, 72, 0.12)",
      },
    },
  },
  plugins: [],
};
