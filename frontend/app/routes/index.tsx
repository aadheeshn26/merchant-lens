import { json } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";

export const loader = async () => {
  const [totalSales, sentiment, recommendations] = await Promise.all([
    fetch("http://localhost:8000/sales/total").then(res => res.json()),
    fetch("http://localhost:8000/reviews/sentiment").then(res => res.json()),
    fetch("http://localhost:8000/recommendations/pricing").then(res => res.json())
  ]);
  return json({ totalSales, sentiment, recommendations });
};

export default function Index() {
  const { totalSales, sentiment, recommendations } = useLoaderData<typeof loader>();
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">MerchantLens Dashboard</h1>
      <div className="mb-4">
        <h2 className="text-xl font-semibold">Total Sales</h2>
        <p>${totalSales.total_sales}</p>
      </div>
      <div className="mb-4">
        <h2 className="text-xl font-semibold">Review Sentiment</h2>
        <ul className="list-disc pl-5">
          {Object.entries(sentiment).map(([text, info]: any) => (
            <li key={text}>
              {text}: {info.sentiment} (Polarity: {info.polarity})
            </li>
          ))}
        </ul>
      </div>
      <div>
        <h2 className="text-xl font-semibold">Pricing Recommendations</h2>
        <ul className="list-disc pl-5">
          {Object.entries(recommendations.pricing_suggestions).map(([product, suggestion]: any) => (
            <li key={product}>{product}: {suggestion}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}