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
        <footer className="mt-12">
          <div className="container mx-auto px-6 pb-8">
            <div className="text-center text-sm text-slate-500 dark:text-slate-400">
              <a
                href="https://github.com/Balaji-30/Delivery-Management-System-API"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Open project on GitHub"
                className="inline-flex items-center justify-center gap-2 hover:underline"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="18"
                  height="18"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  className="text-slate-600 dark:text-slate-300"
                  aria-hidden="true"
                >
                  <path d="M12 .5C5.73.5.75 5.48.75 11.75c0 4.93 3.19 9.11 7.61 10.58.56.1.77-.24.77-.54 0-.27-.01-1-.01-1.95-3.09.67-3.75-1.49-3.75-1.49-.5-1.29-1.22-1.63-1.22-1.63-.99-.68.08-.67.08-.67 1.09.08 1.67 1.12 1.67 1.12.97 1.66 2.55 1.18 3.17.9.1-.7.38-1.18.69-1.45-2.47-.28-5.07-1.24-5.07-5.52 0-1.22.44-2.22 1.17-3-.12-.29-.51-1.45.11-3.02 0 0 .95-.31 3.12 1.16.9-.25 1.86-.38 2.82-.38.96 0 1.92.13 2.82.38 2.17-1.47 3.12-1.16 3.12-1.16.62 1.57.23 2.73.11 3.02.73.78 1.17 1.78 1.17 3 0 4.29-2.61 5.24-5.09 5.51.39.34.73 1.01.73 2.04 0 1.47-.01 2.66-.01 3.02 0 .3.21.65.78.54 4.42-1.48 7.61-5.65 7.61-10.58C23.25 5.48 18.27.5 12 .5z" />
                </svg>
                View source on GitHub
              </a>
            </div>
          </div>
        </footer>
      </div>

    </div>
  )
}
