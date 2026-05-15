"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Search, Sparkles, ShoppingBag, Loader2, X, MessageCircle } from "lucide-react";
import Link from "next/link";
import { formatPrice } from "@/lib/utils";

export default function ShopPage() {
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [filteredProducts, setFilteredProducts] = useState<any[]>([]);
  
  // AI Assistant State
  const [showAI, setShowAI] = useState(false);
  const [aiQuery, setAiQuery] = useState("");
  const [aiLoading, setAiLoading] = useState(false);
  const [aiResult, setAiResult] = useState<any>(null);

  useEffect(() => {
    fetchProducts();
  }, []);

  useEffect(() => {
    if (searchQuery) {
      const filtered = products.filter((product) =>
        product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        product.description?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        product.category?.name?.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setFilteredProducts(filtered);
    } else {
      setFilteredProducts(products);
    }
  }, [searchQuery, products]);

  const fetchProducts = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/products/');
      const data = await response.json();
      const productsArray = Array.isArray(data) ? data : (data.results || []);
      setProducts(productsArray);
      setFilteredProducts(productsArray);
    } catch (error) {
      console.error('Failed to fetch products:', error);
      setProducts([]);
      setFilteredProducts([]);
    } finally {
      setLoading(false);
    }
  };

  const handleAISearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!aiQuery.trim()) return;

    setAiLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/ai/search/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: aiQuery }),
      });

      const data = await response.json();
      setAiResult(data);
      
      // Update displayed products with AI results
      if (data.products && data.products.length > 0) {
        setFilteredProducts(data.products);
        // Scroll to products
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else {
        // If no AI results, show all products
        setFilteredProducts(products);
      }
    } catch (error) {
      console.error('AI search failed:', error);
      setAiResult({
        success: false,
        ai_response: 'Sorry, search is temporarily unavailable. Please try again later.',
        products: [],
      });
      // Show all products on error
      setFilteredProducts(products);
    } finally {
      setAiLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b sticky top-0 bg-background z-40">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center gap-2">
              <ShoppingBag className="h-6 w-6" />
              <span className="text-xl font-bold">AI Shop</span>
            </Link>
            <div className="flex items-center gap-4">
              <Link href="/shop/cart">
                <Button variant="outline" className="relative">
                  <ShoppingBag className="h-5 w-5 mr-2" />
                  Cart
                </Button>
              </Link>
              <Link href="/login">
                <Button variant="outline">Seller Login</Button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Search Bar */}
        <div className="mb-8">
          <div className="relative max-w-2xl mx-auto">
            <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
            <Input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search for products..."
              className="pl-10 h-12"
            />
          </div>
        </div>

        {/* Products Grid */}
        {loading ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
              <Card key={i} className="overflow-hidden">
                <div className="aspect-square bg-muted animate-pulse" />
                <CardHeader>
                  <div className="h-4 bg-muted animate-pulse rounded" />
                </CardHeader>
                <CardContent>
                  <div className="h-8 bg-muted animate-pulse rounded" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : filteredProducts.length === 0 ? (
          <Card>
            <CardContent className="py-16 text-center">
              <ShoppingBag className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
              <h3 className="text-lg font-semibold mb-2">No products found</h3>
              <p className="text-muted-foreground mb-4">
                {searchQuery ? "We couldn't find any products matching your search" : "No products available at the moment"}
              </p>
              {searchQuery && (
                <Button variant="outline" onClick={() => setSearchQuery("")}>
                  Clear Search
                </Button>
              )}
            </CardContent>
          </Card>
        ) : (
          <>
            <div className="mb-4 flex items-center justify-between">
              <p className="text-muted-foreground">
                {filteredProducts.length} product{filteredProducts.length !== 1 ? 's' : ''}
              </p>
              {(searchQuery || aiResult) && (
                <Button 
                  variant="outline" 
                  size="sm"
                  onClick={() => {
                    setSearchQuery("");
                    setAiResult(null);
                    setFilteredProducts(products);
                  }}
                >
                  Show All Products
                </Button>
              )}
            </div>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {filteredProducts.map((product: any) => (
                <Link key={product.id} href={`/shop/${product.slug}`}>
                  <Card className="overflow-hidden hover:shadow-lg transition-shadow cursor-pointer h-full">
                    <div className="aspect-square bg-muted flex items-center justify-center relative">
                      {product.images && product.images.length > 0 ? (
                        <img
                          src={product.images[0].image}
                          alt={product.name}
                          className="h-full w-full object-cover"
                        />
                      ) : (
                        <ShoppingBag className="h-12 w-12 text-muted-foreground" />
                      )}
                      {/* Stock Badge */}
                      {product.stock_quantity === 0 && (
                        <div className="absolute top-2 right-2">
                          <Badge variant="destructive">Out of Stock</Badge>
                        </div>
                      )}
                      {product.stock_quantity > 0 && product.stock_quantity <= 5 && (
                        <div className="absolute top-2 right-2">
                          <Badge className="bg-orange-600">Low Stock</Badge>
                        </div>
                      )}
                    </div>
                    <CardHeader>
                      <div className="space-y-2">
                        <CardTitle className="line-clamp-2 text-base">
                          {product.name}
                        </CardTitle>
                        {product.category && (
                          <Badge variant="secondary" className="text-xs">
                            {product.category.name}
                          </Badge>
                        )}
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        <p className="text-sm text-muted-foreground line-clamp-2">
                          {product.short_description || product.description}
                        </p>
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="text-xl font-bold">{formatPrice(product.price)}</p>
                              {product.compare_price && parseFloat(product.compare_price) > parseFloat(product.price) && (
                                <p className="text-xs text-muted-foreground line-through">
                                  {formatPrice(product.compare_price)}
                                </p>
                              )}
                            </div>
                            <Button size="sm" onClick={(e) => e.preventDefault()}>View</Button>
                          </div>
                          {/* Stock Info */}
                          <div className="text-xs text-muted-foreground">
                            {product.stock_quantity > 0 ? (
                              <span className={product.stock_quantity <= 5 ? "text-orange-600" : "text-green-600"}>
                                {product.stock_quantity} in stock
                              </span>
                            ) : (
                              <span className="text-red-600">Out of stock</span>
                            )}
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              ))}
            </div>
          </>
        )}
      </main>

      {/* AI Assistant Button */}
      <button
        onClick={() => setShowAI(!showAI)}
        className="fixed bottom-6 right-6 h-14 w-14 rounded-full bg-primary text-primary-foreground shadow-lg hover:shadow-xl transition-all hover:scale-110 flex items-center justify-center z-50"
        aria-label="AI Assistant"
      >
        {showAI ? (
          <X className="h-6 w-6" />
        ) : (
          <Sparkles className="h-6 w-6" />
        )}
      </button>

      {/* AI Assistant Panel */}
      {showAI && (
        <div className="fixed bottom-24 right-6 w-96 max-w-[calc(100vw-3rem)] bg-background border rounded-lg shadow-2xl z-50 overflow-hidden">
          <div className="bg-primary text-primary-foreground p-4 flex items-center gap-2">
            <Sparkles className="h-5 w-5" />
            <h3 className="font-semibold">AI Shopping Assistant</h3>
          </div>
          
          <div className="p-4 space-y-4 max-h-[500px] overflow-y-auto">
            {/* AI Response */}
            {aiResult && (
              <div className="bg-muted p-3 rounded-lg">
                <div className="flex items-start gap-2 mb-2">
                  <MessageCircle className="h-4 w-4 text-primary mt-1 flex-shrink-0" />
                  <p className="text-sm leading-relaxed">{aiResult.ai_response}</p>
                </div>
                {aiResult.products_count > 0 && (
                  <p className="text-xs text-muted-foreground mt-2">
                    Found {aiResult.products_count} product{aiResult.products_count !== 1 ? 's' : ''}
                  </p>
                )}
              </div>
            )}

            {/* Search Form */}
            <form onSubmit={handleAISearch} className="space-y-3">
              <div className="space-y-2">
                <label className="text-sm font-medium">Ask the AI Assistant</label>
                <Input
                  value={aiQuery}
                  onChange={(e) => setAiQuery(e.target.value)}
                  placeholder='e.g., "I need running shoes under $100"'
                  disabled={aiLoading}
                  className="text-sm"
                />
              </div>
              <Button 
                type="submit" 
                className="w-full gap-2"
                disabled={aiLoading || !aiQuery.trim()}
                size="sm"
              >
                {aiLoading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Searching...
                  </>
                ) : (
                  <>
                    <Sparkles className="h-4 w-4" />
                    Search with AI
                  </>
                )}
              </Button>
            </form>

            {/* Quick Examples */}
            <div className="space-y-2">
              <p className="text-xs text-muted-foreground">Quick examples:</p>
              <div className="flex flex-wrap gap-2">
                {[
                  "running shoes",
                  "organic products",
                  "wireless headphones",
                ].map((example) => (
                  <Button
                    key={example}
                    variant="outline"
                    size="sm"
                    className="text-xs"
                    onClick={() => {
                      setAiQuery(example);
                      handleAISearch({ preventDefault: () => {} } as any);
                    }}
                    disabled={aiLoading}
                  >
                    {example}
                  </Button>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
