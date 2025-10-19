// Dummy data for all dashboard tabs - used until actual integration is established

export const dummyOverviewData = {
  stats: [
    {
      label: "Outstanding Amount",
      value: "₹2,45,000",
      change: "+12% from last month",
      changeType: "negative",
      icon: "trending-down"
    },
    {
      label: "Collected This Month",
      value: "₹1,85,000",
      change: "+8% from last month",
      changeType: "positive",
      icon: "check-circle"
    },
    {
      label: "Collection Rate",
      value: "78%",
      change: "+5% improvement",
      changeType: "positive",
      icon: "bar-chart"
    },
    {
      label: "Overdue Accounts",
      value: "23",
      change: "-3 from last week",
      changeType: "positive",
      icon: "alert-circle"
    }
  ],
  cashFlowForecast: [
    { period: "Next 7 Days", label: "Expected collections", amount: "₹1,20,000" },
    { period: "Next 30 Days", label: "Projected collections", amount: "₹3,85,000" },
    { period: "Next Quarter", label: "Total forecast", amount: "₹12,50,000" }
  ],
  riskAssessment: [
    { risk: "High Risk", amount: "₹85,000", accounts: 8, color: "red", status: "Urgent" },
    { risk: "Medium Risk", amount: "₹1,20,000", accounts: 12, color: "orange", status: "Monitor" },
    { risk: "Low Risk", amount: "₹2,15,000", accounts: 35, color: "green", status: "Stable" }
  ],
  recentActions: [
    { action: "Payment reminder sent", company: "ABC Corp", details: "Invoice #INV-001", time: "2 hours ago" },
    { action: "Payment received", company: "XYZ Ltd", details: "₹45,000 paid", time: "5 hours ago" },
    { action: "Follow-up scheduled", company: "Tech Solutions", details: "Call on Friday", time: "1 day ago" }
  ]
};

export const dummyCollectionsData = {
  stats: [
    {
      label: "Today's Collections",
      value: "₹45,000",
      change: "3 payments received",
      icon: "check-circle"
    },
    {
      label: "This Week",
      value: "₹2,15,000",
      change: "+15% vs last week",
      changeType: "positive",
      icon: "trending-up"
    },
    {
      label: "Average Days to Pay",
      value: "18",
      change: "-2 days improvement",
      changeType: "positive",
      icon: "clock"
    },
    {
      label: "Success Rate",
      value: "85%",
      change: "AI-assisted collections",
      icon: "bar-chart"
    }
  ],
  recentCollections: [
    { company: "ABC Enterprises", invoice: "#INV-001", amount: "₹25,000", status: "Auto-reminder sent", time: "2 hours ago" },
    { company: "XYZ Solutions", invoice: "#INV-002", amount: "₹15,000", status: "Payment plan completed", time: "5 hours ago" },
    { company: "Tech Innovations", invoice: "#INV-003", amount: "₹35,000", status: "Direct payment", time: "1 day ago" }
  ],
  priorityCollections: [
    { company: "Global Corp", amount: "₹45,000", dueDate: "Due: 15 days ago", status: "AI escalation scheduled", priority: "high" },
    { company: "Smart Systems", amount: "₹28,000", dueDate: "Due: 8 days ago", status: "Payment plan offered", priority: "medium" },
    { company: "Future Tech", amount: "₹18,000", dueDate: "Due: 3 days ago", status: "Follow-up scheduled", priority: "low" }
  ]
};

export const dummyReconciliationData = {
  stats: [
    {
      label: "Reconciled Today",
      value: "₹85,000",
      change: "12 transactions",
      icon: "check-circle"
    },
    {
      label: "Pending Reconciliation",
      value: "₹32,000",
      change: "5 transactions",
      icon: "clock"
    },
    {
      label: "Auto-Reconciled",
      value: "94%",
      change: "AI efficiency rate",
      icon: "robot"
    },
    {
      label: "Discrepancies",
      value: "2",
      change: "Requires attention",
      icon: "alert-circle"
    }
  ],
  timeline: [
    { batch: "Morning Batch", time: "8:00 AM", amount: "₹45,000", status: "Complete", statusType: "success" },
    { batch: "Afternoon Batch", time: "2:00 PM", amount: "₹28,000", status: "In Progress", statusType: "processing" },
    { batch: "Evening Batch", time: "6:00 PM", amount: "₹12,000", status: "Pending", statusType: "pending" }
  ],
  issues: [
    { type: "Amount Mismatch", invoice: "#INV-045", details: "Expected ₹15,000, Received ₹14,500", note: "Requires manual review", severity: "high" },
    { type: "Missing Reference", transaction: "₹8,500", details: "Bank transaction without invoice reference", note: "AI attempting to match", severity: "medium" }
  ]
};

export const dummyAnalyticsData = {
  stats: [
    {
      label: "DSO (Days Sales Outstanding)",
      value: "24",
      change: "-3 days vs last month",
      changeType: "positive",
      icon: "clock"
    },
    {
      label: "Bad Debt Ratio",
      value: "2.1%",
      change: "-0.5% improvement",
      changeType: "positive",
      icon: "trending-down"
    },
    {
      label: "Collection Efficiency",
      value: "89%",
      change: "+7% this quarter",
      changeType: "positive",
      icon: "zap"
    },
    {
      label: "AI Impact Score",
      value: "92",
      change: "Excellent performance",
      icon: "sparkles"
    }
  ],
  performanceTrends: [
    { period: "This Week", rate: 80, color: "green" },
    { period: "Last Week", rate: 70, color: "blue" },
    { period: "Last Month", rate: 60, color: "orange" },
    { period: "Quarter Average", rate: 75, color: "purple" }
  ],
  customerBehavior: [
    { category: "Excellent Payers", description: "Pay within 7 days", volume: "₹8.5L", percentage: "45%" },
    { category: "Good Payers", description: "Pay within 30 days", volume: "₹6.2L", percentage: "35%" },
    { category: "Slow Payers", description: "Pay after 30 days", volume: "₹3.8L", percentage: "20%" }
  ],
  recommendations: [
    { title: "Optimize follow-up timing", description: "Data suggests Tuesday mornings get 23% better response", priority: "high" },
    { title: "Personalize communication", description: "Customers in Tech industry prefer email over calls", priority: "medium" },
    { title: "Offer early payment incentives", description: "2% discount could improve DSO by 5 days", priority: "low" }
  ]
};

export const dummyCommunicationData = {
  stats: [
    {
      label: "Messages Sent Today",
      value: "47",
      change: "+12 from yesterday",
      icon: "mail"
    },
    {
      label: "Response Rate",
      value: "78%",
      change: "+5% this week",
      changeType: "positive",
      icon: "trending-up"
    },
    {
      label: "Avg Response Time",
      value: "2.4h",
      change: "-0.8h improvement",
      changeType: "positive",
      icon: "clock"
    },
    {
      label: "Success Rate",
      value: "65%",
      change: "Payment after contact",
      icon: "check-circle"
    }
  ],
  recentCommunications: [
    { type: "AI Reminder Sent", company: "ABC Enterprises", invoice: "#INV-001", message: "Personalized payment reminder with payment link", time: "2 hours ago", icon: "mail" },
    { type: "Customer Response", company: "XYZ Solutions", message: "Payment will be processed by end of day", time: "3 hours ago", icon: "message-square" },
    { type: "Escalation Notice", company: "Global Corp", invoice: "Final notice", message: "Legal action warning for ₹45,000 overdue", time: "5 hours ago", icon: "alert-circle" }
  ],
  channels: [
    { name: "Email", description: "Primary channel", successRate: "85%", icon: "mail" },
    { name: "WhatsApp", description: "Quick responses", successRate: "92%", icon: "message-circle" },
    { name: "SMS", description: "Urgent reminders", successRate: "78%", icon: "smartphone" }
  ]
};