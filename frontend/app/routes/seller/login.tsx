import { Package } from "lucide-react"
import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router";
import { toast } from "sonner";

import { LoginForm } from "~/components/login-form"

export default function SellerLoginPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    // Check for SUCCESS
    if (searchParams.get("verified") === "true") {
      toast.success("Email verified successfully! Please login.");
      
      // Clean the URL so the user doesn't see the ugly param
      cleanUrl();
    }

    // Check for ERROR
    if (searchParams.get("verified") === "false") {
      toast.error("Verification link expired or invalid. Please try registering again.");
      cleanUrl();
      navigate("/seller/login")
    } 
  }, [searchParams]);

  // Helper to remove params without refreshing the page
  const cleanUrl = () => {
    setSearchParams((params) => {
      params.delete("verified");
      params.delete("error");
      return params;
    });
  };

  return (
    <div className="grid min-h-svh lg:grid-cols-2">
      <div className="flex flex-col gap-4 p-6 md:p-10">
        <div className="flex justify-center gap-2 md:justify-start">
          <a href="/" className="flex items-center gap-2 font-medium">
            <div className="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
              <Package className="size-4" />
            </div>
            Shippin
          </a>
        </div>
        <div className="flex flex-1 items-center justify-center">
          <div className="w-full max-w-xs">
            <LoginForm user="seller"/>
          </div>
        </div>
      </div>
      <div className="bg-muted relative hidden lg:block">
        <img
          src="/shippin.png"
          alt="Image"
          className="absolute inset-0 h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
        />
      </div>
    </div>
  )
}
