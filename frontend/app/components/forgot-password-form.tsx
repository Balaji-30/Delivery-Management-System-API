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
import { AuthContext, type UserType } from "~/contexts/AuthContext"
import { useContext } from "react"
import api from "~/lib/api"
import { toast } from "sonner"

export function ForgotPasswordForm({
  className,
  user,
  ...props
}:{user:UserType} & React.ComponentProps<"form">) {

  const {login}=useContext(AuthContext)

  async function sendResetLink(data: FormData) {
    const email = data.get("email")?.toString()
    if ( !email ) {
      return
    }
    const userApi = user==="seller" ? api.seller.sellerForgotPassword : api.partner.deliveryPartnerForgotPassword 
    await userApi({email})
    toast.success("If an account with that email exists, a reset link has been sent.")
  }
  return (
    <form className={cn("flex flex-col gap-6", className)} {...props} action={sendResetLink}>
      <FieldGroup>
        <div className="flex flex-col items-center gap-1 text-center">
          <h1 className="text-2xl font-bold">Recover your Shippin account</h1>
          <p className="text-muted-foreground text-sm text-balance">
            Enter your email below to receive a password reset link
          </p>
        </div>
        <Field>
          <FieldLabel htmlFor="email">Email</FieldLabel>
          <Input id="email" type="email" name="email" placeholder="user@example.com" required />
        </Field>
        
        <Field>
          <Button type="submit">Send Reset Link</Button>
        </Field>
        <FieldDescription className="text-center">
          Don&apos;t have an account?{" "}
          <a href={`/${user}/register`} className="underline underline-offset-4">
            Sign up
          </a>
        </FieldDescription>
      </FieldGroup>
    </form>
  )
}
