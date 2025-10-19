import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { toast } from '../hooks/use-toast';
import { mockTeamMembers, mockAgents } from '../mockData';
import { TrendingUp, Shield, Users, CheckCircle2, Briefcase, Zap, ArrowRight, PlayCircle } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const iconMap = {
  'briefcase': Briefcase,
  'trending-up': TrendingUp,
  'zap': Zap,
  'users': Users,
  'check-circle': CheckCircle2,
  'shield': Shield
};

const Landing = () => {
  const navigate = useNavigate();
  const [demoFormOpen, setDemoFormOpen] = useState(false);
  const [videoOpen, setVideoOpen] = useState(false);
  const [demoForm, setDemoForm] = useState({ name: '', email: '', company: '', phone: '' });
  const [salesForm, setSalesForm] = useState({ name: '', email: '', message: '' });

  const handleDemoSubmit = async (e) => {
    e.preventDefault();
    try {
      await demoContactAPI.scheduleDemo(demoForm);
      toast({
        title: "Demo Scheduled!",
        description: "We'll contact you shortly to schedule your demo.",
      });
      setDemoFormOpen(false);
      setDemoForm({ name: '', email: '', company: '', phone: '' });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to schedule demo. Please try again.",
        variant: "destructive",
      });
    }
  };

  const handleSalesSubmit = async (e) => {
    e.preventDefault();
    try {
      await demoContactAPI.contactSales(salesForm);
      toast({
        title: "Message Sent!",
        description: "Our sales team will reach out to you soon.",
      });
      setSalesForm({ name: '', email: '', message: '' });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to send message. Please try again.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <Navbar />

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <div className="mb-6">
            <span className="inline-block px-4 py-2 bg-green-50 text-green-700 rounded-full text-sm font-medium">
              AI-Powered Fintech Innovation
            </span>
          </div>
          <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
            Revolutionizing
            <br />
            Credit Collections
            <br />
            with <span className="text-green-600">AI Intelligence</span>
          </h1>
          <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
            Transform how businesses recover payments through our multi-agent AI platform. 
            Achieve 30-40% faster collections while preserving valuable customer relationships.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              size="lg" 
              className="bg-green-600 hover:bg-green-700 text-white px-8 py-6 text-lg"
              onClick={() => navigate('/signup')}
            >
              Get Started
              <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
            <Button 
              size="lg" 
              variant="outline" 
              className="border-gray-300 px-8 py-6 text-lg"
              onClick={() => setVideoOpen(true)}
            >
              <PlayCircle className="mr-2 w-5 h-5" />
              Watch Demo
            </Button>
          </div>
          <p className="mt-8 text-gray-500">
            Addressing a <span className="font-bold text-gray-900">$60B+ annual loss</span> in the Indian MSME market
          </p>
        </div>
      </section>

      {/* Challenge Section */}
      <section id="solution" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid md:grid-cols-2 gap-12">
            <div>
              <h2 className="text-4xl font-bold mb-12">The Challenge We Address</h2>
              <div className="space-y-6">
                <Card className="border-l-4 border-l-red-500">
                  <CardHeader>
                    <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-3">
                      <TrendingUp className="w-6 h-6 text-red-600" />
                    </div>
                    <CardTitle>$60B+ Annual Losses</CardTitle>
                    <CardDescription>
                      Indian MSMEs and lenders lose billions due to inefficient debt recovery processes.
                    </CardDescription>
                  </CardHeader>
                </Card>
                <Card className="border-l-4 border-l-orange-500">
                  <CardHeader>
                    <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mb-3">
                      <TrendingUp className="w-6 h-6 text-orange-600" />
                    </div>
                    <CardTitle>70% Unresolved Debt</CardTitle>
                    <CardDescription>
                      Overdue payments remain unresolved beyond 90 days, creating cash flow problems.
                    </CardDescription>
                  </CardHeader>
                </Card>
                <Card className="border-l-4 border-l-yellow-500">
                  <CardHeader>
                    <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mb-3">
                      <Shield className="w-6 h-6 text-yellow-600" />
                    </div>
                    <CardTitle>100% Manual Methods</CardTitle>
                    <CardDescription>
                      Traditional methods are entirely manual, opaque, and damage customer relationships.
                    </CardDescription>
                  </CardHeader>
                </Card>
              </div>
            </div>

            <div>
              <Card className="bg-gradient-to-br from-green-50 to-green-100 border-green-200 h-full">
                <CardHeader>
                  <CardTitle className="text-green-800 text-3xl">Our Solution</CardTitle>
                  <CardDescription className="text-green-700 text-base">
                    Vasool's multi-agent AI platform automates the entire debt recovery lifecycle, 
                    from predictive analytics to empathetic communication and smart escalation.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-3">
                    <li className="flex items-start">
                      <CheckCircle2 className="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" />
                      <span className="text-green-800">Autonomous AI agents working together</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle2 className="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" />
                      <span className="text-green-800">Preserves customer relationships</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle2 className="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" />
                      <span className="text-green-800">30-40% faster collection cycles</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle2 className="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" />
                      <span className="text-green-800">RBI compliant and secure</span>
                    </li>
                  </ul>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Multi-Agent Platform Section */}
      <section id="technology" className="py-20">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Multi-Agent AI Platform</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Six specialized AI agents work together, managed by a central orchestrator, 
              to handle the end-to-end collections lifecycle.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockAgents.map((agent) => {
              const IconComponent = iconMap[agent.icon];
              return (
                <Card 
                  key={agent.id} 
                  className="hover:shadow-lg transition-all duration-300 cursor-pointer group"
                  onClick={() => navigate(`/agent/${agent.id}`)}
                >
                  <CardHeader>
                    <div className={`w-12 h-12 bg-${agent.color === 'green' ? 'green' : 'red'}-100 rounded-lg flex items-center justify-center mb-3 group-hover:scale-110 transition-transform`}>
                      <IconComponent className={`w-6 h-6 text-${agent.color === 'green' ? 'green' : 'red'}-600`} />
                    </div>
                    <CardTitle className="group-hover:text-green-600 transition-colors">{agent.name}</CardTitle>
                    <CardDescription>{agent.description}</CardDescription>
                  </CardHeader>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Why Choose Vasool Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Why Choose Vasool</h2>
            <p className="text-xl text-gray-600">
              Beyond automation - intelligent, adaptive, and relationship-preserving collections
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <Card>
              <CardHeader>
                <CardTitle className="text-2xl">Agentic AI Power</CardTitle>
                <CardDescription className="text-base">
                  Our multi-agent system intelligently negotiates, adapts, and learns, 
                  significantly boosting recovery rates beyond simple automation.
                </CardDescription>
              </CardHeader>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="text-2xl">Relationship-First Approach</CardTitle>
                <CardDescription className="text-base">
                  Prioritize preserving customer relationships through empathetic communication 
                  and dedicated self-service portals.
                </CardDescription>
              </CardHeader>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="text-2xl">Predictive Intelligence</CardTitle>
                <CardDescription className="text-base">
                  Proactive risk profiling and payment forecasting enable timely, targeted interventions, 
                  preventing defaults before they occur.
                </CardDescription>
              </CardHeader>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="text-2xl">Built-in Compliance</CardTitle>
                <CardDescription className="text-base">
                  All interactions adhere strictly to regulatory guidelines, reducing legal risks 
                  and ensuring audit compliance.
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section id="team" className="py-20">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">The Team Behind Vasool</h2>
            <p className="text-xl text-gray-600">
              Experienced leaders combining fintech expertise with cutting-edge AI innovation
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {mockTeamMembers.map((member) => (
              <Card key={member.id} className="text-center">
                <CardHeader>
                  <div className="flex justify-center mb-4">
                    <img
                      src={member.image}
                      alt={member.name}
                      className="w-32 h-32 rounded-full object-cover border-4 border-green-100"
                    />
                  </div>
                  <CardTitle className="text-xl">{member.name}</CardTitle>
                  <p className="text-green-600 font-semibold mb-3">{member.role}</p>
                  <CardDescription className="text-sm">{member.description}</CardDescription>
                </CardHeader>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-green-500 to-green-600">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Transform Your Collections?
          </h2>
          <p className="text-xl text-green-50 mb-10">
            Join the revolution in credit collections. Experience 30-40% faster recovery 
            while preserving your valuable customer relationships.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Dialog open={demoFormOpen} onOpenChange={setDemoFormOpen}>
              <DialogTrigger asChild>
                <Button size="lg" className="bg-white text-green-600 hover:bg-gray-100 px-8 py-6 text-lg">
                  Schedule Demo
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[500px]">
                <DialogHeader>
                  <DialogTitle>Schedule a Demo</DialogTitle>
                  <DialogDescription>
                    Fill out the form below and we'll contact you to schedule your personalized demo.
                  </DialogDescription>
                </DialogHeader>
                <form onSubmit={handleDemoSubmit} className="space-y-4 mt-4">
                  <div>
                    <Label htmlFor="demo-name">Name</Label>
                    <Input
                      id="demo-name"
                      value={demoForm.name}
                      onChange={(e) => setDemoForm({ ...demoForm, name: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="demo-email">Email</Label>
                    <Input
                      id="demo-email"
                      type="email"
                      value={demoForm.email}
                      onChange={(e) => setDemoForm({ ...demoForm, email: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="demo-company">Company</Label>
                    <Input
                      id="demo-company"
                      value={demoForm.company}
                      onChange={(e) => setDemoForm({ ...demoForm, company: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="demo-phone">Phone</Label>
                    <Input
                      id="demo-phone"
                      type="tel"
                      value={demoForm.phone}
                      onChange={(e) => setDemoForm({ ...demoForm, phone: e.target.value })}
                      required
                    />
                  </div>
                  <Button type="submit" className="w-full bg-green-600 hover:bg-green-700">
                    Submit
                  </Button>
                </form>
              </DialogContent>
            </Dialog>

            <Dialog>
              <DialogTrigger asChild>
                <Button 
                  size="lg" 
                  variant="outline" 
                  className="border-white text-white hover:bg-white/10 px-8 py-6 text-lg"
                >
                  Contact Sales
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[500px]">
                <DialogHeader>
                  <DialogTitle>Contact Sales</DialogTitle>
                  <DialogDescription>
                    Our sales team will get back to you within 24 hours.
                  </DialogDescription>
                </DialogHeader>
                <form onSubmit={handleSalesSubmit} className="space-y-4 mt-4">
                  <div>
                    <Label htmlFor="sales-name">Name</Label>
                    <Input
                      id="sales-name"
                      value={salesForm.name}
                      onChange={(e) => setSalesForm({ ...salesForm, name: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="sales-email">Email</Label>
                    <Input
                      id="sales-email"
                      type="email"
                      value={salesForm.email}
                      onChange={(e) => setSalesForm({ ...salesForm, email: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="sales-message">Message</Label>
                    <Textarea
                      id="sales-message"
                      value={salesForm.message}
                      onChange={(e) => setSalesForm({ ...salesForm, message: e.target.value })}
                      rows={4}
                      required
                    />
                  </div>
                  <Button type="submit" className="w-full bg-green-600 hover:bg-green-700">
                    Send Message
                  </Button>
                </form>
              </DialogContent>
            </Dialog>
          </div>
        </div>
      </section>

      {/* Video Modal */}
      <Dialog open={videoOpen} onOpenChange={setVideoOpen}>
        <DialogContent className="sm:max-w-[800px]">
          <DialogHeader>
            <DialogTitle>Vasool Platform Demo</DialogTitle>
          </DialogHeader>
          <div className="aspect-video bg-gray-100 rounded-lg flex items-center justify-center">
            <p className="text-gray-500">Demo video would be embedded here</p>
          </div>
        </DialogContent>
      </Dialog>

      <Footer />
    </div>
  );
};

export default Landing;