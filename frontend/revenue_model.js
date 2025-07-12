import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Check } from 'lucide-react';

const RevenueModelSlide = () => {
  return (
    <div className="bg-gradient-to-br from-blue-100 to-green-100 p-6 rounded-lg shadow-lg">
      <h1 className="text-3xl font-bold text-center mb-6 text-blue-800">Revenue Model: EcoTribe</h1>
      
      <div className="grid grid-cols-2 gap-6">
        <Card className="bg-white">
          <CardHeader>
            <CardTitle className="text-xl font-semibold text-blue-700">Subscription Tiers</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              <li className="flex items-center"><Check className="text-green-500 mr-2" /> Basic: Essential fruit analysis tools</li>
              <li className="flex items-center"><Check className="text-green-500 mr-2" /> Pro: Advanced features + priority support</li>
              <li className="flex items-center"><Check className="text-green-500 mr-2" /> Enterprise: Full suite + customization</li>
            </ul>
          </CardContent>
        </Card>
        
        <Card className="bg-white">
          <CardHeader>
            <CardTitle className="text-xl font-semibold text-blue-700">Premium Features</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              <li className="flex items-center"><Check className="text-green-500 mr-2" /> Federated Training</li>
              <li className="flex items-center"><Check className="text-green-500 mr-2" /> Advanced Data Insights</li>
              <li className="flex items-center"><Check className="text-green-500 mr-2" /> Predictive Analysis</li>
              <li className="flex items-center"><Check className="text-green-500 mr-2" /> Auto-retraining of Vision Models</li>
            </ul>
          </CardContent>
        </Card>
        
        <Card className="bg-white col-span-2">
          <CardHeader>
            <CardTitle className="text-xl font-semibold text-blue-700">Value-Added Services</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 grid grid-cols-2">
              <li className="flex items-center"><Check className="text-green-500 mr-2" /> YOLO Model Integration</li>
              <li className="flex items-center"><Check className="text-green-500 mr-2" /> Custom API Development</li>
              <li className="flex items-center"><Check className="text-green-500 mr-2" /> On-site Installation & Training</li>
              <li className="flex items-center"><Check className="text-green-500 mr-2" /> 24/7 Expert Support</li>
            </ul>
          </CardContent>
        </Card>
      </div>
      
      <div className="mt-6 text-center text-lg font-semibold text-blue-800">
        Projected Annual Recurring Revenue: $10M+ by Year 3
      </div>
    </div>
  );
};

export default RevenueModelSlide;