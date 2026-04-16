"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { aiService } from "@/services/ai.service";
import { useToast } from "@/hooks/use-toast";
import { Sparkles, Send, Loader2, CheckCircle, Store } from "lucide-react";
import { useRouter } from "next/navigation";

interface Message {
  role: "user" | "assistant";
  content: string;
  data?: any;
}

export default function AIPage() {
  const router = useRouter();
  const { toast } = useToast();
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hi! I'm your AI store builder. Tell me what kind of store you want to create, and I'll build it for you automatically!\n\nFor example:\n• \"I want a sports clothing store\"\n• \"organic coffee shop\"\n• \"handmade jewelry\"\n• \"pet supplies\"",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setLoading(true);

    try {
      // Add loading message
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "⚙️ Creating your store...\n\nPlease wait while I:\n✓ Generate store structure\n✓ Create categories\n✓ Generate products\n✓ Set up everything for you",
        },
      ]);

      // Call AI service to create automated store
      const response = await aiService.createAutomatedStore(userMessage);

      // Remove loading message and add success message
      setMessages((prev) => {
        const withoutLoading = prev.slice(0, -1);
        return [
          ...withoutLoading,
          {
            role: "assistant",
            content: `🎉 ${response.message}\n\n**Store Details:**\n• Name: ${response.store.name}\n• Products: ${response.summary.total_products}\n• Categories: ${response.summary.total_categories}\n• Status: ${response.store.status}\n\n**What's been created:**\n${response.categories.map((cat: any) => `✓ ${cat.name}`).join("\n")}\n\n${response.products.slice(0, 3).map((prod: any) => `✓ ${prod.name} - $${prod.price}`).join("\n")}\n${response.products.length > 3 ? `\n...and ${response.products.length - 3} more products!` : ""}\n\nYour store is ready to go! Would you like to:\n• View your store\n• Add more products\n• Customize products`,
            data: response,
          },
        ];
      });

      toast({
        title: "Success!",
        description: `Store "${response.store.name}" created successfully!`,
      });
    } catch (error: any) {
      setMessages((prev) => {
        const withoutLoading = prev.slice(0, -1);
        return [
          ...withoutLoading,
          {
            role: "assistant",
            content: `❌ Oops! Something went wrong: ${error.message}\n\nPlease try again with a different description.`,
          },
        ];
      });

      toast({
        title: "Error",
        description: error.message || "Failed to create store",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleViewStore = (storeSlug: string) => {
    router.push(`/stores/${storeSlug}`);
  };

  const handleViewProducts = () => {
    router.push("/products");
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">AI Store Builder</h1>
        <p className="text-muted-foreground">
          Create a complete store with products in seconds using AI
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Chat Interface */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary" />
              AI Assistant
            </CardTitle>
          </CardHeader>
          <CardContent>
            {/* Messages */}
            <div className="space-y-4 mb-4 max-h-[500px] overflow-y-auto">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${
                    message.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg p-4 ${
                      message.role === "user"
                        ? "bg-primary text-primary-foreground"
                        : "bg-muted"
                    }`}
                  >
                    <div className="whitespace-pre-wrap text-sm">
                      {message.content}
                    </div>
                    {message.data && (
                      <div className="mt-4 space-y-2">
                        <Button
                          size="sm"
                          variant="secondary"
                          onClick={() => handleViewStore(message.data.store.slug)}
                          className="w-full gap-2"
                        >
                          <Store className="h-4 w-4" />
                          View Store
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={handleViewProducts}
                          className="w-full"
                        >
                          View Products
                        </Button>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* Input */}
            <form onSubmit={handleSubmit} className="flex gap-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Describe your store idea..."
                disabled={loading}
              />
              <Button type="submit" disabled={loading}>
                {loading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Send className="h-4 w-4" />
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Info Panel */}
        <Card>
          <CardHeader>
            <CardTitle>How It Works</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <div className="flex gap-3">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm font-bold">
                  1
                </div>
                <div>
                  <h4 className="font-semibold">Describe Your Store</h4>
                  <p className="text-sm text-muted-foreground">
                    Tell the AI what kind of store you want
                  </p>
                </div>
              </div>

              <div className="flex gap-3">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm font-bold">
                  2
                </div>
                <div>
                  <h4 className="font-semibold">AI Builds Everything</h4>
                  <p className="text-sm text-muted-foreground">
                    Store, categories, and products are created automatically
                  </p>
                </div>
              </div>

              <div className="flex gap-3">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm font-bold">
                  3
                </div>
                <div>
                  <h4 className="font-semibold">Customize & Launch</h4>
                  <p className="text-sm text-muted-foreground">
                    Review, customize, and publish your store
                  </p>
                </div>
              </div>
            </div>

            <div className="border-t pt-4">
              <h4 className="font-semibold mb-2">Example Ideas:</h4>
              <div className="space-y-2">
                {[
                  "Sports clothing store",
                  "Organic coffee shop",
                  "Handmade jewelry",
                  "Pet supplies",
                  "Vintage books",
                ].map((idea) => (
                  <Button
                    key={idea}
                    variant="outline"
                    size="sm"
                    className="w-full justify-start"
                    onClick={() => setInput(idea)}
                    disabled={loading}
                  >
                    {idea}
                  </Button>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
