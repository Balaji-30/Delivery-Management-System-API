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
import { toast } from "sonner"

export function LoginForm({
  className,
  user,
  ...props
}:{user:UserType} & React.ComponentProps<"form">) {

  const {login}=useContext(AuthContext)

  function loginUser(data: FormData) {
    const email = data.get("email")
    const password = data.get("password")
    if ( !email || !password ) {
      return
    }
    toast.info("Expect ~2 min delay because of free tier hosting. Thanks for your patience.")
    login(user,email.toString(), password.toString())
  }
  return (
    <form className={cn("flex flex-col gap-6", className)} {...props} action={loginUser}>
      <FieldGroup>
        <div className="flex flex-col items-center gap-1 text-center">
          <h1 className="text-2xl font-bold">Login to your Shippin account</h1>
          <p className="text-muted-foreground text-sm text-balance">
            Enter your email below to login to your account
          </p>
        </div>
        <Field>
          <FieldLabel htmlFor="email">Email</FieldLabel>
          <Input id="email" type="email" name="email" placeholder="user@example.com" required />
        </Field>
        <Field>
          <div className="flex items-center">
            <FieldLabel htmlFor="password">Password</FieldLabel>
            <a
              href={`/${user}/forgot-password`}
              className="ml-auto text-sm underline-offset-4 hover:underline"
            >
              Forgot your password?
            </a>
          </div>
          <Input id="password" name="password" type="password" required />
        </Field>
        <Field>
          <Button type="submit">Login</Button>
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
