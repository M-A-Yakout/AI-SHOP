"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { storeService } from "@/services/store.service";
import { productService } from "@/services/product.service";
import { Store, Package, TrendingUp, Plus, ArrowRight } from "lucide-react";
import Link from "next/link";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";

export default function DashboardPage() {
  const [stats, setStats] = useState({
    stores: 0,
    products: 0,
    revenue: 0,
  });
  const [stores, setStores] = useState<any[]>([]);
  const [recentProducts, setRecentProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [storesData, productsData] = await Promise.all([
          storeService.getMyStores(),
          productService.getProducts(),
        ]);
        
        setStores(storesData);
        setRecentProducts(productsData.slice(0, 5));
        setStats({
          stores: storesData.length,
          products: productsData.length,
          revenue: 0,
        });
      } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-64" />
        <div className="grid gap-4 md:grid-cols-3">
          <Skeleton className="h-32" />
          <Skeleton className="h-32" />
          <Skeleton className="h-32" />
        </div>
        <Skeleton className="h-64" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">Overview of your ecommerce platform</p>
        </div>
        <Link href="/ai">
          <Button className="gap-2">
            <Plus className="h-4 w-4" />
            Create Store with AI
          </Button>
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Stores</CardTitle>
            <Store className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.stores}</div>
            <p className="text-xs text-muted-foreground">Active stores</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Products</CardTitle>
            <Package className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.products}</div>
            <p className="text-xs text-muted-foreground">Published products</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Revenue</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${stats.revenue}</div>
            <p className="text-xs text-muted-foreground">Total earnings</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Stores List */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Your Stores</CardTitle>
            <Link href="/stores">
              <Button variant="ghost" size="sm" className="gap-2">
                View All
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
          </CardHeader>
          <CardContent>
            {stores.length === 0 ? (
              <div className="text-center py-8">
                <Store className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground mb-4">No stores yet</p>
                <Link href="/ai">
                  <Button>Create Your First Store</Button>
                </Link>
              </div>
            ) : (
              <div className="space-y-4">
                {stores.slice(0, 3).map((store: any) => (
                  <div key={store.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors">
                    <div>
                      <h3 className="font-semibold">{store.name}</h3>
                      <p className="text-sm text-muted-foreground">
                        {store.products_count || 0} products
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant={store.status === 'active' ? 'success' : 'secondary'}>
                        {store.status}
                      </Badge>
                      <Link href={`/stores/${store.slug}`}>
                        <Button variant="outline" size="sm">Manage</Button>
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Recent Products */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Recent Products</CardTitle>
            <Link href="/products">
              <Button variant="ghost" size="sm" className="gap-2">
                View All
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
          </CardHeader>
          <CardContent>
            {recentProducts.length === 0 ? (
              <div className="text-center py-8">
                <Package className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground mb-4">No products yet</p>
                <Link href="/products/new">
                  <Button>Add Your First Product</Button>
                </Link>
              </div>
            ) : (
              <div className="space-y-4">
                {recentProducts.map((product: any) => (
                  <div key={product.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors">
                    <div>
                      <h3 className="font-semibold">{product.name}</h3>
                      <p className="text-sm text-muted-foreground">
                        ${product.price}
                      </p>
                    </div>
                    <Badge variant={product.status === 'published' ? 'success' : 'secondary'}>
                      {product.status}
                    </Badge>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
