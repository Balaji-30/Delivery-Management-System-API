import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";
import { Button } from "~/components/ui/button";
import { Link } from "react-router";

// export function meta({}: Route.MetaArgs) {
//   return [
//     { title: "New React Router App" },
//     { name: "description", content: "Welcome to React Router!" },
//   ];
// }

export default function Home() {
  return (
    <div className="min-h-screen bg-linear-to-b from-white via-slate-50 to-slate-100 dark:from-slate-900 dark:via-slate-800 flex items-center justify-center">
      <div className="container mx-auto px-6 py-20">
      <div className="grid grid-cols-1 gap-12 items-center justify-center">
        <div className="mx-auto max-w-3xl text-center">
        <h1 className="text-4xl sm:text-5xl font-extrabold leading-tight text-slate-900 dark:text-white">
          Welcome to <span className="bg-clip-text text-transparent bg-linear-to-r from-indigo-600 to-teal-400">Shippin</span>
        </h1>
        <p className="mt-4 text-lg text-slate-600 dark:text-slate-300 mx-auto max-w-xl">
          A modern delivery management system built for sellers and delivery partners — fast onboarding, real-time tracking, and intuitive workflows.
        </p>

        <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-md mx-auto">
          <Button className="w-full px-5 py-3" asChild>
          <Link to="/seller/login">Seller Login</Link>
          </Button>
          <Button className="w-full px-5 py-3" asChild>
          <Link to="/partner/login">Delivery Partner Login</Link>
          </Button>
          <Button className="w-full px-5 py-3 border border-slate-200 bg-transparent text-slate-700 dark:text-slate-200" asChild>
          <Link to="/seller/register">Seller Signup</Link>
          </Button>
          <Button className="w-full px-5 py-3 border border-slate-200 bg-transparent text-slate-700 dark:text-slate-200" asChild>
          <Link to="/partner/register">Delivery Partner Signup</Link>
          </Button>
        </div>

        <ul className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm text-slate-600 dark:text-slate-300">
          <li className="flex items-center gap-3 justify-center">
          <span className="inline-flex items-center justify-center w-8 h-8 bg-indigo-50 text-indigo-600 rounded-full">✓</span>
          Real-time order & delivery tracking
          </li>
          <li className="flex items-center gap-3 justify-center">
          <span className="inline-flex items-center justify-center w-8 h-8 bg-teal-50 text-teal-600 rounded-full">✓</span>
          Quick onboarding for partners
          </li>
          <li className="flex items-center gap-3 justify-center">
          <span className="inline-flex items-center justify-center w-8 h-8 bg-slate-50 text-slate-700 rounded-full">✓</span>
          Intuitive dashboard & reports
          </li>
          <li className="flex items-center gap-3 justify-center">
          <span className="inline-flex items-center justify-center w-8 h-8 bg-amber-50 text-amber-600 rounded-full">✓</span>
          Secure & extensible platform
          </li>
        </ul>
        </div>
      </div>
      </div>
    </div>
  )
}
