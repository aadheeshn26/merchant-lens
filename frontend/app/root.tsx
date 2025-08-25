import type { MetaFunction, LinksFunction } from "@remix-run/node";
import { Links, LiveReload, Meta, Outlet, Scripts } from "@remix-run/react";
import stylesheet from "./tailwind.css";

export const meta: MetaFunction = () => [{ title: "MerchantLens" }];

export const links: LinksFunction = () => [
  { rel: "stylesheet", href: stylesheet },
];

     export default function App() {
       return (
         <html lang="en">
           <head>
             <meta charSet="utf-8" />
             <meta name="viewport" content="width=device-width, initial-scale=1" />
             <Meta />
             <Links />
           </head>
           <body className="bg-gray-50">
             <Outlet />
             <Scripts />
             <LiveReload />
           </body>
         </html>
       );
     }