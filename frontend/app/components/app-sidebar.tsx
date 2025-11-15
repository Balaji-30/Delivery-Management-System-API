import * as React from "react"
import { GalleryVerticalEnd, Package } from "lucide-react"

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "~/components/ui/sidebar"
import { useContext } from "react"
import { AuthContext } from "~/contexts/AuthContext"

// This is sample data.


export function AppSidebar({currentRoute, ...props }:{currentRoute : string} & React.ComponentProps<typeof Sidebar>) {

  const { user }=useContext(AuthContext)

  const menuItems=[
    {
      title:"Dashboard",
      url:"/dashboard"
    },
    {
      title:"Account",
      url:"/account"
    }
  ]
  return (
    <Sidebar variant="floating" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <a href="/">
                <div className="bg-sidebar-primary text-sidebar-primary-foreground flex aspect-square size-8 items-center justify-center rounded-lg">
                  <Package className="size-4" />
                </div>
                <div className="flex flex-col gap-0.5 leading-none">
                  <span className="font-medium" >Shippin</span>
                  <span className="">DMS v1.0.0</span>
                </div>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarMenu className="gap-1">
            {menuItems.map((item) => (
              <SidebarMenuItem key={item.title}>
                <SidebarMenuButton asChild isActive={currentRoute === item.title}>
                  <a href={item.url} >
                    {item.title}
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
            ))}
            {
              user==="seller" && (
                <SidebarMenuItem>
                  <SidebarMenuButton asChild isActive={currentRoute === "Submit Shipment"}>
                  <a href="/submit-shipment">
                  Submit Shipment
                  </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              )
            }
            {
              user==="partner" && (
                <SidebarMenuItem>
                  <SidebarMenuButton asChild isActive={currentRoute === "Update Shipment"}>
                  <a href="/update-shipment">
                  Update Shipment
                  </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              )
            }
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}
