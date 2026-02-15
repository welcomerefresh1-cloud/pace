"use client";

export default function DashboardHeader() {
    return (
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-emerald-600 via-emerald-500 to-teal-500 p-6 lg:p-8 text-white">
            {/* Decorative mesh */}
            <div className="absolute inset-0 opacity-30">
                <div className="absolute -top-20 -right-20 w-72 h-72 rounded-full bg-white/10 blur-3xl" />
                <div className="absolute -bottom-16 -left-16 w-56 h-56 rounded-full bg-teal-300/20 blur-3xl" />
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full bg-emerald-400/10 blur-3xl" />
            </div>

            {/* Grid overlay pattern */}
            <div className="absolute inset-0 opacity-[0.03]" style={{
                backgroundImage: `radial-gradient(circle at 1px 1px, white 1px, transparent 0)`,
                backgroundSize: '24px 24px',
            }} />

            <div className="relative flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
                {/* Left: Welcome */}
                <div className="flex items-center gap-5">
                    {/* Profile Ring */}
                    <div className="relative flex-shrink-0 hidden sm:block">
                        <svg className="w-20 h-20 -rotate-90" viewBox="0 0 80 80">
                            <circle cx="40" cy="40" r="34" fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth="5" />
                            <circle
                                cx="40" cy="40" r="34" fill="none"
                                stroke="white" strokeWidth="5"
                                strokeLinecap="round"
                                strokeDasharray={`${0.75 * 2 * Math.PI * 34} ${2 * Math.PI * 34}`}
                            />
                        </svg>
                        <div className="absolute inset-0 flex items-center justify-center">
                            <div className="w-14 h-14 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center text-lg font-bold">
                                JD
                            </div>
                        </div>
                        <div className="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-white text-emerald-600 flex items-center justify-center text-[10px] font-bold shadow-lg">
                            75%
                        </div>
                    </div>

                    <div>
                        <p className="text-emerald-100 text-sm font-medium">Good morning,</p>
                        <h1 className="text-2xl lg:text-3xl font-bold tracking-tight mt-0.5">Juan Dela Cruz</h1>
                        <p className="text-emerald-100/80 text-sm mt-1.5 max-w-md">
                            Your career journey is on track. Complete your profile to unlock more opportunities.
                        </p>
                    </div>
                </div>

                {/* Right: Quick Stats Pills */}
                <div className="flex flex-wrap gap-2.5">
                    <div className="flex items-center gap-2 bg-white/15 backdrop-blur-sm rounded-xl px-4 py-2.5 border border-white/10">
                        <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center">
                            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                        </div>
                        <div>
                            <p className="text-[10px] text-emerald-200 font-medium uppercase tracking-wider">Applications</p>
                            <p className="text-lg font-bold leading-tight">12</p>
                        </div>
                    </div>
                    <div className="flex items-center gap-2 bg-white/15 backdrop-blur-sm rounded-xl px-4 py-2.5 border border-white/10">
                        <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center">
                            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                        </div>
                        <div>
                            <p className="text-[10px] text-emerald-200 font-medium uppercase tracking-wider">Interviews</p>
                            <p className="text-lg font-bold leading-tight">3</p>
                        </div>
                    </div>
                    <div className="flex items-center gap-2 bg-white/15 backdrop-blur-sm rounded-xl px-4 py-2.5 border border-white/10">
                        <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center">
                            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                            </svg>
                        </div>
                        <div>
                            <p className="text-[10px] text-emerald-200 font-medium uppercase tracking-wider">Profile Views</p>
                            <p className="text-lg font-bold leading-tight">156</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
