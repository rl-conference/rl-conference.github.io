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

// RLC 2027: advisory committee not yet announced (2026 list: see /2026/data.js)
listOfAdvisoryCommittee = []

// RLC 2027: board members not yet announced (2026 list: see /2026/data.js)
listOfBoardMembers = []


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
    new MenuItemWithSubmenu("Submit", [
        new MenuItem("Call&nbsp;for&nbsp;Papers", "callforpapers.html"), new MenuItem("Call&nbsp;for&nbsp;Workshops", "call_for_workshops.html"), new MenuItem("Submission&nbsp;Instructions", "submissionInstructions.html"),
        new MenuItem("Review&nbsp;Instructions", "https://rlj.org/reviewers-guide"),
    ]),
    // Program tab hidden until the 2027 program exists. Re-enable (and per-location pages) when ready:
    // new MenuItemWithSubmenu("Program", [new MenuItem("Schedule", "schedule.html"), new MenuItem("Paper&nbsp;Schedule", "paper_schedule.html"), new MenuItem("Outstanding&nbspPapers", "RLC2027Awards.html"), new MenuItem("Accepted&nbsp;Workshops", "accepted_workshops.html")]),
    new MenuItemWithSubmenu("Attend", [new MenuItem("Registration", "register.html"), new MenuItem("Accommodation", "accommodation.html"), new MenuItem("FAQ", "faq.html"),
        // new MenuItem("Child&nbsp;care", "TODO: 2027 child care link"),
    ]),
    new MenuItemWithSubmenu("Organizers", [new MenuItem("Organizers", "organizers.html"), new MenuItem("Advisors", "advisors.html"), new MenuItem("Reviewers", "reviewers.html"), new MenuItem("Volunteers", "volunteers.html"), new MenuItem("Board&nbsp;Members", "boardmembers.html")]),
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


