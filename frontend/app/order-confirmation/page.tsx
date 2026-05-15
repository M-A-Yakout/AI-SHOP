"use client";

import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  CheckCircle, 
  Package, 
  Mail, 
  Phone, 
  MapPin,
  ShoppingBag,
  ArrowRight
} from "lucide-react";
import Link from "next/link";
import { formatPrice } from "@/lib/utils";

export default function OrderConfirmationPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const orderNumber = searchParams.get("order");
  const email = searchParams.get("email");
  const total = searchParams.get("total");

  console.log('Order confirmation params:', { orderNumber, email, total });

  useEffect(() => {
    // If no order number, redirect to shop
    if (!orderNumber) {
      console.log('No order number, redirecting to shop');
      router.push("/shop");
    }
  }, [orderNumber, router]);

  if (!orderNumber) {
    return null;
  }

  const totalAmount = total ? parseFloat(total) : 0;
  const isValidTotal = !isNaN(totalAmount) && isFinite(totalAmount);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b">
        <div className="container mx-auto px-4 py-4">
          <Link href="/shop" className="flex items-center gap-2">
            <ShoppingBag className="h-6 w-6" />
            <span className="text-xl font-bold">AI Shop</span>
          </Link>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-16">
        <div className="max-w-2xl mx-auto">
          {/* Success Message */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-100 dark:bg-green-900 mb-4">
              <CheckCircle className="h-8 w-8 text-green-600 dark:text-green-400" />
            </div>
            <h1 className="text-3xl font-bold mb-2">Order Placed Successfully!</h1>
            <p className="text-muted-foreground">
              Thank you for your purchase. Your order has been received and is being processed.
            </p>
          </div>

          {/* Order Details Card */}
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Package className="h-5 w-5" />
                Order Details
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <p className="text-sm text-muted-foreground">Order Number</p>
                  <p className="font-mono font-bold text-lg">{orderNumber}</p>
                </div>
                {isValidTotal && (
                  <div>
                    <p className="text-sm text-muted-foreground">Total Amount</p>
                    <p className="font-bold text-lg">{formatPrice(totalAmount)}</p>
                  </div>
                )}
              </div>

              <div className="border-t pt-4">
                <Badge variant="outline" className="text-yellow-600 border-yellow-600">
                  Processing
                </Badge>
              </div>
            </CardContent>
          </Card>

          {/* Contact Information */}
          {email && (
            <Card className="mb-6">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Mail className="h-5 w-5" />
                  Order Confirmation
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-2">
                  A confirmation email has been sent to:
                </p>
                <p className="font-semibold">{email}</p>
                <p className="text-sm text-muted-foreground mt-4">
                  Please check your email for order details and tracking information.
                </p>
              </CardContent>
            </Card>
          )}

          {/* What's Next */}
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>What Happens Next?</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex gap-3">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold">
                    1
                  </div>
                  <div>
                    <p className="font-semibold">Order Confirmation</p>
                    <p className="text-sm text-muted-foreground">
                      You'll receive an email confirmation with your order details
                    </p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold">
                    2
                  </div>
                  <div>
                    <p className="font-semibold">Processing</p>
                    <p className="text-sm text-muted-foreground">
                      We'll prepare your order for shipment
                    </p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold">
                    3
                  </div>
                  <div>
                    <p className="font-semibold">Shipping</p>
                    <p className="text-sm text-muted-foreground">
                      Your order will be shipped and you'll receive tracking information
                    </p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold">
                    4
                  </div>
                  <div>
                    <p className="font-semibold">Delivery</p>
                    <p className="text-sm text-muted-foreground">
                      Your order will be delivered to your address
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Actions */}
          <div className="flex flex-col sm:flex-row gap-4">
            <Link href="/shop" className="flex-1">
              <Button className="w-full" size="lg">
                Continue Shopping
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
            <Link href="/login" className="flex-1">
              <Button variant="outline" className="w-full" size="lg">
                Create Account to Track Orders
              </Button>
            </Link>
          </div>

          {/* Help Section */}
          <Card className="mt-6 bg-muted/50">
            <CardContent className="pt-6">
              <p className="text-sm text-center text-muted-foreground">
                Need help with your order? Contact us at{" "}
                <a href="mailto:support@example.com" className="text-primary hover:underline">
                  support@example.com
                </a>
              </p>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
