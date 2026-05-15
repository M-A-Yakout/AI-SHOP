"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { orderService } from "@/services/order.service";
import { ShoppingCart, Package, DollarSign, Edit } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/hooks/use-toast";
import { formatPrice, formatDate } from "@/lib/utils";

export default function OrdersPage() {
  const [orders, setOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [updatingOrderId, setUpdatingOrderId] = useState<number | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const data = await orderService.getOrders();
      const ordersArray = Array.isArray(data) ? data : [];
      setOrders(ordersArray);
    } catch (error) {
      console.error('Failed to fetch orders:', error);
      setOrders([]);
      toast({
        title: "Error",
        description: "Failed to fetch orders",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (orderId: number, newStatus: string) => {
    setUpdatingOrderId(orderId);
    try {
      await orderService.updateOrder(orderId, { status: newStatus });
      
      // Update local state
      setOrders(orders.map(order => 
        order.id === orderId ? { ...order, status: newStatus } : order
      ));
      
      toast({
        title: "Success",
        description: "Order status updated successfully",
      });
    } catch (error: any) {
      toast({
        title: "Error",
        description: error.message || "Failed to update order status",
        variant: "destructive",
      });
    } finally {
      setUpdatingOrderId(null);
    }
  };

  const handlePaymentStatusChange = async (orderId: number, newStatus: string) => {
    setUpdatingOrderId(orderId);
    try {
      await orderService.updateOrder(orderId, { payment_status: newStatus });
      
      // Update local state
      setOrders(orders.map(order => 
        order.id === orderId ? { ...order, payment_status: newStatus } : order
      ));
      
      toast({
        title: "Success",
        description: "Payment status updated successfully",
      });
    } catch (error: any) {
      toast({
        title: "Error",
        description: error.message || "Failed to update payment status",
        variant: "destructive",
      });
    } finally {
      setUpdatingOrderId(null);
    }
  };

  const getStatusVariant = (status: string) => {
    switch (status) {
      case 'delivered':
        return 'success';
      case 'cancelled':
        return 'destructive';
      case 'processing':
      case 'shipped':
        return 'default';
      default:
        return 'secondary';
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-64" />
        <div className="space-y-4">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-32" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Orders</h1>
        <p className="text-muted-foreground">
          View orders you've placed and orders for your products
        </p>
      </div>

      {orders.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-16">
            <div className="text-center">
              <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-muted">
                <ShoppingCart className="h-8 w-8 text-muted-foreground" />
              </div>
              <h3 className="mb-2 text-lg font-semibold">No orders yet</h3>
              <p className="mb-4 text-sm text-muted-foreground">
                Orders will appear here when you make purchases or customers buy your products
              </p>
            </div>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => (
            <Card key={order.id}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="flex items-center gap-2">
                      <ShoppingCart className="h-5 w-5" />
                      Order #{order.order_number}
                    </CardTitle>
                    <p className="text-sm text-muted-foreground mt-1">
                      {formatDate(order.created_at)}
                    </p>
                    {order.customer_name && (
                      <p className="text-sm text-muted-foreground mt-1">
                        Customer: {order.customer_name || order.email}
                      </p>
                    )}
                    {!order.customer && order.email && (
                      <p className="text-sm text-muted-foreground mt-1">
                        Guest Order: {order.email}
                      </p>
                    )}
                  </div>
                  <div className="flex gap-2 flex-wrap justify-end">
                    {/* Order Status Dropdown */}
                    <div className="flex flex-col gap-1">
                      <select
                        value={order.status}
                        onChange={(e) => handleStatusChange(order.id, e.target.value)}
                        disabled={updatingOrderId === order.id}
                        className="text-xs px-2 py-1 rounded-md border border-input bg-background"
                      >
                        <option value="pending">Pending</option>
                        <option value="processing">Processing</option>
                        <option value="shipped">Shipped</option>
                        <option value="delivered">Delivered</option>
                        <option value="cancelled">Cancelled</option>
                      </select>
                      <select
                        value={order.payment_status}
                        onChange={(e) => handlePaymentStatusChange(order.id, e.target.value)}
                        disabled={updatingOrderId === order.id}
                        className="text-xs px-2 py-1 rounded-md border border-input bg-background"
                      >
                        <option value="pending">Payment Pending</option>
                        <option value="paid">Paid</option>
                        <option value="failed">Failed</option>
                        <option value="refunded">Refunded</option>
                      </select>
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid gap-4 md:grid-cols-3">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-muted">
                      <Package className="h-5 w-5 text-muted-foreground" />
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Items</p>
                      <p className="font-semibold">{order.items?.length || 0}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-muted">
                      <DollarSign className="h-5 w-5 text-muted-foreground" />
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Total</p>
                      <p className="font-semibold">{formatPrice(order.total_amount)}</p>
                    </div>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Contact</p>
                    <p className="text-sm font-medium">
                      {order.phone || "N/A"}
                    </p>
                    <p className="text-sm text-muted-foreground truncate">
                      {order.email || "N/A"}
                    </p>
                  </div>
                </div>
                
                {/* Order Items */}
                {order.items && order.items.length > 0 && (
                  <div className="mt-4 pt-4 border-t">
                    <p className="text-sm font-semibold mb-2">Order Items:</p>
                    <div className="space-y-2">
                      {order.items.map((item: any, index: number) => (
                        <div key={index} className="flex justify-between text-sm">
                          <span className="text-muted-foreground">
                            {item.product_name} x {item.quantity}
                          </span>
                          <span className="font-medium">
                            {formatPrice(item.subtotal)}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
                {/* Shipping Address */}
                <div className="mt-4 pt-4 border-t">
                  <p className="text-sm font-semibold mb-1">Shipping Address:</p>
                  <p className="text-sm text-muted-foreground whitespace-pre-wrap">
                    {order.shipping_address || "N/A"}
                  </p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
