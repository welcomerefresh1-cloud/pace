export default function StatCard({
    title,
    value,
    change,
    changeType,
    icon,
    gradient,
}: {
    title: string;
    value: string;
    change: string;
    changeType: "positive" | "negative" | "neutral";
    icon: React.ReactNode;
    gradient: string;
}) {
    return (
        <div className="group relative overflow-hidden rounded-2xl bg-white/80 backdrop-blur-sm border border-slate-200/60 p-6 transition-all duration-500 hover:shadow-xl hover:shadow-slate-200/50 hover:-translate-y-1 hover:border-slate-300/80 hover:bg-white">
            {/* Outer glow effect on hover */}
            <div className={`absolute -inset-1 ${gradient} opacity-0 blur-xl transition-all duration-500 group-hover:opacity-10 rounded-3xl`} />

            {/* Decorative background gradient */}
            <div className={`absolute -right-6 -top-6 h-32 w-32 rounded-full ${gradient} opacity-10 blur-2xl transition-all duration-500 group-hover:opacity-25 group-hover:scale-150`} />

            {/* Secondary decorative orb */}
            <div className={`absolute -left-10 bottom-0 h-20 w-20 rounded-full ${gradient} opacity-5 blur-xl transition-all duration-500 group-hover:opacity-10`} />

            {/* Subtle diagonal lines pattern */}
            <div className="absolute inset-0 opacity-[0.015] pointer-events-none"
                style={{
                    backgroundImage: `repeating-linear-gradient(
                        -45deg,
                        transparent,
                        transparent 8px,
                        rgba(0,0,0,0.1) 8px,
                        rgba(0,0,0,0.1) 9px
                    )`
                }}
            />

            {/* Subtle grid pattern */}
            <div className="absolute inset-0 opacity-[0.02] pointer-events-none"
                style={{
                    backgroundImage: 'radial-gradient(circle at 1px 1px, rgb(0,0,0) 1px, transparent 0)',
                    backgroundSize: '16px 16px'
                }}
            />

            {/* Top shine effect */}
            <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white to-transparent opacity-80" />

            <div className="relative flex items-start justify-between">
                <div className="flex-1">
                    <p className="text-sm font-medium text-slate-500 tracking-wide">{title}</p>
                    <p className="mt-3 text-4xl font-bold bg-gradient-to-br from-slate-900 via-slate-800 to-slate-700 bg-clip-text text-transparent">
                        {value}
                    </p>
                    <div className="mt-3 flex items-center gap-2">
                        <span
                            className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-semibold ${changeType === "positive"
                                ? "bg-emerald-50 text-emerald-600"
                                : changeType === "negative"
                                    ? "bg-red-50 text-red-500"
                                    : "bg-slate-100 text-slate-500"
                                }`}
                        >
                            {changeType === "positive" && (
                                <svg className="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
                                </svg>
                            )}
                            {changeType === "negative" && (
                                <svg className="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                </svg>
                            )}
                            {change}
                        </span>
                        <span className="text-xs text-slate-400">vs last month</span>
                    </div>
                </div>

                {/* Enhanced icon container with glass effect */}
                <div className="relative">
                    <div className={`absolute inset-0 ${gradient} rounded-2xl blur-lg opacity-40 group-hover:opacity-60 transition-opacity duration-500`} />
                    <div className={`relative flex h-14 w-14 items-center justify-center rounded-2xl ${gradient} text-white shadow-lg ring-4 ring-white/50`}>
                        {icon}
                    </div>
                </div>
            </div>

            {/* Animated bottom border */}
            <div className="absolute bottom-0 left-0 h-1 w-0 rounded-br-2xl rounded-bl-2xl bg-gradient-to-r from-emerald-400 via-emerald-500 to-emerald-600 transition-all duration-500 group-hover:w-full" />
        </div>
    );
}
