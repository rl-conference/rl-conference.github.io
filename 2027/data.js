/////// HOME PAGE ///////

/// Advisory committee ///
class AdvisoryCommittee {
    constructor(name, affiliation, image) {
        this.name = name;
        this.affiliation = affiliation;
        this.image = image;
    }
}

/// Board Members ///
class BoardMember {
    constructor(name, affiliation, image) {
        this.name = name;
        this.affiliation = affiliation;
        this.image = image;
    }
}

/// Advisory committee ///
class KeynoteSpeaker {
    constructor(name, affiliation, image, url, cancelled) {
        this.name = name;
        this.affiliation = affiliation;
        this.image = image;
        this.url = url || "";
        this.cancelled = !!cancelled;
    }
}

// RLC 2027 advisory committee: same as 2026. Photos copied from /2026/data/advisoryCom/ as firstname-lastname.ext
listOfAdvisoryCommittee = [new AdvisoryCommittee("Peter Stone", "The University of Texas at Austin / SonyAI", "data/advisoryCom/peter-stone.jpg"),
new AdvisoryCommittee("Satinder Singh", "University of Michigan / DeepMind", "data/advisoryCom/satinder-singh.jpg"),
new AdvisoryCommittee("Emma Brunskill", "Stanford University", "data/advisoryCom/emma-brunskill.jpg"),
new AdvisoryCommittee("Michael Littman", "Brown University", "data/advisoryCom/michael-littman.jpg"),
new AdvisoryCommittee("Shie Mannor", "Technion / NVIDIA", "data/advisoryCom/shie-mannor.jpg"),
new AdvisoryCommittee("Michael Bowling", "University of Alberta", "data/advisoryCom/michael-bowling.jpg"),
new AdvisoryCommittee("Sergey Levine", "University of California, Berkeley", "data/advisoryCom/sergey-levine.jpg"),
new AdvisoryCommittee("Balaraman Ravindran", "IIT Madras", "data/advisoryCom/balaraman-ravindran.jpg"),
new AdvisoryCommittee("Sham Kakade", "Harvard University", "data/advisoryCom/sham-kakade.jpg"),
new AdvisoryCommittee("Benjamin Rosman", "University of Witwatersrand", "data/advisoryCom/benjamin-rosman.jpg"),
new AdvisoryCommittee("Marc Deisenroth", "University College London", "data/advisoryCom/marc-deisenroth.jpg"),
new AdvisoryCommittee("Andrew Barto", "University of Massachusetts Amherst", "data/advisoryCom/andrew-barto.jpg"),
new AdvisoryCommittee("Benjamin Van Roy", "Stanford University / DeepMind", "data/advisoryCom/benjamin-van-roy.jpg")]

// RLC 2027 board. Photos copied from /2026/data/board/ as firstname-lastname.ext
listOfBoardMembers = [new BoardMember("Eugene Vinitsky", "New York University", "data/board/eugene-vinitsky.jpg"),
new BoardMember("Glen Berseth", "Université de Montréal", "data/board/glen-berseth.webp"),
new BoardMember("Amy Zhang", "The University of Texas at Austin", "data/board/amy-zhang.webp"),
new BoardMember("Martha White", "University of Alberta", "data/board/martha-white.webp"),
new BoardMember("Adam White", "University of Alberta", "data/board/adam-white.webp"),
new BoardMember("Scott Niekum", "University of Massachusetts Amherst", "data/board/scott-niekum.jpg")]


///// Menu Items /////
class MenuItem {
    constructor(name, link) {
        this.name = name;
        this.link = link;
    }
}

class MenuItemWithSubmenu {
    constructor(name, subMenuItems) {
        this.name = name;
        this.subMenuItems = subMenuItems;
    }
}





listOfMenuItems = [
    // Submission/review instructions now live on rlj.org (linked from "Presenting at RLC").
    new MenuItemWithSubmenu("Submit", [
        new MenuItem("Presenting&nbsp;at&nbsp;RLC", "presenting.html"), new MenuItem("Call&nbsp;for&nbsp;Workshops", "call_for_workshops.html"),
    ]),
    // Program tab hidden until the 2027 program exists. Re-enable (and per-location pages) when ready:
    // new MenuItemWithSubmenu("Program", [new MenuItem("Schedule", "schedule.html"), new MenuItem("Paper&nbsp;Schedule", "paper_schedule.html"), new MenuItem("Outstanding&nbspPapers", "RLC2027Awards.html"), new MenuItem("Accepted&nbsp;Workshops", "accepted_workshops.html")]),
    new MenuItemWithSubmenu("Attend", [new MenuItem("Registration", "register.html"), new MenuItem("Accommodation", "accommodation.html"), new MenuItem("FAQ", "faq.html"),
        // new MenuItem("Child&nbsp;care", "TODO: 2027 child care link"),
    ]),
    new MenuItemWithSubmenu("Organizers", [new MenuItem("Organizers", "organizers.html"), new MenuItem("Advisors", "advisors.html"), new MenuItem("Volunteers", "volunteers.html"), new MenuItem("Board&nbsp;Members", "boardmembers.html")]),
    new MenuItemWithSubmenu("Year", [new MenuItem("2026", "/2026/index.html"), new MenuItem("2025", "/2025/index.html"), new MenuItem("2024", "/2024/index.html")]),
]


let footerText = `© 2027 Reinforcement Learning Conference Organization Committee`

//// SEO ////
let mainPageTitleforSEO = 'Reinforcement Learning Conference'
let homeSearchEngineDescription = "Reinforcement Learning Conference."


/// Organizers ///

class Organizer {
    constructor(name, role, image) {
        this.name = name;
        this.role = role;
        this.image = image;
    }
}

// RLC 2027 organizers. Photos live in data/organizers/ as firstname-lastname.ext
listOfOrganizers = [new Organizer("Josiah Hanna", "General Chair", "data/organizers/josiah-hanna.webp"),
    new Organizer("Nan Jiang", "Program Chair", "data/organizers/nan-jiang.jpg"),
    new Organizer("Claire Vernade", "Program Chair", "data/organizers/claire-vernade.jpeg"),
    new Organizer("Pablo Samuel Castro", "Program Chair", "data/organizers/pablo-castro.png"),
    new Organizer("Claas Voelcker", "Inclusion Chair", "data/organizers/claas-voelcker.jpg"),
    new Organizer("Brad Knox", "Sponsorship Chair", "data/organizers/brad-knox.png"),
    new Organizer("Serena Booth", "Local Chair (Providence)", "data/organizers/serena-booth.jpg"),
    new Organizer("George Konidaris", "Local Chair (Providence)", "data/organizers/george-konidaris.jpg"),
    new Organizer("Michael Littman", "Local Chair (Providence)", "data/organizers/michael-littman.jpeg"),
    new Organizer("Eura Nofshin", "Website Chair", "data/organizers/eura-nofshin.jpg")
]


// RLC 2027: keynote speakers not yet announced
listOfKeynoteSpeakers = []

class Workshop {
    constructor(name, link, description, contacts, room) {
        this.name = name;
        this.link = link;
        this.description = description;
        this.contacts = contacts;
        this.room = room;
    }
}

class Sponsor {
    constructor(name, link, image, level, description) {
        this.name = name;
        this.link = link;
        this.image = image;
        this.level = level;
        this.description = description;
    }
}


