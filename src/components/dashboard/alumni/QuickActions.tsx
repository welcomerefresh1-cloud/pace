import Link from "next/link";

export default function QuickActions() {
    return (
        <div className="relative flex-1 flex flex-col justify-center rounded-2xl bg-white border border-slate-400/50 p-6 shadow-lg shadow-slate-300/50 hover:shadow-xl transition-all duration-300 overflow-hidden">
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
    );
}
