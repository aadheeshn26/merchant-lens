import { redirect } from "@remix-run/node";
     import { Form, useLoaderData, useActionData } from "@remix-run/react";
     import { useState } from "react";

     export const loader = async () => {
       const [totalSales, sentiment, recommendations] = await Promise.all([
         fetch("http://localhost:8000/sales/total").then(res => res.json()),
         fetch("http://localhost:8000/reviews/sentiment").then(res => res.json()),
         fetch("http://localhost:8000/recommendations/pricing").then(res => res.json())
       ]);
             return { totalSales, sentiment, recommendations };
    };

    export const action = async ({ request }: { request: Request }) => {
       const formData = await request.formData();
       const intent = formData.get("intent");
       if (intent === "upload") {
         const salesFile = formData.get("salesFile");
         const reviewsFile = formData.get("reviewsFile");
         if (salesFile) {
           await fetch("http://localhost:8000/upload-sales", {
             method: "POST",
             body: formData
           });
         }
         if (reviewsFile) {
           await fetch("http://localhost:8000/upload-reviews", {
             method: "POST",
             body: formData
           });
         }
         return redirect("/");
       } else if (intent === "query") {
         const query = formData.get("query");
         const response = await fetch("http://localhost:8000/nlp/query", {
           method: "POST",
           headers: { "Content-Type": "application/json" },
           body: JSON.stringify({ query })
         });
         return await response.json();
       }
       return null;
     };

     export default function Index() {
       const { totalSales, sentiment, recommendations } = useLoaderData<typeof loader>();
       const actionData = useActionData<typeof action>();
       const [query, setQuery] = useState("");

       return (
         <div className="container mx-auto p-6 bg-gray-50 min-h-screen">
           <h1 className="text-4xl font-bold text-gray-800 mb-6">MerchantLens Dashboard</h1>

           {/* File Upload Form */}
           <div className="mb-8 bg-white p-6 rounded-lg shadow-md">
             <h2 className="text-2xl font-semibold text-gray-700 mb-4">Upload Data</h2>
             <Form method="post" encType="multipart/form-data" className="space-y-4">
               <div>
                 <label className="block text-sm font-medium text-gray-600">Sales CSV</label>
                 <input
                   type="file"
                   name="salesFile"
                   accept=".csv"
                   className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-gray-600"
                 />
               </div>
               <div>
                 <label className="block text-sm font-medium text-gray-600">Reviews CSV</label>
                 <input
                   type="file"
                   name="reviewsFile"
                   accept=".csv"
                   className="mt-1 block w-full border border-gray-300 rounded-md p-2 text-gray-600"
                 />
               </div>
               <input type="hidden" name="intent" value="upload" />
               <button
                 type="submit"
                 className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-md transition duration-200"
               >
                 Upload Files
               </button>
             </Form>
           </div>

           {/* NLP Query Form */}
           <div className="mb-8 bg-white p-6 rounded-lg shadow-md">
             <h2 className="text-2xl font-semibold text-gray-700 mb-4">Ask a Question</h2>
             <Form method="post" className="space-y-4">
               <div>
                 <label className="block text-sm font-medium text-gray-600">Query</label>
                 <input
                   type="text"
                   name="query"
                   value={query}
                   onChange={(e) => setQuery(e.target.value)}
                   className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                   placeholder="e.g., Compare sales last week vs. previous"
                 />
               </div>
               <input type="hidden" name="intent" value="query" />
               <button
                 type="submit"
                 className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-md transition duration-200"
               >
                 Submit Query
               </button>
             </Form>
             {actionData?.answer && (
               <div className="mt-6 p-4 bg-blue-50 rounded-md">
                 <p className="text-sm font-medium text-gray-700">
                   <strong>Query:</strong> {actionData.query}
                 </p>
                 <p className="text-sm text-gray-600">
                   <strong>Answer:</strong> {actionData.answer}
                 </p>
               </div>
             )}
           </div>

           {/* Dashboard Sections */}
           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
             <div className="bg-white p-6 rounded-lg shadow-md">
               <h2 className="text-xl font-semibold text-gray-700 mb-2">Total Sales</h2>
               <p className="text-2xl text-blue-600">${totalSales.total_sales.toFixed(2)}</p>
             </div>
             <div className="bg-white p-6 rounded-lg shadow-md">
               <h2 className="text-xl font-semibold text-gray-700 mb-2">Review Sentiment</h2>
               <ul className="list-disc pl-5 text-gray-600">
                 {Object.entries(sentiment).map(([text, info]: any) => (
                   <li key={text} className="mb-1">
                     {text.slice(0, 50)}...: {info.sentiment} (Polarity: {info.polarity.toFixed(2)})
                   </li>
                 ))}
               </ul>
             </div>
             <div className="bg-white p-6 rounded-lg shadow-md">
               <h2 className="text-xl font-semibold text-gray-700 mb-2">Pricing Recommendations</h2>
               <ul className="list-disc pl-5 text-gray-600">
                 {Object.entries(recommendations.pricing_suggestions).map(([product, suggestion]: any) => (
                   <li key={product} className="mb-1">
                     {product}: {suggestion}
                   </li>
                 ))}
               </ul>
             </div>
           </div>
         </div>
       );
     }