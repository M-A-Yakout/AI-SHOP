"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { storeService } from "@/services/store.service";
import { Plus, Store as StoreIcon, Edit, Trash2 } from "lucide-react";
import Link from "next/link";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/hooks/use-toast";

export default function StoresPage() {
  const [stores, setStores] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();

  useEffect(() => {
    fetchStores();
  }, []);

  const fetchStores = async () => {
    try {
      const data = await storeService.getMyStores();
      const storesArray = Array.isArray(data) ? data : [];
      setStores(storesArray);
    } catch (error) {
      console.error('Failed to fetch stores:', error);
      setStores([]);
      toast({
        title: "Error",
        description: "Failed to fetch stores",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (slug: string) => {
    if (!confirm("Are you sure you want to delete this store?")) return;

    try {
      await storeService.deleteStore(slug);
      toast({
        title: "Success",
        description: "Store deleted successfully",
      });
      fetchStores();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete store",
        variant: "destructive",
      });
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-64" />
        <div className="grid gap-4 md:grid-cols-2">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-48" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Stores</h1>
          <p className="text-muted-foreground">Manage your online stores</p>
        </div>
        <Link href="/ai">
          <Button className="gap-2">
            <Plus className="h-4 w-4" />
            Create Store with AI
          </Button>
        </Link>
      </div>

      {stores.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-16">
            <div className="text-center">
              <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-muted">
                <StoreIcon className="h-8 w-8 text-muted-foreground" />
              </div>
              <h3 className="mb-2 text-lg font-semibold">No stores yet</h3>
              <p className="mb-4 text-sm text-muted-foreground">
                Get started by creating your first store with AI
              </p>
              <Link href="/ai">
                <Button>Create Store</Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-6 md:grid-cols-2">
          {stores.map((store) => (
            <Card key={store.id}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="flex items-center gap-2">
                      <StoreIcon className="h-5 w-5" />
                      {store.name}
                    </CardTitle>
                    <p className="text-sm text-muted-foreground mt-1">
                      {store.description || "No description"}
                    </p>
                  </div>
                  <Badge variant={store.status === 'active' ? 'success' : 'secondary'}>
                    {store.status}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-muted-foreground">Products</p>
                      <p className="font-semibold">{store.products_count || 0}</p>
                    </div>
                    <div>
                      <p className="text-muted-foreground">Created</p>
                      <p className="font-semibold">
                        {new Date(store.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Link href={`/stores/${store.slug}`} className="flex-1">
                      <Button variant="outline" size="sm" className="w-full gap-2">
                        <Edit className="h-4 w-4" />
                        Manage
                      </Button>
                    </Link>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDelete(store.slug)}
                      className="gap-2"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
