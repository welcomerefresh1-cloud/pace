import Link from "next/link";
import JobCard from "./JobCard";

export default function RecommendedJobs() {
    return (
        <div className="lg:col-span-2 flex flex-col">
            <div className="relative h-full flex flex-col rounded-2xl bg-white border border-slate-400/50 p-6 shadow-lg shadow-slate-300/50 hover:shadow-xl transition-all duration-300 overflow-hidden">
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
    );
}
