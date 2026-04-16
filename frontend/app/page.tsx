import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, Sparkles, Store, Package, TrendingUp } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <Store className="h-6 w-6 text-primary" />
            <span className="text-xl font-bold">AI Ecommerce</span>
          </div>
          <nav className="hidden md:flex items-center gap-6">
            <Link href="/shop" className="text-sm font-medium hover:text-primary">
              Shop
            </Link>
            <Link href="#features" className="text-sm font-medium hover:text-primary">
              Features
            </Link>
            <Link href="#how-it-works" className="text-sm font-medium hover:text-primary">
              How It Works
            </Link>
            <Link href="/login" className="text-sm font-medium hover:text-primary">
              Login
            </Link>
            <Link href="/register">
              <Button>Get Started</Button>
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container flex flex-col items-center justify-center gap-8 py-24 md:py-32">
        <div className="flex flex-col items-center gap-4 text-center">
          <div className="inline-flex items-center gap-2 rounded-full border px-4 py-1.5 text-sm">
            <Sparkles className="h-4 w-4 text-primary" />
            <span>AI-Powered Store Creation</span>
          </div>
          <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl lg:text-7xl">
            Turn Your Idea Into a Store
            <br />
            <span className="text-primary">in 5 Minutes</span>
          </h1>
          <p className="max-w-[700px] text-lg text-muted-foreground sm:text-xl">
            AI-powered platform that transforms simple ideas into fully functional online stores.
            No coding required.
          </p>
          <div className="flex flex-col gap-4 sm:flex-row">
            <Link href="/register">
              <Button size="lg" className="gap-2">
                Start Building Free
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link href="#demo">
              <Button size="lg" variant="outline">
                Watch Demo
              </Button>
            </Link>
          </div>
          <div className="flex items-center gap-8 text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <span className="text-green-500">✓</span>
              <span>No coding required</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-green-500">✓</span>
              <span>AI-powered</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-green-500">✓</span>
              <span>Free to start</span>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="border-t bg-muted/50 py-24">
        <div className="container">
          <div className="flex flex-col items-center gap-4 text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
              How It Works
            </h2>
            <p className="max-w-[700px] text-lg text-muted-foreground">
              Three simple steps to launch your online store
            </p>
          </div>
          <div className="grid gap-8 md:grid-cols-3">
            <div className="flex flex-col items-center gap-4 text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary text-2xl font-bold text-primary-foreground">
                1
              </div>
              <h3 className="text-xl font-bold">Share Your Idea</h3>
              <p className="text-muted-foreground">
                Tell our AI what kind of store you want to create. Just a simple description is enough.
              </p>
            </div>
            <div className="flex flex-col items-center gap-4 text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary text-2xl font-bold text-primary-foreground">
                2
              </div>
              <h3 className="text-xl font-bold">AI Builds Your Store</h3>
              <p className="text-muted-foreground">
                Watch as AI creates your store with products, categories, and everything you need.
              </p>
            </div>
            <div className="flex flex-col items-center gap-4 text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary text-2xl font-bold text-primary-foreground">
                3
              </div>
              <h3 className="text-xl font-bold">Go Live & Sell</h3>
              <p className="text-muted-foreground">
                Your store is ready! Customize if needed and start selling to customers.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-24">
        <div className="container">
          <div className="flex flex-col items-center gap-4 text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
              Powerful Features
            </h2>
            <p className="max-w-[700px] text-lg text-muted-foreground">
              Everything you need to run a successful online store
            </p>
          </div>
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            <div className="flex flex-col gap-4 rounded-lg border p-6">
              <Sparkles className="h-10 w-10 text-primary" />
              <h3 className="text-xl font-bold">AI-Powered</h3>
              <p className="text-muted-foreground">
                Auto-generate products, descriptions, and SEO content with advanced AI.
              </p>
            </div>
            <div className="flex flex-col gap-4 rounded-lg border p-6">
              <Package className="h-10 w-10 text-primary" />
              <h3 className="text-xl font-bold">Unlimited Products</h3>
              <p className="text-muted-foreground">
                Add as many products as you want. No limits on your inventory.
              </p>
            </div>
            <div className="flex flex-col gap-4 rounded-lg border p-6">
              <TrendingUp className="h-10 w-10 text-primary" />
              <h3 className="text-xl font-bold">Analytics</h3>
              <p className="text-muted-foreground">
                Track sales, visitors, and performance with built-in analytics.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="border-t bg-muted/50 py-24">
        <div className="container flex flex-col items-center gap-8 text-center">
          <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
            Ready to Build Your Store?
          </h2>
          <p className="max-w-[600px] text-lg text-muted-foreground">
            Join thousands of entrepreneurs who have launched their stores with AI
          </p>
          <Link href="/register">
            <Button size="lg" className="gap-2">
              Get Started Free
              <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
          <p className="text-sm text-muted-foreground">No credit card required</p>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8">
        <div className="container flex flex-col items-center justify-between gap-4 md:flex-row">
          <div className="flex gap-4">
            <Link href="#" className="text-sm text-muted-foreground hover:text-primary">
              About
            </Link>
            <Link href="#" className="text-sm text-muted-foreground hover:text-primary">
              Contact
            </Link>
            <Link href="#" className="text-sm text-muted-foreground hover:text-primary">
              Terms
            </Link>
            <Link href="#" className="text-sm text-muted-foreground hover:text-primary">
              Privacy
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
