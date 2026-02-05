import ActivityItem from "./ActivityItem";

export default function RecentActivity() {
    return (
        <div className="relative rounded-2xl bg-white border border-slate-400/50 p-6 shadow-lg shadow-slate-300/50 hover:shadow-xl transition-all duration-300 overflow-hidden">
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
    );
}
