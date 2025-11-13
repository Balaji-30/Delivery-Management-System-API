import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";
import { Button } from "~/components/ui/button";
import { Link } from "react-router";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  return( 
  <div><Button asChild>
    <Link to="/seller/login">Seller Login</Link>
    </Button>
    <Button asChild>
    <Link to="/partner/login">Delivery Partner Login</Link>
    </Button>
    </div>
  )
}
