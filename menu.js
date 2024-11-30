doc = document.getElementById("largeMenu")
var str = '<div class="flex flex-row-reverse">'
for (let i = listOfMenuItems.length - 1; i > -1; i--) {
    // check if the menu item has a submenu
    if (listOfMenuItems[i].subMenuItems) {
        str += '<div class="relative text-center group">'
        str += '<a href="#" class="font-rubik text-center text-xl ml-4 mr-4 text-blue hover:text-rldarkblue-500 hover:cursor-pointer">' + listOfMenuItems[i].name + '</a>'
        str += '<div class="hidden group-hover:block absolute right-0 bg-rlgrey/100 shadow-md p-2 rounded-md border-1 border-black z-40">'
        for (let j = 0; j < listOfMenuItems[i].subMenuItems.length; j++) {
            str += '<div class="m-2 p-2"><a href="' + listOfMenuItems[i].subMenuItems[j].link + '" class="p-2 m-2 font-rubik text-center text-rldarkblue-900 hover:text-rldarkblue-500 hover:cursor-pointer  text-base sm:text-base">' + listOfMenuItems[i].subMenuItems[j].name + '</a></div>'
        }
        str += '</div>'
        str += '</div>'
    }
    else {
        str += '<a href="' + listOfMenuItems[i].link + '"class="font-rubik text-xl ml-4 mr-4 text-blue hover:text-rldarkblue-500 hover:cursor-pointer">' + listOfMenuItems[i].name + '</a>'
    }
}
str += '</div>'
doc.innerHTML = str

// Add collapsed menu items as rows
doc = document.getElementById("collapsedMenuItems")
var str = ''
for (let i = 0; i < listOfMenuItems.length; i++) {
    if(listOfMenuItems[i].subMenuItems){
        str += '<div class="relative text-center p-2 m-2 group">'
        str += '<a href="#" class="font-rubik text-center text-rldarkblue-900 hover:text-rldarkblue-500 hover:cursor-pointer  text-base sm:text-base">' + listOfMenuItems[i].name + '</a>'
        str += '<div class="hidden group-hover:block absolute right-0 bg-rlgrey/100 shadow-lg mt-2 p-2 rounded-md z-40">'
        for (let j = 0; j < listOfMenuItems[i].subMenuItems.length; j++) {
            str += '<div class="m-2 p-2"><a href="' + listOfMenuItems[i].subMenuItems[j].link + '" class="p-2 font-rubik text-center m-2 text-rldarkblue-900 hover:text-rldarkblue-500 hover:cursor-pointer  text-base sm:text-base">' + listOfMenuItems[i].subMenuItems[j].name + '</a></div>'
        }
        str += '</div>'
        str += '</div>'
    }
    else {
        str += '<a href="' + listOfMenuItems[i].link + '" class="p-2 font-rubik text-center m-2 text-rldarkblue-900 hover:text-rldarkblue-500 hover:cursor-pointer  text-base sm:text-base">' + listOfMenuItems[i].name + '</a>'
    }
}
doc.innerHTML = str


showMenu = function () {

    // Chcck if "hidden" class is present
    if ($('#collapsedMenuItems').hasClass('hidden')) {
        $('#collapsedMenuItems').removeClass('hidden')
    } else {
        $('#collapsedMenuItems').addClass('hidden')
    }
}

// Add footer
doc = document.getElementById("footerText")
doc.innerHTML = footerText

