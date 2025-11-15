import { cn } from "~/lib/utils"
import { Button } from "~/components/ui/button"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldSeparator,
} from "~/components/ui/field"
import { Input } from "~/components/ui/input"
import { toast } from "sonner"
import type { SellerCreate } from "~/lib/client"
import { useMutation } from "@tanstack/react-query"
import api from "~/lib/api"
import type { AxiosError } from "axios"
import { useNavigate } from "react-router"

export function SignupForm({
  className,
  ...props
}: React.ComponentProps<"form">) {

  const navigate = useNavigate();

  const sellers = useMutation({
    mutationFn: (data: SellerCreate) => api.seller.registerSeller(data),
    onSuccess: (response) => {
      toast(`Account verification email sent to (#${response.data.email}). Please verify.`)
      navigate("/seller/login")
    },
    onError: (error) => {
      const apiError = error as AxiosError
      toast.error(`Error:${apiError.status}. Failed to create account. `)
    }

  })

  
 async function registerSeller(data: FormData) {

    const name = data.get("fullname")?.toString()
    const email = data.get("email")?.toString()
    const password1 = data.get("password1")?.toString()
    const password2 = data.get("password2")?.toString()
    const zipcode = data.get("zipcode")?.toString()

    if(password1!== password2){
      toast.error("Passwords entered do not match!")
      return
    }

    if (!name || !email || !password1 || !password2 || !zipcode) {
      return
    }

    const seller = {
      name: name,
      email: email,
      password: password1,
      zipcode: parseInt(zipcode),
    }
    sellers.mutate(seller)
  }

  return (
    <form className={cn("flex flex-col gap-6", className)} {...props} action={registerSeller}>
      <FieldGroup>
        <div className="flex flex-col items-center gap-1 text-center">
          <h1 className="text-2xl font-bold">Create your Seller account</h1>
          <p className="text-muted-foreground text-sm text-balance">
            Enter your details below to create an account
          </p>
        </div>
        <Field>
          <FieldLabel htmlFor="name">Full Name</FieldLabel>
          <Input id="name" name="fullname" type="text" placeholder="John Doe" required />
        </Field>
        <Field>
          <FieldLabel htmlFor="email">Email</FieldLabel>
          <Input id="email" name="email" type="email" placeholder="m@example.com" required />
          
        </Field>
        <Field>
          <FieldLabel htmlFor="password">Password</FieldLabel>
          <Input id="password" name="password1" type="password" minLength={5} required />
          {/* <FieldDescription>
            Must be at least 8 characters long.
          </FieldDescription> */}
        </Field>
        <Field>
          <FieldLabel htmlFor="confirm-password">Confirm Password</FieldLabel>
          <Input id="confirm-password" name="password2" type="password" minLength={5} required />
          <FieldDescription>Please confirm your password.</FieldDescription>
        </Field>
        <Field>
          <FieldLabel htmlFor="zip-code">Zip Code</FieldLabel>
          <Input id="zip-code" name="zipcode" type="text" inputMode="numeric" pattern="[0-9]*" minLength={5} required />
          <FieldDescription>Zip code from seller warehouse.</FieldDescription>
        </Field>
        <Field>
          <Button type="submit">Create Account</Button>
        </Field>
        <Field>
          <FieldDescription className="px-6 text-center">
            Already have an account? <a href="/seller/login">Sign in</a>
          </FieldDescription>
        </Field>
      </FieldGroup>
    </form>
  )
}
