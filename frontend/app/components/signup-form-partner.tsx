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
import type { DeliveryPartnerCreate } from "~/lib/client"
import { useMutation } from "@tanstack/react-query"
import api from "~/lib/api"
import type { AxiosError } from "axios"
import { useNavigate } from "react-router"

export function SignupForm({
  className,
  ...props
}: React.ComponentProps<"form">) {

  const navigate = useNavigate();

  const partners = useMutation({
    mutationFn: (data: DeliveryPartnerCreate) => api.partner.registerDeliveryPartner(data),
    onSuccess: (response) => {
      toast(`Account verification email sent to (#${response.data.email}). Please verify.`)
      navigate("/partner/login")
    },
    onError: (error) => {
      const apiError = error as AxiosError
      toast.error(`Error:${apiError.status}. Failed to create account. `)
    }

  })

  
 async function registerPartner(data: FormData) {

    const name = data.get("name")?.toString()
    const email = data.get("email")?.toString()
    const password1 = data.get("password1")?.toString()
    const password2 = data.get("password2")?.toString()
    const capacity = data.get("handling_capacity")?.toString()
    const zipcode = data.get("zipcode")?.toString()

    if(password1!== password2){
      toast.error("Passwords entered do not match!")
      return
    }

    if (!name || !email || !password1 || !password2 || !zipcode || !capacity) {
      return
    }

    const zipCodesList = zipcode
      .split(",")                  // 1. Split into array
      .map((z) => z.trim())        // 2. Remove whitespace
      .filter((z) => z !== "")     // 3. Remove empty entries
      .map((z) => parseInt(z))     // 4. Convert to Integer
      .filter((z) => !isNaN(z));   // 5. Remove invalid numbers

      if (zipCodesList.length < 1){
        toast.error("Number of serviceable zipcodes")
        return
      }

    const partner = {
      name: name,
      email: email,
      password: password1,
      serviceable_zipcodes: zipCodesList,
      max_handling_capacity: parseInt(capacity)
    }
    partners.mutate(partner)
  }

  return (
    <form className={cn("flex flex-col gap-6", className)} {...props} action={registerPartner}>
      <FieldGroup>
        <div className="flex flex-col items-center gap-1 text-center">
          <h1 className="text-2xl font-bold">Create your account</h1>
        </div>
        <Field>
          <FieldLabel htmlFor="name">Name</FieldLabel>
          <Input id="name" name="name" type="text" placeholder="Rapido" required />
        </Field>
        <Field>
          <FieldLabel htmlFor="email">Email</FieldLabel>
          <Input id="email" name="email" type="email" placeholder="m@example.com" required />
        </Field>
        <Field>
          <FieldLabel htmlFor="password">Password</FieldLabel>
          <Input id="password" name="password1" type="password" minLength={5} required />
        </Field>
        <Field>
          <FieldLabel htmlFor="confirm-password">Confirm Password</FieldLabel>
          <Input id="confirm-password" name="password2" type="password" minLength={5} required />
        </Field>
        <Field>
          <FieldLabel htmlFor="handling-capacity">Handling Capacity</FieldLabel>
          <Input id="handling-capacity" name="handling_capacity" type="number" min={1} defaultValue={10} required />
          <FieldDescription>No. of shipments that can be handled at a time.</FieldDescription>
        </Field>
        <Field>
          <FieldLabel htmlFor="zip-code">Serviceable Zip Codes</FieldLabel>
          <Input 
            id="zip-code" 
            name="zipcode" 
            type="text"
            placeholder="570028, 560001, 560002" 
            required 
          />
          <FieldDescription>
            Separate multiple zip codes with commas (e.g.22202, 570028, 560011).
          </FieldDescription>
        </Field>
        <Field>
          <Button type="submit">Create Account</Button>
        </Field>
        <Field>
          <FieldDescription className="px-6 text-center">
            Already have an account? <a href="/partner/login">Sign in</a>
          </FieldDescription>
        </Field>
      </FieldGroup>
    </form>
  )
}
