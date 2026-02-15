const activities = [
    {
        action: "New employer registered",
        detail: "Tech Solutions Inc.",
        time: "15m",
        color: "#10b981",
        bgClass: "bg-emerald-50",
        icon: (
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008z" />
            </svg>
        ),
    },
    {
        action: "Job posting approved",
        detail: "UI/UX Designer at Accenture",
        time: "1h",
        color: "#3b82f6",
        bgClass: "bg-blue-50",
        icon: (
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 14.15v4.25c0 1.094-.787 2.036-1.872 2.18-2.087.277-4.216.42-6.378.42s-4.291-.143-6.378-.42c-1.085-.144-1.872-1.086-1.872-2.18v-4.25m16.5 0a2.18 2.18 0 00.75-1.661V8.706c0-1.081-.768-2.015-1.837-2.175a48.114 48.114 0 00-3.413-.387m4.5 8.006c-.194.165-.42.295-.673.38A23.978 23.978 0 0112 15.75c-2.648 0-5.195-.429-7.577-1.22a2.016 2.016 0 01-.673-.38m0 0A2.18 2.18 0 013 12.489V8.706c0-1.081.768-2.015 1.837-2.175a48.111 48.111 0 013.413-.387m7.5 0V5.25A2.25 2.25 0 0013.5 3h-3a2.25 2.25 0 00-2.25 2.25v.894m7.5 0a48.667 48.667 0 00-7.5 0M12 12.75h.008v.008H12v-.008z" />
            </svg>
        ),
    },
    {
        action: "Event created",
        detail: "Career Fair 2026 — March 20",
        time: "3h",
        color: "#8b5cf6",
        bgClass: "bg-violet-50",
        icon: (
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
            </svg>
        ),
    },
    {
        action: "Alumni verified",
        detail: "Maria Santos — BSIT 2024",
        time: "5h",
        color: "#10b981",
        bgClass: "bg-emerald-50",
        icon: (
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z" />
            </svg>
        ),
    },
    {
        action: "Report generated",
        detail: "Monthly analytics — Jan 2026",
        time: "1d",
        color: "#f59e0b",
        bgClass: "bg-amber-50",
        icon: (
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
            </svg>
        ),
    },
];

export default function PlatformActivity() {
    return (
        <div className="group relative rounded-2xl bg-white border border-gray-100/80 shadow-sm transition-all duration-500 hover:shadow-xl hover:shadow-gray-200/20 hover:border-gray-200/80 overflow-hidden flex flex-col">


            {/* Header */}
            <div className="px-6 pt-5 pb-4 flex items-start justify-between">
                <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-slate-500 to-slate-600 text-white shadow-lg shadow-slate-500/25">
                        <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                    <div>
                        <h3 className="text-[13px] font-semibold text-gray-900 tracking-tight">Activity Log</h3>
                        <p className="text-[11px] text-gray-400 mt-0.5">Platform-wide actions</p>
                    </div>
                </div>
                <button className="text-[11px] font-semibold text-gray-500 hover:text-gray-900 transition-all duration-200 px-3 py-1.5 rounded-lg hover:bg-gray-50 ring-1 ring-gray-100/60 hover:ring-gray-200">
                    View All
                </button>
            </div>

            {/* Timeline */}
            <div className="px-6 pb-2 flex-1">
                <div className="relative">
                    {/* Vertical timeline line */}
                    <div
                        className="absolute left-[15px] top-[20px] bottom-[20px] w-px"
                        style={{
                            background: "linear-gradient(to bottom, #e2e8f0, #e2e8f0 60%, transparent)",
                        }}
                    />

                    <div className="space-y-0.5">
                        {activities.slice(0, 4).map((item, idx) => (
                            <div
                                key={idx}
                                className="group/item relative flex items-start gap-4 py-3 px-2 -mx-2 rounded-xl hover:bg-gray-50/60 transition-all duration-200 cursor-pointer"
                            >
                                {/* Icon node */}
                                <div className="relative z-10 flex-shrink-0 mt-0.5">
                                    <div
                                        className={`w-[30px] h-[30px] rounded-lg ${item.bgClass} flex items-center justify-center ring-[3px] ring-white transition-all duration-300 group-hover/item:scale-110 group-hover/item:shadow-md`}
                                        style={{ color: item.color }}
                                    >
                                        {item.icon}
                                    </div>
                                </div>

                                {/* Content */}
                                <div className="flex-1 min-w-0 pt-0.5">
                                    <p className="text-[13px] font-medium text-gray-800 leading-tight group-hover/item:text-gray-900 transition-colors">
                                        {item.action}
                                    </p>
                                    <p className="text-[11px] text-gray-400 mt-0.5 truncate">{item.detail}</p>
                                </div>

                                {/* Time badge */}
                                <div className="flex-shrink-0 mt-1">
                                    <span className="text-[10px] font-medium text-gray-400 bg-gray-50 px-2 py-1 rounded-md ring-1 ring-gray-100/60 group-hover/item:bg-white group-hover/item:ring-gray-200/80 transition-all">
                                        {item.time} ago
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>


        </div>
    );
}
