"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { 
  ArrowLeft, 
  ShoppingBag, 
  Store as StoreIcon, 
  Package,
  Loader2,
  Star,
  Truck,
  Shield,
  RefreshCw,
  Plus,
  Minus,
  ShoppingCart
} from "lucide-react";
import Link from "next/link";
import { formatPrice } from "@/lib/utils";
import { useCartStore } from "@/store/useCartStore";
import { useToast } from "@/hooks/use-toast";

export default function ProductDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { toast } = useToast();
  const { addItem } = useCartStore();
  const [product, setProduct] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState(0);
  const [quantity, setQuantity] = useState(1);

  useEffect(() => {
    fetchProduct();
  }, [params.slug]);

  const fetchProduct = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/products/${params.slug}/`);
      if (!response.ok) {
        throw new Error('Product not found');
      }
      const data = await response.json();
      setProduct(data);
    } catch (error) {
      console.error('Failed to fetch product:', error);
      router.push('/shop');
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = () => {
    if (!product) return;

    // Check if product is in stock
    if (product.stock_quantity <= 0) {
      toast({
        title: "Out of Stock",
        description: "This product is currently out of stock.",
        variant: "destructive",
      });
      return;
    }

    // Check if requested quantity is available
    if (quantity > product.stock_quantity) {
      toast({
        title: "Insufficient Stock",
        description: `Only ${product.stock_quantity} items available.`,
        variant: "destructive",
      });
      return;
    }

    addItem({
      id: product.id,
      slug: product.slug,
      name: product.name,
      price: parseFloat(product.price),
      quantity: quantity,
      stock_quantity: product.stock_quantity,
      image: product.images?.[0]?.image,
      store_name: product.store?.name,
    });

    toast({
      title: "Added to cart!",
      description: `${quantity} x ${product.name} added to your cart.`,
    });

    setQuantity(1);
  };

  const incrementQuantity = () => {
    if (product && quantity < product.stock_quantity) {
      setQuantity(quantity + 1);
    }
  };

  const decrementQuantity = () => {
    if (quantity > 1) {
      setQuantity(quantity - 1);
    }
  };

  if (loading) {
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
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center justify-center min-h-[400px]">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
          </div>
        </div>
      </div>
    );
  }

  if (!product) {
    return null;
  }

  const discount = product.compare_price && parseFloat(product.compare_price) > parseFloat(product.price)
    ? Math.round(((parseFloat(product.compare_price) - parseFloat(product.price)) / parseFloat(product.compare_price)) * 100)
    : 0;

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
            <div className="flex items-center gap-4">
              <Link href="/shop/cart">
                <Button variant="outline" size="icon" className="relative">
                  <ShoppingCart className="h-5 w-5" />
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
        {/* Back Button */}
        <Button
          variant="ghost"
          className="mb-6"
          onClick={() => router.back()}
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Shop
        </Button>

        <div className="grid gap-8 lg:grid-cols-2">
          {/* Product Images */}
          <div className="space-y-4">
            <Card className="overflow-hidden">
              <div className="aspect-square bg-muted flex items-center justify-center">
                {product.images && product.images.length > 0 ? (
                  <img
                    src={product.images[selectedImage]?.image || product.images[0].image}
                    alt={product.name}
                    className="h-full w-full object-cover"
                  />
                ) : (
                  <Package className="h-24 w-24 text-muted-foreground" />
                )}
              </div>
            </Card>

            {/* Image Thumbnails */}
            {product.images && product.images.length > 1 && (
              <div className="grid grid-cols-4 gap-2">
                {product.images.map((image: any, index: number) => (
                  <button
                    key={image.id}
                    onClick={() => setSelectedImage(index)}
                    className={`aspect-square rounded-lg overflow-hidden border-2 transition-colors ${
                      selectedImage === index ? 'border-primary' : 'border-transparent'
                    }`}
                  >
                    <img
                      src={image.image}
                      alt={`${product.name} ${index + 1}`}
                      className="h-full w-full object-cover"
                    />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Product Info */}
          <div className="space-y-6">
            <div>
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <h1 className="text-3xl font-bold mb-2">{product.name}</h1>
                  {product.category && (
                    <Badge variant="secondary">{product.category.name}</Badge>
                  )}
                </div>
                {discount > 0 && (
                  <Badge variant="destructive" className="text-lg">
                    -{discount}%
                  </Badge>
                )}
              </div>

              {/* Price */}
              <div className="flex items-baseline gap-3 mt-4">
                <p className="text-4xl font-bold">{formatPrice(product.price)}</p>
                {product.compare_price && parseFloat(product.compare_price) > parseFloat(product.price) && (
                  <p className="text-xl text-muted-foreground line-through">
                    {formatPrice(product.compare_price)}
                  </p>
                )}
              </div>

              {/* Stock Status */}
              <div className="mt-4 space-y-2">
                {product.stock_quantity > 0 ? (
                  <>
                    {product.stock_quantity <= 5 ? (
                      <Badge variant="outline" className="text-orange-600 border-orange-600">
                        Low Stock
                      </Badge>
                    ) : (
                      <Badge variant="outline" className="text-green-600 border-green-600">
                        In Stock
                      </Badge>
                    )}
                    <p className="text-sm text-muted-foreground">
                      {product.stock_quantity} {product.stock_quantity === 1 ? 'unit' : 'units'} available
                    </p>
                    {product.stock_quantity <= 5 && (
                      <p className="text-sm text-orange-600">
                        Only {product.stock_quantity} left - Order soon!
                      </p>
                    )}
                  </>
                ) : (
                  <>
                    <Badge variant="outline" className="text-red-600 border-red-600">
                      Out of Stock
                    </Badge>
                    <p className="text-sm text-muted-foreground">
                      0 units available
                    </p>
                    <p className="text-sm text-red-600">
                      This product is currently unavailable
                    </p>
                  </>
                )}
              </div>
            </div>

            {/* Store Info */}
            {product.store && (
              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-center gap-3">
                    <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center">
                      <StoreIcon className="h-6 w-6 text-primary" />
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Sold by</p>
                      <p className="font-semibold">{product.store.name}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Quantity Selector */}
            {product.stock_quantity > 0 && (
              <div className="space-y-2">
                <label className="text-sm font-medium">Quantity</label>
                <div className="flex items-center gap-3">
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={decrementQuantity}
                    disabled={quantity <= 1}
                  >
                    <Minus className="h-4 w-4" />
                  </Button>
                  <Input
                    type="number"
                    min="1"
                    max={product.stock_quantity}
                    value={quantity}
                    onChange={(e) => {
                      const val = parseInt(e.target.value);
                      if (val >= 1 && val <= product.stock_quantity) {
                        setQuantity(val);
                      }
                    }}
                    className="w-20 text-center"
                  />
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={incrementQuantity}
                    disabled={quantity >= product.stock_quantity}
                  >
                    <Plus className="h-4 w-4" />
                  </Button>
                  <span className="text-sm text-muted-foreground">
                    Max: {product.stock_quantity}
                  </span>
                </div>
              </div>
            )}

            {/* Action Buttons */}
            <div className="space-y-3">
              <Button 
                size="lg" 
                className="w-full" 
                disabled={product.stock_quantity === 0}
                onClick={handleAddToCart}
              >
                <ShoppingCart className="mr-2 h-5 w-5" />
                Add to Cart
              </Button>
              <Link href="/shop/cart">
                <Button size="lg" variant="outline" className="w-full">
                  View Cart & Checkout
                </Button>
              </Link>
            </div>

            {/* Features */}
            <div className="grid grid-cols-3 gap-4 pt-4 border-t">
              <div className="text-center">
                <Truck className="h-6 w-6 mx-auto mb-2 text-muted-foreground" />
                <p className="text-xs text-muted-foreground">Free Shipping</p>
              </div>
              <div className="text-center">
                <Shield className="h-6 w-6 mx-auto mb-2 text-muted-foreground" />
                <p className="text-xs text-muted-foreground">Secure Payment</p>
              </div>
              <div className="text-center">
                <RefreshCw className="h-6 w-6 mx-auto mb-2 text-muted-foreground" />
                <p className="text-xs text-muted-foreground">Easy Returns</p>
              </div>
            </div>
          </div>
        </div>

        {/* Product Details */}
        <div className="mt-12 grid gap-6 lg:grid-cols-3">
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle>Product Description</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="prose prose-sm max-w-none">
                <p className="text-muted-foreground whitespace-pre-wrap">
                  {product.description || product.short_description || 'No description available.'}
                </p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Product Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {product.sku && (
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">SKU:</span>
                  <span className="font-medium">{product.sku}</span>
                </div>
              )}
              {product.brand && (
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Brand:</span>
                  <span className="font-medium">{product.brand.name}</span>
                </div>
              )}
              {product.category && (
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Category:</span>
                  <span className="font-medium">{product.category.name}</span>
                </div>
              )}
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Status:</span>
                <Badge variant={product.status === 'published' ? 'default' : 'secondary'}>
                  {product.status}
                </Badge>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
