export const mockTeamMembers = [
  {
    id: 1,
    name: "Ajith",
    role: "CEO",
    description: "CS and CA Finalist with over a decade in compliance, taxation, and enterprise software sales.",
    image: "https://images.unsplash.com/photo-1576558656222-ba66febe3dec?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwxfHxwcm9mZXNzaW9uYWwlMjBidXNpbmVzcyUyMGhlYWRzaG90fGVufDB8fHx8MTc2MDg3ODUyNHww&ixlib=rb-4.1.0&q=85"
  },
  {
    id: 2,
    name: "Geerthivasan",
    role: "CTO",
    description: "Built high-performance engineering teams, drove $10M+ in new revenue with AI solutions.",
    image: "https://images.unsplash.com/photo-1652471943570-f3590a4e52ed?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwyfHxwcm9mZXNzaW9uYWwlMjBidXNpbmVzcyUyMGhlYWRzaG90fGVufDB8fHx8MTc2MDg3ODUyNHww&ixlib=rb-4.1.0&q=85"
  },
  {
    id: 3,
    name: "Arunoday",
    role: "Head of SE",
    description: "Led development of secure, scalable enterprise platforms with full-stack expertise.",
    image: "https://images.unsplash.com/photo-1655249493799-9cee4fe983bb?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwzfHxwcm9mZXNzaW9uYWwlMjBidXNpbmVzcyUyMGhlYWRzaG90fGVufDB8fHx8MTc2MDg3ODUyNHww&ixlib=rb-4.1.0&q=85"
  },
  {
    id: 4,
    name: "Srivatsa",
    role: "Head of AI",
    description: "14 years in AI/Data Science, delivered patented globally deployed AI solutions.",
    image: "https://images.pexels.com/photos/2182970/pexels-photo-2182970.jpeg"
  }
];

export const mockAgents = [
  {
    id: "orchestrator",
    name: "Orchestrator Agent",
    icon: "briefcase",
    color: "green",
    description: "Master controller activating and coordinating all other agents to optimize the collections portfolio.",
    details: "The Orchestrator Agent is the central brain of Vasool's multi-agent system. It continuously monitors portfolio performance, activates relevant agents based on debtor profiles, and coordinates their actions to maximize recovery efficiency."
  },
  {
    id: "analyst",
    name: "Analyst Agent",
    icon: "trending-up",
    color: "green",
    description: "Ingests real-time debtor data, creating dynamic risk profiles based on willingness and ability to pay.",
    details: "Using advanced machine learning models, the Analyst Agent processes transaction history, payment patterns, and behavioral signals to create comprehensive risk profiles that enable targeted collection strategies."
  },
  {
    id: "strategist",
    name: "Strategist Agent",
    icon: "zap",
    color: "green",
    description: "Designs hyper-personalized outreach strategies, determining optimal channel, timing, and tone.",
    details: "The Strategist Agent leverages AI to craft personalized collection strategies, selecting the right communication channel, optimal timing, and appropriate tone based on each debtor's profile and preferences."
  },
  {
    id: "communication",
    name: "Communication Agent",
    icon: "users",
    color: "green",
    description: "Engages debtors with empathetic dialogue, negotiating terms and processing payments autonomously.",
    details: "Through natural language processing and empathetic AI, the Communication Agent engages in human-like conversations, understanding debtor concerns and negotiating payment plans while maintaining positive relationships."
  },
  {
    id: "reconciliation",
    name: "Reconciliation Agent",
    icon: "check-circle",
    color: "green",
    description: "Automates payment tracking, matches payments to accounts, and flags discrepancies.",
    details: "The Reconciliation Agent ensures accuracy by automatically matching incoming payments to outstanding debts, identifying discrepancies, and maintaining real-time portfolio updates across all systems."
  },
  {
    id: "compliance",
    name: "Compliance Agent",
    icon: "shield",
    color: "red",
    description: "Ensures all actions adhere strictly to RBI guidelines, providing an immutable audit trail.",
    details: "Every action taken by the platform is validated by the Compliance Agent against regulatory requirements, creating an immutable audit trail and ensuring full adherence to RBI guidelines and legal standards."
  }
];

export const mockChatMessages = [
  {
    id: 1,
    sender: "assistant",
    message: "Hello! I'm your AI Collections Assistant. I can help you analyze your portfolio, track payments, and optimize your collection strategies. What would you like to know?",
    timestamp: new Date().toISOString()
  }
];

export const mockUser = {
  email: "abc@test.com",
  password: "test",
  name: "Test User"
};