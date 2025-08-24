import type { MetaFunction } from "@remix-run/node";
import { Links, LiveReload, Meta, Outlet, Scripts } from "@remix-run/react";

// Import Tailwind CSS using relative path
import "./tailwind.css";

export const meta: MetaFunction = () => [{ title: "MerchantLens" }];

export default function App() {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body>
        <h1 className="text-3xl font-bold text-center py-8">MerchantLens FrontEnd! 🚀</h1>
        <Outlet />
        <Scripts />
        <LiveReload />
      </body>
    </html>
  );
}