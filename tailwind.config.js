/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["index.html", "guidelines.html", "organizers.html", "reviewProcess.html", "callforpapers.html", "recordings.html", "submissionInstructions.html", "contact.html", "advisors.html", "reviewers.html", "sponsors.html", "reviewinstructions.html", "participate.html", "register.html", "hotels.html", "hotelmap.html", "registration_confirmation.html", "code_of_conduct.html"],
  theme: {
    colors: {
      'rlyellow': {
        '50': '#fffaeb',
        '100': '#fdf0c8',
        '200': '#fcdf8b',
        '300': '#fac84f',
        '400': '#f8ae1c',
        '500': '#f2900e',
        '600': '#d66b09',
        '700': '#b2490b',
        '800': '#903910',
        '900': '#772f10',
        '950': '#441604',
      },
      'rllightblue': {
        '50': '#f4f8fb',
        '100': '#e8f0f6',
        '200': '#cbe1ec',
        '300': '#96c3d8',
        '400': '#6aaac6',
        '500': '#478fb0',
        '600': '#357494',
        '700': '#2c5d78',
        '800': '#284f64',
        '900': '#254355',
        '950': '#192c38',
      },
      'rldarkblue': {
        '50': '#f1f8fe',
        '100': '#e3f0fb',
        '200': '#c1e1f6',
        '300': '#8acaef',
        '400': '#4baee5',
        '500': '#2494d3',
        '600': '#1676b3',
        '700': '#135d91',
        '800': '#135079',
        '900': '#154161',
        '950': '#0e2b43',
      },
      'rlgrey' : "#FFFFFF",
      'blue' : "#1B3A9E",
      'midblue' : "#256ed4",
      'white' : '#FFFFFF',
      'black' : '#000000',
      'backgroundcolor' : "#F0EFEB"
    },
    extend: {
      aspectRatio: {
        '2/3': '2 / 3',
      },
    },
    fontFamily: {
      'bai' : ['Bai Jamjuree', 'sans-serif'],
      'rubik' : ['Rubik', 'sans-serif'],
      'roboto': ['Roboto', 'sans-serif']
    },
    safelist: [
      "backdrop-blur-sm", "font-rubik" ,"text-xl" ,"ml-4" ,"mr-4" ,"text-rldarkblue-900" ,"hover:text-rldarkblue-500" ,"hover:cursor-pointer", "flex" ,"flex-row-reverse",
        "right-20", "bg-white", "m-6", "p-6"

    ]
  },
  plugins: [],
}

