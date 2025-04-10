/////// HOME PAGE ///////

var listOfPapers = ["RL algorithms (e.g., new algorithms for existing settings and new settings)", "Hierarchical RL (e.g., skill discovery, hierarchical representations and abstractions)",
"Exploration (e.g., intrinsic motivation, curiosity-driven learning, exploration-exploitation tradeoff)", "Theoretical RL (e.g., complexity results, convergence analysis)",
"Social and economic aspects (e.g., safety, fairness, interpretability, privacy, trustworthiness, human-AI interaction, philosophy)",
"Bandit algorithms (e.g., theoretical contributions, practical algorithms)",
"Planning algorithms (e.g., decision-making under uncertainty, model-based approaches)",
"Foundations (e.g., showing relationships between methods, unifying theory, clarifying misconceptions in the literature)",
"Evaluation (e.g., methodology, meta studies, replicability, and validity)",
"Applied reinforcement learning (e.g., medical, operations, traffic)",
"Deep reinforcement learning (e.g., analysis on the interplay between RL and deep learning models)",
"Multi-agent RL (e.g., cooperative, competitive, self-play, etc)",
"Multidisciplinary work (RL research that relates to other fields)",
"RL Systems (e.g., distributed training, multi-GPU training)",
"RL from human feedback (e.g. reward learning from human data, human-in-the-loop learning, etc.)"]

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
   new  AdvisoryCommittee("Balaraman Ravindran", "IIT Madras", "data/advisoryCom/br_1.jpg"),
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
    new MenuItem("Home", "index.html"),
    new MenuItemWithSubmenu("Program", [ new MenuItem("Accepted&nbspWorkshops", "accepted_workshops.html")]),
    // new MenuItem("Submit", "#"),
    // new MenuItem("Attend", "#"),
    // new MenuItem("Organizers", "#"),

    // new MenuItemWithSubmenu("Year", [ new MenuItem("2024", "2024/index.html"), new MenuItem("2025", "index.html")] ),
    new MenuItemWithSubmenu("Submit", [new MenuItem("Call&nbspfor&nbspPapers", "callforpapers.html"), new MenuItem("Call&nbspfor&nbspWorkshops", "callforworkshops.html"), new MenuItem("Submission&nbspInstructions", "submissionInstructions.html") , new MenuItem("Review&nbspInstructions", "https://docs.google.com/document/d/1ZGDiRiAjfkTZCS36e9h4qwITYBDfLAxBltR4Kd0IXAE/edit?usp=sharing"), new MenuItem("Journal&nbspto&nbspConference", "https://docs.google.com/forms/d/e/1FAIpQLScpQ4WRsQa9MEki8B7lZbh2GGAnycPqjtS8-CIHmWgg49RwIg/viewform")] ),
    new MenuItemWithSubmenu("Attend", [new MenuItem("Registration", "register.html"),  new MenuItem("Accommodation", "hotels.html"), new MenuItem("Code&nbspof&nbspConduct", "code_of_conduct.html")] ),
    new MenuItemWithSubmenu("Participate", [new MenuItem("Review&nbsp(Self&nbspNomination)", "participate.html"),  new MenuItem("Sponsor", "sponsors.html")] ),
    new MenuItemWithSubmenu("Organizers", [new MenuItem("Organizers", "organizers.html"),  new MenuItem("Advisors", "advisors.html"),  new MenuItem("Reviewers", "reviewers.html")] ),
    new MenuItemWithSubmenu("Year", [new MenuItem("2024", "/2024/index.html"),  new MenuItem("2025", "index.html")] ),
    new MenuItem("Contact&nbspUs", "contact.html"),
    // new MenuItem("Register", "#"),
    // new MenuItem("Attend", "#"),
    // new MenuItem("Organizers", "#"),
    // new MenuItem("FAQ", "#"),
    // new MenuItem("Blogs", "#"),
    // new MenuItem("Sponsors", "#")
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
    new Organizer("Scott Jordan", "Keynote and Scheduling Chair", "data/organizers/sj.webp"),
    new Organizer("Roberta Raileanu", "Awards Chair", "data/organizers/rr.jpg"),
    new Organizer("Martha White", "Local Chair", "data/organizers/mw.webp"),
    new Organizer("Mike Bowling", "Local Chair", "data/organizers/mb.jpg"),
    new Organizer("Patrick Pilarski", "Local and Volunteers Chair", "data/organizers/pp.jpg"),
    new Organizer("Glen Berseth", "Sponsorship Chair", "data/organizers/gb.webp"),
    new Organizer("Audrey Durand", "Sponsorship Chair", "data/organizers/ad.jpg"),
    new Organizer("Josiah Hanna", "Workshop Chair", "data/organizers/jh.jpeg"),
    new Organizer("Claire Vernade", "Workshop Chair", "data/organizers/cv.jpg"),
    new Organizer("Eugene Vinitsky", "Communication Chair", "data/organizers/ev.jpg"),
    new Organizer("Khurram Javed", "Communication Chair", "data/organizers/kj.png"),
    new Organizer("Pablo Samuel Castro", "Inclusion Chair", "data/organizers/psc.png")
]

class Workshop {
    constructor(name, link, description) {
        this.name = name;
        this.link = link;
        this.description = description;
    }
}

//
// listOfGeneralChair = [new Organizer("Adam White", "General Chair", "data/organizers/aw.jpg")]
//
// listOfProgramChairs = [new Organizer("Phil Thomas", "Program Chair", "data/organizers/pt.jpg"),
//     new Organizer("Marlos C Machado", "Program Chair", "data/organizers/mcm.jpg"),
//     new Organizer("Cathy Wu", "Program Chair", "data/organizers/cw.jpg"),
//     new Organizer("Andrew Patterson", "Program Chair", "data/organizers/ap.jpg")]
//
// listOfLocalChairs = [new Organizer("Martha White", "Local Chair", "data/organizers/mw.jpg"),
//     new Organizer("Mike Bowling", "Local Chair", "data/organizers/mb.jpg"),
//     new Organizer("Patrick Pilarski", "Local Chair", "data/organizers/pp.jpg")]
//
// listOfWorkshopChairs = [new Organizer("Josiah Hanna", "Workshop Chair", "data/organizers/jh.jpg"),
//     new Organizer("Claire Vernade", "Workshop Chair", "data/organizers/cv.jpg")]
//
// listOfCommsChairs = [new Organizer("Khurram Javed", "Comms & Website", "data/organizers/kj.jpg"),
//     new Organizer("Eugene Vinitsky", "Comms & Website", "data/organizers/ev.jpg")]
//
// listOfIncludeChairs = [new Organizer("Pablo Samuel Castro", "Inclusion Chair", "data/organizers/psc.jpg")]
//
// listOfSponsorshipChairs = [new Organizer("Glen Berseth", "Sponsorship Chair", "data/organizers/gb.jpg"),
//     new Organizer("Audrey Durand", "Sponsorship Chair", "data/organizers/ad.jpg")]
//
// listOfKeynoteChairs = [new Organizer("Brad Knox", "Keynote and Scheduling Chair", "data/organizers/bk.jpg"),
//     new Organizer("Tom Schaul", "Keynote and Scheduling Chair", "data/organizers/ts.jpg"),
//     new Organizer("Scott Jordan", "Keynote and Scheduling Chair", "data/organizers/sj.jpg")]
//
// listOfAwardsChairs = [new Organizer("Roberta Raileanu", "Awards Chair", "data/organizers/rr.jpg")]



