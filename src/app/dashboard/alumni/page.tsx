import Link from "next/link";

import StatCard from "@/components/dashboard/alumni/StatCard";
import JobCard from "@/components/dashboard/alumni/JobCard";
import EventCard from "@/components/dashboard/alumni/EventCard";
import ActivityItem from "@/components/dashboard/alumni/ActivityItem";

export default function AlumniDashboard() {
    return (
        <div className="relative space-y-8">
            {/* Decorative background elements */}
            <div className="pointer-events-none absolute inset-0 overflow-hidden">

                <div className="absolute top-1/3 -left-20 h-64 w-64 rounded-full bg-blue-100 opacity-30 blur-3xl" />
                <div className="absolute bottom-20 right-1/4 h-48 w-48 rounded-full bg-violet-100 opacity-30 blur-3xl" />
            </div>

            {/* Page Header */}
            <div className="relative flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                    <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-900 via-slate-800 to-slate-700 bg-clip-text text-transparent">
                        Dashboard Overview
                    </h1>
                    <p className="mt-1.5 text-slate-500">
                        Track your applications, discover opportunities, and stay updated.
                    </p>
                </div>
                <div className="flex gap-3">

                </div>
            </div>

            {/* Stats Grid */}
            <div className="relative grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
                <StatCard
                    title="Total Applications"
                    value="12"
                    change="+3"
                    changeType="positive"
                    gradient="bg-gradient-to-br from-blue-500 to-blue-600"
                    icon={
                        <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                    }
                />
                <StatCard
                    title="Interviews Scheduled"
                    value="3"
                    change="+2"
                    changeType="positive"
                    gradient="bg-gradient-to-br from-emerald-500 to-emerald-600"
                    icon={
                        <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                    }
                />
                <StatCard
                    title="Profile Views"
                    value="156"
                    change="+23%"
                    changeType="positive"
                    gradient="bg-gradient-to-br from-violet-500 to-violet-600"
                    icon={
                        <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                    }
                />
                <StatCard
                    title="Saved Jobs"
                    value="24"
                    change="0"
                    changeType="neutral"
                    gradient="bg-gradient-to-br from-amber-500 to-amber-600"
                    icon={
                        <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                        </svg>
                    }
                />
            </div>

            {/* Main Grid */}
            <div className="relative grid gap-6 lg:grid-cols-3">
                {/* Recommended Jobs */}
                <div className="lg:col-span-2 flex flex-col">
                    <div className="relative h-full flex flex-col rounded-2xl bg-white/70 backdrop-blur-sm border border-slate-200/60 p-6 shadow-sm hover:shadow-lg hover:bg-white/90 transition-all duration-300 overflow-hidden">
                        {/* Subtle texture pattern */}
                        <div
                            className="pointer-events-none absolute inset-0 opacity-[0.015]"
                            style={{
                                backgroundImage: `repeating-linear-gradient(
                                    -45deg,
                                    transparent,
                                    transparent 6px,
                                    rgba(0,0,0,0.05) 6px,
                                    rgba(0,0,0,0.05) 7px
                                )`
                            }}
                        />
                        {/* Top shine */}
                        <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white to-transparent opacity-80" />
                        {/* Decorative orb */}
                        <div className="absolute -top-10 -right-10 w-40 h-40 bg-gradient-to-br from-emerald-100/50 to-transparent rounded-full blur-2xl" />
                        <div className="relative z-10 mb-6 flex items-center justify-between">
                            <div>
                                <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                                    <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-100 text-emerald-600">
                                        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                                        </svg>
                                    </span>
                                    Recommended For You
                                </h2>
                                <p className="mt-1 text-sm text-slate-500">Based on your profile and preferences</p>
                            </div>
                            <Link href="/dashboard/alumni/jobs" className="group text-sm font-medium text-emerald-600 hover:text-emerald-700 flex items-center gap-1">
                                View all
                                <svg className="h-4 w-4 transition-transform group-hover:translate-x-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                </svg>
                            </Link>
                        </div>
                        <div className="relative z-10 flex-1 flex flex-col gap-4">
                            <JobCard
                                title="Junior Software Developer"
                                company="Accenture Philippines"
                                location="BGC, Taguig"
                                salary="₱35k - ₱50k"
                                type="Full-time"
                                postedAgo="2 days ago"
                                logo="A"
                                className="flex-1"
                            />
                            <JobCard
                                title="IT Support Specialist"
                                company="Globe Telecom"
                                location="Makati City"
                                salary="₱25k - ₱35k"
                                type="Full-time"
                                postedAgo="3 days ago"
                                logo="G"
                                className="flex-1"
                            />
                            <JobCard
                                title="Web Developer Intern"
                                company="Freelancer.com"
                                location="Remote"
                                salary="₱15k - ₱20k"
                                type="Internship"
                                postedAgo="1 week ago"
                                logo="F"
                                className="flex-1"
                            />
                        </div>
                    </div>
                </div>

                {/* Right Column */}
                <div className="flex flex-col gap-6 h-full">
                    {/* Profile Completion - Enhanced */}
                    <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-emerald-500 via-emerald-600 to-emerald-700 p-6 text-white shadow-xl shadow-emerald-500/20">
                        {/* Decorative elements */}
                        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(255,255,255,0.15),transparent_50%)]" />
                        <div className="absolute -bottom-8 -right-8 h-32 w-32 rounded-full bg-white/10 blur-xl" />
                        <div className="absolute top-0 right-0 h-20 w-20 rounded-full bg-emerald-400/30 blur-2xl" />

                        <div className="relative">
                            <div className="flex items-center justify-between">
                                <h3 className="font-bold text-lg">Profile Strength</h3>
                                <span className="rounded-full bg-white/20 backdrop-blur-sm px-3 py-1 text-sm font-bold shadow-sm">75%</span>
                            </div>

                            {/* Enhanced progress bar */}
                            <div className="mt-4 h-3 overflow-hidden rounded-full bg-white/20 backdrop-blur-sm">
                                <div className="h-full w-3/4 rounded-full bg-gradient-to-r from-white via-emerald-200 to-white relative overflow-hidden transition-all duration-500">
                                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/50 to-transparent -translate-x-full animate-[shimmer_2s_infinite]" />
                                </div>
                            </div>

                            <p className="mt-4 text-sm text-emerald-100/90">
                                Add your work experience to boost your profile visibility.
                            </p>

                            <Link
                                href="/dashboard/alumni/profile"
                                className="mt-5 inline-flex items-center gap-2 rounded-xl bg-white px-4 py-2.5 text-sm font-semibold text-emerald-700 shadow-lg transition-all hover:bg-emerald-50 hover:shadow-xl hover:-translate-y-0.5"
                            >
                                Complete Profile
                                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                </svg>
                            </Link>
                        </div>
                    </div>

                    {/* Quick Actions - Enhanced */}
                    <div className="relative flex-1 flex flex-col justify-center rounded-2xl bg-white/70 backdrop-blur-sm border border-slate-200/60 p-6 shadow-sm hover:shadow-lg hover:bg-white/90 transition-all duration-300 overflow-hidden">
                        {/* Subtle texture */}
                        <div
                            className="pointer-events-none absolute inset-0 opacity-[0.012]"
                            style={{
                                backgroundImage: 'radial-gradient(circle at 1px 1px, rgb(0,0,0) 0.5px, transparent 0)',
                                backgroundSize: '12px 12px'
                            }}
                        />
                        {/* Top shine */}
                        <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white to-transparent opacity-80" />

                        <h3 className="relative z-10 font-bold text-slate-900 flex items-center gap-2">
                            <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-slate-100">
                                <svg className="h-4 w-4 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                            </span>
                            Quick Actions
                        </h3>
                        <div className="relative z-10 mt-4 grid grid-cols-2 gap-3 flex-1">
                            <Link
                                href="/dashboard/alumni/profile"
                                className="group flex flex-col items-center justify-center gap-2.5 rounded-xl border border-slate-100 bg-slate-50/50 p-3 lg:p-4 text-center transition-all duration-300 hover:border-emerald-200 hover:bg-emerald-50 hover:shadow-md hover:-translate-y-0.5"
                            >
                                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-100 text-emerald-600 transition-transform duration-300 group-hover:scale-110">
                                    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                                    </svg>
                                </div>
                                <span className="text-xs font-medium text-slate-700 group-hover:text-emerald-700">Upload Resume</span>
                            </Link>
                            <Link
                                href="/dashboard/alumni/applications"
                                className="group flex flex-col items-center justify-center gap-2.5 rounded-xl border border-slate-100 bg-slate-50/50 p-3 lg:p-4 text-center transition-all duration-300 hover:border-blue-200 hover:bg-blue-50 hover:shadow-md hover:-translate-y-0.5"
                            >
                                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 text-blue-600 transition-transform duration-300 group-hover:scale-110">
                                    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                                    </svg>
                                </div>
                                <span className="text-xs font-medium text-slate-700 group-hover:text-blue-700">Track Applications</span>
                            </Link>
                            <Link
                                href="/dashboard/alumni/events"
                                className="group flex flex-col items-center justify-center gap-2.5 rounded-xl border border-slate-100 bg-slate-50/50 p-3 lg:p-4 text-center transition-all duration-300 hover:border-violet-200 hover:bg-violet-50 hover:shadow-md hover:-translate-y-0.5"
                            >
                                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-violet-100 text-violet-600 transition-transform duration-300 group-hover:scale-110">
                                    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                    </svg>
                                </div>
                                <span className="text-xs font-medium text-slate-700 group-hover:text-violet-700">Find Events</span>
                            </Link>
                            <Link
                                href="/dashboard/alumni/settings"
                                className="group flex flex-col items-center justify-center gap-2.5 rounded-xl border border-slate-100 bg-slate-50/50 p-3 lg:p-4 text-center transition-all duration-300 hover:border-amber-200 hover:bg-amber-50 hover:shadow-md hover:-translate-y-0.5"
                            >
                                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-amber-100 text-amber-600 transition-transform duration-300 group-hover:scale-110">
                                    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                    </svg>
                                </div>
                                <span className="text-xs font-medium text-slate-700 group-hover:text-amber-700">Settings</span>
                            </Link>
                        </div>
                    </div>
                </div>
            </div>

            {/* Bottom Grid */}
            <div className="relative grid gap-6 lg:grid-cols-2">
                {/* Upcoming Events */}
                <div className="relative rounded-2xl bg-white/70 backdrop-blur-sm border border-slate-200/60 p-6 shadow-sm hover:shadow-lg hover:bg-white/90 transition-all duration-300 overflow-hidden">
                    {/* Subtle texture */}
                    <div
                        className="pointer-events-none absolute inset-0 opacity-[0.012]"
                        style={{
                            backgroundImage: `repeating-linear-gradient(
                                45deg,
                                transparent,
                                transparent 5px,
                                rgba(0,0,0,0.03) 5px,
                                rgba(0,0,0,0.03) 6px
                            )`
                        }}
                    />
                    {/* Top shine */}
                    <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white to-transparent opacity-80" />
                    {/* Decorative orb */}
                    <div className="absolute -top-8 -left-8 w-32 h-32 bg-gradient-to-br from-violet-100/40 to-transparent rounded-full blur-2xl" />
                    <div className="relative z-10 mb-6 flex items-center justify-between">
                        <div>
                            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                                <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-violet-100 text-violet-600">
                                    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                    </svg>
                                </span>
                                Upcoming Events
                            </h2>
                            <p className="mt-1 text-sm text-slate-500">Don&apos;t miss these opportunities</p>
                        </div>
                        <Link href="/dashboard/alumni/events" className="group text-sm font-medium text-emerald-600 hover:text-emerald-700 flex items-center gap-1">
                            View all
                            <svg className="h-4 w-4 transition-transform group-hover:translate-x-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                            </svg>
                        </Link>
                    </div>
                    <div className="relative z-10 space-y-4">
                        <EventCard
                            title="PLP Career Fair 2024"
                            date="15 Feb"
                            time="9:00 AM - 5:00 PM"
                            location="PLP Main Campus"
                            attendees={234}
                            type="Career Fair"
                        />
                        <EventCard
                            title="Resume Writing Workshop"
                            date="20 Feb"
                            time="2:00 PM - 4:00 PM"
                            location="Virtual Event"
                            attendees={89}
                            type="Workshop"
                        />
                    </div>
                </div>

                {/* Recent Activity */}
                <div className="relative rounded-2xl bg-white/70 backdrop-blur-sm border border-slate-200/60 p-6 shadow-sm hover:shadow-lg hover:bg-white/90 transition-all duration-300 overflow-hidden">
                    {/* Subtle texture */}
                    <div
                        className="pointer-events-none absolute inset-0 opacity-[0.01]"
                        style={{
                            backgroundImage: 'radial-gradient(circle at 2px 2px, rgb(0,0,0) 0.5px, transparent 0)',
                            backgroundSize: '14px 14px'
                        }}
                    />
                    {/* Top shine */}
                    <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white to-transparent opacity-80" />
                    {/* Decorative orb */}
                    <div className="absolute -top-8 -right-8 w-32 h-32 bg-gradient-to-bl from-blue-100/40 to-transparent rounded-full blur-2xl" />
                    <div className="relative z-10 mb-6">
                        <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-100 text-blue-600">
                                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </span>
                            Recent Activity
                        </h2>
                        <p className="mt-1 text-sm text-slate-500">Your latest actions and updates</p>
                    </div>
                    <div className="relative z-10 space-y-1">
                        <ActivityItem
                            title="Application Submitted"
                            description="Junior Developer at Accenture Philippines"
                            time="2 hours ago"
                            iconBg="bg-emerald-100 text-emerald-600"
                            icon={
                                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                </svg>
                            }
                        />
                        <ActivityItem
                            title="Profile Updated"
                            description="Added new skills: React, TypeScript"
                            time="Yesterday"
                            iconBg="bg-blue-100 text-blue-600"
                            icon={
                                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                </svg>
                            }
                        />
                        <ActivityItem
                            title="Interview Scheduled"
                            description="Globe Telecom - Feb 18, 2024 at 10:00 AM"
                            time="2 days ago"
                            iconBg="bg-violet-100 text-violet-600"
                            icon={
                                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                            }
                        />
                        <ActivityItem
                            title="Job Saved"
                            description="Technical Support at DITO Telecommunity"
                            time="3 days ago"
                            iconBg="bg-amber-100 text-amber-600"
                            isLast={true}
                            icon={
                                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                                </svg>
                            }
                        />
                    </div>
                </div>
            </div>
        </div>
    );
}
