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
                    bg-white border-r-2 border-slate-300 shadow-lg shadow-slate-200/50
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
                {/* Top Header - Modern Professional Design */}
                <header className="relative flex h-20 items-center justify-between border-b-2 border-slate-300 bg-gradient-to-r from-white via-white to-slate-50 shadow-md shadow-slate-200/50 px-4 lg:px-8 overflow-hidden">
                    {/* Decorative background elements */}
                    <div className="pointer-events-none absolute inset-0">
                        {/* Subtle grid pattern */}
                        <div
                            className="absolute inset-0 opacity-[0.03]"
                            style={{
                                backgroundImage: 'radial-gradient(circle at 1px 1px, rgb(0,0,0) 0.5px, transparent 0)',
                                backgroundSize: '20px 20px'
                            }}
                        />
                        {/* Decorative gradient orb */}
                        <div className="absolute -top-10 right-1/4 w-40 h-40 bg-gradient-to-br from-emerald-100/40 to-transparent rounded-full blur-3xl" />
                    </div>

                    {/* Bottom accent line */}
                    <div className="absolute bottom-0 left-0 right-0 h-[2px] bg-gradient-to-r from-emerald-500 via-emerald-400 to-transparent" />

                    {/* Left Section - Welcome */}
                    <div className="relative flex items-center gap-4">
                        <button
                            className="rounded-xl p-2.5 text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-all duration-200 lg:hidden"
                            onClick={() => setSidebarOpen(true)}
                        >
                            <MenuIcon />
                        </button>
                        <div className="flex items-center gap-4">
                            {/* Date & Time Badge - Modern Split Design */}
                            <div className="hidden md:flex items-center gap-0 rounded-xl overflow-hidden shadow-sm border border-slate-200">
                                {/* Day Number */}
                                <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-br from-emerald-500 to-emerald-600 text-white">
                                    <span className="text-xl font-bold">5</span>
                                </div>
                                {/* Month & Day */}
                                <div className="flex flex-col justify-center px-3 py-1.5 bg-white">
                                    <span className="text-xs font-bold text-slate-800 uppercase tracking-wide">Feb 2026</span>
                                    <span className="text-[10px] text-slate-500 font-medium">Wednesday</span>
                                </div>
                            </div>
                            <div className="h-8 w-px bg-slate-200 hidden md:block" />
                            <div>
                                <h1 className="text-lg font-bold bg-gradient-to-r from-slate-900 via-slate-800 to-slate-600 bg-clip-text text-transparent">Welcome back, Juan!</h1>
                                <p className="text-sm text-slate-500 hidden sm:block">Here&apos;s what&apos;s happening with your career journey</p>
                            </div>
                        </div>
                    </div>

                    {/* Right Section - Actions */}
                    <div className="relative flex items-center gap-3">
                        {/* Search Bar */}
                        <div className="hidden lg:flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-100/80 border border-slate-200 hover:border-slate-300 hover:bg-slate-100 transition-all duration-200 group">
                            <svg className="h-4 w-4 text-slate-400 group-hover:text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                            <input
                                type="text"
                                placeholder="Search jobs, events..."
                                className="bg-transparent text-sm text-slate-600 placeholder:text-slate-400 focus:outline-none w-40 xl:w-48"
                            />
                            <kbd className="hidden xl:flex items-center gap-0.5 px-1.5 py-0.5 rounded bg-slate-200/80 text-[10px] font-medium text-slate-500">
                                ⌘K
                            </kbd>
                        </div>

                        {/* Notifications */}
                        <button className="relative flex items-center justify-center h-10 w-10 rounded-xl bg-slate-100/80 border border-slate-200 text-slate-500 transition-all duration-200 hover:bg-emerald-50 hover:border-emerald-200 hover:text-emerald-600 hover:shadow-sm">
                            <BellIcon />
                            <span className="absolute -right-0.5 -top-0.5 flex h-4 w-4">
                                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75" />
                                <span className="relative inline-flex h-4 w-4 items-center justify-center rounded-full bg-emerald-500 text-[9px] font-bold text-white ring-2 ring-white">3</span>
                            </span>
                        </button>

                        {/* Quick Settings */}
                        <button className="hidden sm:flex items-center justify-center h-10 w-10 rounded-xl bg-slate-100/80 border border-slate-200 text-slate-500 transition-all duration-200 hover:bg-slate-100 hover:border-slate-300 hover:text-slate-600 hover:shadow-sm">
                            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                        </button>


                    </div>
                </header>

                {/* Page Content */}
                <main className="relative flex-1 overflow-y-auto bg-gradient-to-br from-slate-100 via-slate-100 to-slate-200/80 p-4 lg:p-6">
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
