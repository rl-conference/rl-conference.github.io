/////// HOME PAGE ///////

/// Advisory committee ///
class AdvisoryCommittee {
    constructor(name, affiliation, image) {
        this.name = name;
        this.affiliation = affiliation;
        this.image = image;
    }
}

/// Advisory committee ///
class KeynoteSpeaker {
    constructor(name, affiliation, image) {
        this.name = name;
        this.affiliation = affiliation;
        this.image = image;
    }
}

listOfAdvisoryCommittee = [new AdvisoryCommittee("Peter Stone", "The University of Texas at Austin / SonyAI", "data/advisoryCom/ps.jpg"),
new AdvisoryCommittee("Satinder Singh", "University of Michigan / DeepMind", "data/advisoryCom/ss.jpg"),
new AdvisoryCommittee("Emma Brunskill", "Stanford University", "data/advisoryCom/eb.jpg"),
new AdvisoryCommittee("Michael Littman", "Brown University", "data/advisoryCom/ml.jpg"),
new AdvisoryCommittee("Shie Mannor", "Technion / NVIDIA", "data/advisoryCom/sm.jpg"),
new AdvisoryCommittee("Michael Bowling", "University of Alberta", "data/advisoryCom/mb.jpg"),
new AdvisoryCommittee("Sergey Levine", "University of California, Berkeley"
    , "data/advisoryCom/sl.jpg"),
new AdvisoryCommittee("Balaraman Ravindran", "IIT Madras", "data/advisoryCom/br_1.jpg"),
new AdvisoryCommittee("Sham Kakade", "Harvard University", "data/advisoryCom/sk.jpg"),
new AdvisoryCommittee("Benjamin Rosman", "University of Witwatersrand", "data/advisoryCom/br.jpg"),
new AdvisoryCommittee("Marc Deisenroth", "University College London", "data/advisoryCom/md.jpg"),
new AdvisoryCommittee("Andrew Barto", "University of Massachusetts Amherst", "data/advisoryCom/ab.jpg"),
new AdvisoryCommittee("Benjamin Van Roy", "Stanford University / DeepMind", "data/advisoryCom/bvr.jpg")]

listOfKeynoteSpeakers = [new KeynoteSpeaker("Leslie Kaelbling", "Massachusetts Institute of Technology", "data/keynoteSpeakers/lk.jpg"),
new KeynoteSpeaker("Peter Dayan", "Max Planck Institute for Biological Cybernetics", "data/keynoteSpeakers/pd.webp"),
new KeynoteSpeaker("Richard S. Sutton", "University of Alberta / Keen Technologies / Amii", "data/keynoteSpeakers/rs.webp"),
new KeynoteSpeaker("Dale Schuurmans", "University of Alberta / Google DeepMind / Amii", "data/keynoteSpeakers/ds.webp"),
new KeynoteSpeaker("Joelle Pineau", "McGill University / Meta / Mila", "data/keynoteSpeakers/jp.webp"),
new KeynoteSpeaker("Michael Littman", "Brown University", "data/keynoteSpeakers/ml.webp")]


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
    new MenuItemWithSubmenu("Previous Years", [new MenuItem("2025", "/2025/index.html"), new MenuItem("2024", "/2024/index.html")]),
]


///// Footer /////
let footerText = `© 2025 Reinforcement Learning Conference Organization Committee`

//// SEO ////
let mainPageTitleforSEO = 'RLC 2025'
let homeSearchEngineDescription = "Reinforcement Learning Conference."


/// Organizers ///

class Organizer {
    constructor(name, role, image) {
        this.name = name;
        this.role = role;
        this.image = image;
    }
}

listOfOrganizers = [new Organizer("Adam White", "General Chair", "data/organizers/aw.webp"),
new Organizer("Phil Thomas", "Program Chair", "data/organizers/pt.jpg"),
new Organizer("Marlos C Machado", "Program Chair", "data/organizers/mcm.webp"),
new Organizer("Cathy Wu", "Program Chair", "data/organizers/cw.jpg"),
new Organizer("Andrew Patterson", "Program Chair", "data/organizers/ap.jpg"),
new Organizer("Brad Knox", "Keynote and Scheduling Chair", "data/organizers/bk.png"),
new Organizer("Tom Schaul", "Keynote and Scheduling Chair", "data/organizers/ts.jpg"),
new Organizer("Emma Jordan", "Keynote and Scheduling Chair", "data/organizers/ej.webp"),
new Organizer("Roberta Raileanu", "Awards Chair", "data/organizers/rr.jpg"),
new Organizer("Ida Momennejad", "Awards Chair", "data/organizers/im.jpg"),
new Organizer("Martha White", "Local Chair", "data/organizers/mw.webp"),
new Organizer("Mike Bowling", "Local Chair", "data/organizers/mb.jpg"),
new Organizer("Patrick Pilarski", "Local and Volunteers Chair", "data/organizers/pp.jpg"),
new Organizer("Alex Lewandowski", "Local and Volunteers Chair", "data/organizers/al.jpg"),
new Organizer("Glen Berseth", "Sponsorship Chair", "data/organizers/gb.webp"),
new Organizer("Audrey Durand", "Sponsorship Chair", "data/organizers/ad.jpg"),
new Organizer("Josiah Hanna", "Workshop Chair", "data/organizers/jh.jpeg"),
new Organizer("Claire Vernade", "Workshop Chair", "data/organizers/cv.jpg"),
new Organizer("Eugene Vinitsky", "Communication Chair", "data/organizers/ev.jpg"),
new Organizer("Khurram Javed", "Communication Chair", "data/organizers/kj.png"),
new Organizer("Pablo Samuel Castro", "Inclusion Chair", "data/organizers/psc.png")
]

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


