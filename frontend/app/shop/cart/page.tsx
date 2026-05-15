"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { 
  ShoppingBag, 
  ShoppingCart, 
  Trash2, 
  Plus, 
  Minus,
  ArrowLeft,
  Loader2
} from "lucide-react";
import Link from "next/link";
import { formatPrice } from "@/lib/utils";
import { useCartStore } from "@/store/useCartStore";
import { useAuthStore } from "@/store/useAuthStore";
import { useToast } from "@/hooks/use-toast";

export default function CartPage() {
  const router = useRouter();
  const { toast } = useToast();
  const { user } = useAuthStore();
  const { items, updateQuantity, removeItem, clearCart, getTotalPrice } = useCartStore();
  const [loading, setLoading] = useState(false);
  const [showCheckout, setShowCheckout] = useState(false);
  
  // Calculate total safely
  const totalPrice = getTotalPrice();
  const isValidTotal = !isNaN(totalPrice) && isFinite(totalPrice) && totalPrice > 0;
  
  // Check for stock issues
  const hasOutOfStockItems = items.some(item => item.stock_quantity <= 0);
  const hasInsufficientStock = items.some(item => item.quantity > item.stock_quantity);
  const canCheckout = isValidTotal && !hasOutOfStockItems && !hasInsufficientStock;
  
  // Debug: Log cart items to console
  useEffect(() => {
    console.log('Cart items:', items);
    console.log('Total price:', totalPrice);
    console.log('Is valid total:', isValidTotal);
    console.log('Has out of stock:', hasOutOfStockItems);
    console.log('Has insufficient stock:', hasInsufficientStock);
    console.log('Can checkout:', canCheckout);
  }, [items, totalPrice, isValidTotal, hasOutOfStockItems, hasInsufficientStock, canCheckout]);
  
  const [checkoutData, setCheckoutData] = useState({
    shipping_address: "",
    billing_address: "",
    phone: "",
    email: user?.email || "",
    notes: "",
  });

  const handleCheckout = async (e: React.FormEvent) => {
    e.preventDefault();

    // Check if cart is empty
    if (items.length === 0) {
      toast({
        title: "Cart is empty",
        description: "Add some products to your cart first",
        variant: "destructive",
      });
      return;
    }

    // Check if any items are out of stock
    const outOfStockItems = items.filter(item => item.stock_quantity <= 0);
    if (outOfStockItems.length > 0) {
      toast({
        title: "Items Out of Stock",
        description: `Some items in your cart are out of stock. Please remove them.`,
        variant: "destructive",
      });
      return;
    }

    // Check if quantities exceed stock
    const insufficientStockItems = items.filter(item => item.quantity > item.stock_quantity);
    if (insufficientStockItems.length > 0) {
      toast({
        title: "Insufficient Stock",
        description: `Some items exceed available stock. Please adjust quantities.`,
        variant: "destructive",
      });
      return;
    }

    setLoading(true);

    try {
      const orderItems = items.map(item => ({
        product: item.id,
        quantity: item.quantity,
      }));

      // Prepare headers - include auth token if user is logged in
      const headers: any = {
        "Content-Type": "application/json",
      };
      
      if (user) {
        headers["Authorization"] = `Bearer ${localStorage.getItem("access_token")}`;
      }

      const response = await fetch("http://localhost:8000/api/orders/create/", {
        method: "POST",
        headers: headers,
        body: JSON.stringify({
          ...checkoutData,
          items: orderItems,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || error.message || "Failed to create order");
      }

      const order = await response.json();
      
      console.log('Order response:', order);

      toast({
        title: "Order placed successfully!",
        description: `Order #${order.order_number} has been created.`,
      });

      clearCart();
      
      // Redirect based on login status
      if (user) {
        router.push("/orders");
      } else {
        // Guest checkout - redirect to order confirmation page
        const confirmUrl = `/order-confirmation?order=${order.order_number}&email=${encodeURIComponent(checkoutData.email)}&total=${order.total_amount}`;
        console.log('Redirecting to:', confirmUrl);
        router.push(confirmUrl);
      }
    } catch (error: any) {
      toast({
        title: "Order failed",
        description: error.message || "Failed to place order",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  if (items.length === 0) {
    return (
      <div className="min-h-screen bg-background">
        <header className="border-b">
          <div className="container mx-auto px-4 py-4">
            <Link href="/shop" className="flex items-center gap-2">
              <ShoppingBag className="h-6 w-6" />
              <span className="text-xl font-bold">AI Shop</span>
            </Link>
          </div>
        </header>
        <div className="container mx-auto px-4 py-16">
          <Card>
            <CardContent className="py-16 text-center">
              <ShoppingCart className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
              <h2 className="text-2xl font-bold mb-2">Your cart is empty</h2>
              <p className="text-muted-foreground mb-6">
                Add some products to get started
              </p>
              <Link href="/shop">
                <Button>Continue Shopping</Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b sticky top-0 bg-background z-40">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link href="/shop" className="flex items-center gap-2">
              <ShoppingBag className="h-6 w-6" />
              <span className="text-xl font-bold">AI Shop</span>
            </Link>
            <Link href="/login">
              <Button variant="outline">Seller Login</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <Button
          variant="ghost"
          className="mb-6"
          onClick={() => router.back()}
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Continue Shopping
        </Button>

        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold">Shopping Cart</h1>
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              if (confirm("Are you sure you want to clear your cart?")) {
                clearCart();
                toast({
                  title: "Cart cleared",
                  description: "All items have been removed from your cart",
                });
              }
            }}
          >
            <Trash2 className="mr-2 h-4 w-4" />
            Clear Cart
          </Button>
        </div>

        <div className="grid gap-8 lg:grid-cols-3">
          {/* Cart Items */}
          <div className="lg:col-span-2 space-y-4">
            {items.map((item) => {
              const isOutOfStock = item.stock_quantity <= 0;
              const exceedsStock = item.quantity > item.stock_quantity;
              
              return (
              <Card key={item.id} className={isOutOfStock ? "border-destructive" : ""}>
                <CardContent className="p-4">
                  {isOutOfStock && (
                    <div className="mb-3 bg-destructive/10 text-destructive text-sm p-2 rounded">
                      ⚠️ This item is out of stock
                    </div>
                  )}
                  {exceedsStock && !isOutOfStock && (
                    <div className="mb-3 bg-yellow-50 dark:bg-yellow-950 text-yellow-700 dark:text-yellow-300 text-sm p-2 rounded">
                      ⚠️ Only {item.stock_quantity} available
                    </div>
                  )}
                  <div className="flex gap-4">
                    {/* Product Image */}
                    <div className="w-24 h-24 bg-muted rounded-lg flex items-center justify-center flex-shrink-0">
                      {item.image ? (
                        <img
                          src={item.image}
                          alt={item.name}
                          className="w-full h-full object-cover rounded-lg"
                        />
                      ) : (
                        <ShoppingBag className="h-8 w-8 text-muted-foreground" />
                      )}
                    </div>

                    {/* Product Info */}
                    <div className="flex-1 min-w-0">
                      <Link href={`/shop/${item.slug}`}>
                        <h3 className="font-semibold hover:text-primary truncate">
                          {item.name}
                        </h3>
                      </Link>
                      {item.store_name && (
                        <p className="text-sm text-muted-foreground">
                          by {item.store_name}
                        </p>
                      )}
                      <p className="text-lg font-bold mt-2">
                        {formatPrice(item.price)}
                      </p>
                      {item.stock_quantity > 0 && (
                        <p className="text-xs text-muted-foreground mt-1">
                          {item.stock_quantity} in stock
                        </p>
                      )}

                      {/* Quantity Controls */}
                      <div className="flex items-center gap-2 mt-3">
                        <Button
                          variant="outline"
                          size="icon"
                          className="h-8 w-8"
                          onClick={() => updateQuantity(item.id, item.quantity - 1)}
                          disabled={isOutOfStock}
                        >
                          <Minus className="h-3 w-3" />
                        </Button>
                        <span className="w-12 text-center font-medium">
                          {item.quantity}
                        </span>
                        <Button
                          variant="outline"
                          size="icon"
                          className="h-8 w-8"
                          onClick={() => updateQuantity(item.id, item.quantity + 1)}
                          disabled={item.quantity >= item.stock_quantity || isOutOfStock}
                        >
                          <Plus className="h-3 w-3" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-8 w-8 ml-auto"
                          onClick={() => removeItem(item.id)}
                        >
                          <Trash2 className="h-4 w-4 text-destructive" />
                        </Button>
                      </div>
                    </div>

                    {/* Subtotal */}
                    <div className="text-right">
                      <p className="font-bold text-lg">
                        {formatPrice(item.price * item.quantity)}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
            )}
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <Card className="sticky top-24">
              <CardHeader>
                <CardTitle>Order Summary</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Subtotal</span>
                    <span>{isValidTotal ? formatPrice(totalPrice) : '$0.00'}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Shipping</span>
                    <span className="text-green-600">Free</span>
                  </div>
                  <div className="border-t pt-2 flex justify-between font-bold text-lg">
                    <span>Total</span>
                    <span>{isValidTotal ? formatPrice(totalPrice) : '$0.00'}</span>
                  </div>
                </div>

                {!isValidTotal && (
                  <div className="bg-destructive/10 text-destructive text-sm p-3 rounded-lg">
                    Cart has invalid data. Please clear cart and try again.
                  </div>
                )}
                
                {hasOutOfStockItems && (
                  <div className="bg-destructive/10 text-destructive text-sm p-3 rounded-lg">
                    Some items are out of stock. Please remove them to continue.
                  </div>
                )}
                
                {hasInsufficientStock && !hasOutOfStockItems && (
                  <div className="bg-yellow-50 dark:bg-yellow-950 text-yellow-700 dark:text-yellow-300 text-sm p-3 rounded-lg">
                    Some items exceed available stock. Please adjust quantities.
                  </div>
                )}

                {!showCheckout ? (
                  <div className="space-y-3">
                    {!user && (
                      <div className="bg-blue-50 dark:bg-blue-950 text-blue-700 dark:text-blue-300 text-sm p-3 rounded-lg">
                        💡 You can checkout as a guest or <Link href="/login" className="underline font-semibold">login</Link> to track your order
                      </div>
                    )}
                    <Button 
                      className="w-full" 
                      size="lg"
                      disabled={!canCheckout}
                      onClick={() => setShowCheckout(true)}
                    >
                      Proceed to Checkout
                    </Button>
                  </div>
                ) : (
                  <form onSubmit={handleCheckout} className="space-y-4">
                    {!user && (
                      <div className="bg-green-50 dark:bg-green-950 text-green-700 dark:text-green-300 text-sm p-3 rounded-lg">
                        ✓ Checking out as guest. Order confirmation will be sent to your email.
                      </div>
                    )}
                    
                    <div className="space-y-2">
                      <Label htmlFor="email">Email *</Label>
                      <Input
                        id="email"
                        type="email"
                        value={checkoutData.email}
                        onChange={(e) => setCheckoutData({ ...checkoutData, email: e.target.value })}
                        placeholder="your@email.com"
                        required
                      />
                      <p className="text-xs text-muted-foreground">
                        Order confirmation will be sent here
                      </p>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="phone">Phone *</Label>
                      <Input
                        id="phone"
                        type="tel"
                        value={checkoutData.phone}
                        onChange={(e) => setCheckoutData({ ...checkoutData, phone: e.target.value })}
                        required
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="shipping">Shipping Address *</Label>
                      <Textarea
                        id="shipping"
                        value={checkoutData.shipping_address}
                        onChange={(e) => setCheckoutData({ ...checkoutData, shipping_address: e.target.value })}
                        rows={3}
                        required
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="billing">Billing Address *</Label>
                      <Textarea
                        id="billing"
                        value={checkoutData.billing_address}
                        onChange={(e) => setCheckoutData({ ...checkoutData, billing_address: e.target.value })}
                        rows={3}
                        required
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="notes">Order Notes (Optional)</Label>
                      <Textarea
                        id="notes"
                        value={checkoutData.notes}
                        onChange={(e) => setCheckoutData({ ...checkoutData, notes: e.target.value })}
                        rows={2}
                        placeholder="Any special instructions..."
                      />
                    </div>

                    <div className="space-y-2">
                      <Button type="submit" className="w-full" size="lg" disabled={loading}>
                        {loading ? (
                          <>
                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            Placing Order...
                          </>
                        ) : (
                          "Place Order"
                        )}
                      </Button>
                      <Button
                        type="button"
                        variant="outline"
                        className="w-full"
                        onClick={() => setShowCheckout(false)}
                        disabled={loading}
                      >
                        Cancel
                      </Button>
                    </div>
                  </form>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
