"use client";

import { useState } from "react";
import Link from "next/link";

import { usePathname } from "next/navigation";

import {
    HomeIcon,
    BriefcaseIcon,
    CalendarIcon,
    UserIcon,
    DocumentIcon,
    SettingsIcon,
    LogoutIcon,
    BellIcon,
    MenuIcon,
    CloseIcon,
    ChevronIcon
} from "@/components/dashboard/icons";

const navItems = [
    { name: "Overview", href: "/dashboard/alumni", icon: HomeIcon },
    { name: "Job Listings", href: "/dashboard/alumni/jobs", icon: BriefcaseIcon },
    { name: "Events", href: "/dashboard/alumni/events", icon: CalendarIcon },
    { name: "My Applications", href: "/dashboard/alumni/applications", icon: DocumentIcon },
    { name: "Profile", href: "/dashboard/alumni/profile", icon: UserIcon },
];

export default function AlumniLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const pathname = usePathname();
    const [sidebarOpen, setSidebarOpen] = useState(false);

    return (
        <div className="flex h-screen w-full bg-slate-50">
            {/* Mobile sidebar overlay */}
            {sidebarOpen && (
                <div
                    className="fixed inset-0 z-40 bg-black/20 backdrop-blur-sm lg:hidden transition-opacity duration-300"
                    onClick={() => setSidebarOpen(false)}
                />
            )}

            {/* Sidebar - Modern Corporate Light Design */}
            <aside
                className={`
                    fixed inset-y-0 left-0 z-50 w-[272px] transform
                    bg-white border-r border-slate-200/80
                    transition-all duration-300 ease-out lg:relative lg:translate-x-0
                    ${sidebarOpen ? "translate-x-0 shadow-2xl" : "-translate-x-full"}
                    flex flex-col overflow-hidden
                `}
            >


                {/* Logo Section */}
                <div className="relative flex h-[72px] items-center justify-between px-5 border-b border-slate-100">
                    <Link href="/" className="flex items-center gap-3 group">
                        <div className="relative h-12 w-12 flex-shrink-0">
                            <img
                                src="/plp-logo.png"
                                alt="PLP Logo"
                                width="48"
                                height="48"
                                className="object-contain p-0.5"
                            />
                        </div>
                        <div className="flex flex-col">
                            <span className="text-[15px] font-bold text-slate-800 tracking-tight">P.A.C.E.</span>
                            <span className="text-[10px] text-emerald-600 font-semibold tracking-wide uppercase">Alumni Portal</span>
                        </div>
                    </Link>
                    <button
                        className="rounded-lg p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors lg:hidden"
                        onClick={() => setSidebarOpen(false)}
                    >
                        <CloseIcon />
                    </button>
                </div>

                {/* Navigation Section Label */}
                <div className="relative px-5 pt-6 pb-2">
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-[0.1em]">Navigation</span>
                </div>

                {/* Navigation */}
                <nav className="relative flex-1 overflow-y-auto px-3 pb-4">
                    <div className="space-y-1">
                        {navItems.map((item) => {
                            const isActive = pathname === item.href;
                            return (
                                <Link
                                    key={item.name}
                                    href={item.href}
                                    className={`
                                        group relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-[13px] font-medium
                                        transition-all duration-200 ease-out
                                        ${isActive
                                            ? "bg-gradient-to-r from-emerald-50 to-emerald-50/50 text-emerald-700 shadow-sm ring-1 ring-emerald-100"
                                            : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
                                        }
                                    `}
                                >
                                    {/* Active indicator line */}
                                    {isActive && (
                                        <div className="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-7 bg-gradient-to-b from-emerald-500 to-emerald-600 rounded-r-full shadow-sm" />
                                    )}

                                    <span className={`
                                        flex items-center justify-center w-8 h-8 rounded-lg transition-all duration-200
                                        ${isActive
                                            ? "bg-emerald-100 text-emerald-600"
                                            : "bg-slate-100 text-slate-400 group-hover:bg-slate-200/70 group-hover:text-slate-600"
                                        }
                                    `}>
                                        <item.icon />
                                    </span>
                                    <span className="flex-1">{item.name}</span>

                                    {/* Hover arrow indicator */}
                                    <svg
                                        className={`w-4 h-4 transition-all duration-200 ${isActive ? 'text-emerald-500 opacity-100' : 'opacity-0 -translate-x-2 group-hover:opacity-40 group-hover:translate-x-0 text-slate-400'}`}
                                        fill="none"
                                        viewBox="0 0 24 24"
                                        stroke="currentColor"
                                    >
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                    </svg>
                                </Link>
                            );
                        })}
                    </div>

                    {/* Preferences Section */}
                    <div className="mt-6">
                        <div className="px-3 pb-2">
                            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-[0.1em]">Preferences</span>
                        </div>
                        <Link
                            href="/dashboard/alumni/settings"
                            className={`
                                group relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-[13px] font-medium
                                transition-all duration-200 ease-out
                                ${pathname === "/dashboard/alumni/settings"
                                    ? "bg-gradient-to-r from-emerald-50 to-emerald-50/50 text-emerald-700 shadow-sm ring-1 ring-emerald-100"
                                    : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
                                }
                            `}
                        >
                            {pathname === "/dashboard/alumni/settings" && (
                                <div className="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-7 bg-gradient-to-b from-emerald-500 to-emerald-600 rounded-r-full shadow-sm" />
                            )}
                            <span className={`
                                flex items-center justify-center w-8 h-8 rounded-lg transition-all duration-200
                                ${pathname === "/dashboard/alumni/settings"
                                    ? "bg-emerald-100 text-emerald-600"
                                    : "bg-slate-100 text-slate-400 group-hover:bg-slate-200/70 group-hover:text-slate-600"
                                }
                            `}>
                                <SettingsIcon />
                            </span>
                            <span className="flex-1">Settings</span>
                            <svg
                                className={`w-4 h-4 transition-all duration-200 ${pathname === "/dashboard/alumni/settings" ? 'text-emerald-500 opacity-100' : 'opacity-0 -translate-x-2 group-hover:opacity-40 group-hover:translate-x-0 text-slate-400'}`}
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                            </svg>
                        </Link>
                    </div>
                </nav>

                {/* User Section - Premium card design */}
                <div className="relative p-3 border-t border-slate-100">
                    {/* Subtle top highlight */}
                    <div className="absolute inset-x-3 -top-px h-px bg-gradient-to-r from-transparent via-emerald-200/50 to-transparent" />

                    <div className="rounded-2xl bg-gradient-to-br from-slate-50 to-slate-100/50 p-3 ring-1 ring-slate-200/60 shadow-sm">
                        <div className="flex items-center gap-3">
                            {/* Avatar with status indicator */}
                            <div className="relative">
                                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-400 via-emerald-500 to-teal-500 text-sm font-bold text-white shadow-md shadow-emerald-500/20">
                                    JD
                                </div>
                                {/* Online status */}
                                <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-emerald-400 rounded-full ring-2 ring-white" />
                            </div>

                            <div className="flex-1 min-w-0">
                                <p className="text-sm font-semibold text-slate-800 truncate">Juan Dela Cruz</p>
                                <p className="text-[11px] text-slate-500 truncate">BSIT Graduate 2024</p>
                            </div>

                            {/* Sign out button - compact */}
                            <Link
                                href="/"
                                className="p-2 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 transition-all duration-200"
                                title="Sign out"
                            >
                                <LogoutIcon />
                            </Link>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Content Area */}
            <div className="flex flex-1 flex-col overflow-hidden">
                {/* Top Header - Enhanced with texture */}
                <header className="relative flex h-16 items-center justify-between border-b border-slate-200/80 bg-white/90 backdrop-blur-sm px-4 lg:px-6 overflow-hidden">
                    {/* Subtle header texture */}
                    <div
                        className="pointer-events-none absolute inset-0 opacity-[0.02]"
                        style={{
                            backgroundImage: 'linear-gradient(90deg, transparent 0%, transparent 50%, rgba(0,0,0,0.02) 50%, rgba(0,0,0,0.02) 100%)',
                            backgroundSize: '4px 4px'
                        }}
                    />
                    {/* Decorative gradient line at bottom */}
                    <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-slate-200 to-transparent" />

                    <div className="relative flex items-center gap-3">
                        <button
                            className="rounded-lg p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-600 lg:hidden"
                            onClick={() => setSidebarOpen(true)}
                        >
                            <MenuIcon />
                        </button>
                        <div>
                            <h1 className="text-base font-semibold text-slate-900">Welcome back, Juan!</h1>
                            <p className="text-xs text-slate-500 hidden sm:block">Here&apos;s what&apos;s happening with your career journey</p>
                        </div>
                    </div>

                    <div className="relative flex items-center gap-2">
                        {/* Notifications */}
                        <button className="relative rounded-xl p-2.5 text-slate-400 transition-all duration-200 hover:bg-slate-100 hover:text-slate-600 hover:shadow-sm">
                            <BellIcon />
                            <span className="absolute right-2 top-2 flex h-2 w-2">
                                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75" />
                                <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-500 ring-2 ring-white" />
                            </span>
                        </button>
                    </div>
                </header>

                {/* Page Content */}
                <main className="relative flex-1 overflow-y-auto bg-gradient-to-br from-slate-50 via-slate-50 to-slate-100/80 p-4 lg:p-6">
                    {/* Subtle noise texture overlay */}
                    <div
                        className="pointer-events-none fixed inset-0 z-0 opacity-[0.015]"
                        style={{
                            backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
                        }}
                    />

                    {/* Subtle dot grid pattern */}
                    <div
                        className="pointer-events-none fixed inset-0 z-0 opacity-[0.03]"
                        style={{
                            backgroundImage: 'radial-gradient(circle at 1px 1px, rgb(100,116,139) 1px, transparent 0)',
                            backgroundSize: '24px 24px'
                        }}
                    />

                    {/* Decorative corner accent */}

                    <div className="pointer-events-none fixed bottom-0 left-64 w-80 h-80 z-0">
                        <div className="absolute inset-0 bg-gradient-to-tr from-blue-100/30 via-transparent to-transparent blur-3xl" />
                    </div>

                    <div className="relative z-10">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
}
