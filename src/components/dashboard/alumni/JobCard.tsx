export default function JobCard({
    title,
    company,
    location,
    salary,
    type,
    logo,
    description,
    className,
}: {
    title: string;
    company: string;
    location: string;
    salary: string;
    type: string;
    logo: string;
    description?: string;
    className?: string;
}) {
    // Determine badge color based on type
    const getBadgeStyle = () => {
        switch (type.toLowerCase()) {
            case 'full-time':
                return 'bg-emerald-50 text-emerald-700 ring-emerald-600/20';
            case 'internship':
                return 'bg-blue-50 text-blue-700 ring-blue-600/20';
            case 'part-time':
                return 'bg-amber-50 text-amber-700 ring-amber-600/20';
            default:
                return 'bg-slate-50 text-slate-700 ring-slate-600/20';
        }
    };

    return (
        <div className={`group relative flex items-start gap-4 rounded-xl border border-slate-400/50 bg-white shadow-lg shadow-slate-300/50 p-5 transition-all duration-300 hover:border-emerald-400 hover:shadow-xl hover:shadow-emerald-200/50 overflow-hidden ${className}`}>
            {/* Subtle diagonal texture */}
            <div
                className="absolute inset-0 opacity-[0.012] pointer-events-none"
                style={{
                    backgroundImage: `repeating-linear-gradient(
                        45deg,
                        transparent,
                        transparent 4px,
                        rgba(0,0,0,0.1) 4px,
                        rgba(0,0,0,0.1) 5px
                    )`
                }}
            />

            {/* Hover accent border */}
            <div className="absolute left-0 top-0 h-full w-1 bg-gradient-to-b from-emerald-400 to-emerald-600 opacity-0 transition-all duration-300 group-hover:opacity-100" />

            {/* Top shine line */}
            <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-slate-200/50 to-transparent" />

            {/* Logo with gradient ring */}
            <div className="relative flex-shrink-0">
                <div className="absolute inset-0 bg-gradient-to-br from-emerald-400 to-emerald-600 rounded-xl blur opacity-0 group-hover:opacity-30 transition-opacity duration-300" />
                <div className="relative flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-slate-50 to-slate-100 text-lg font-bold text-slate-600 ring-2 ring-slate-100 group-hover:ring-emerald-200 transition-all duration-300">
                    {logo}
                </div>
            </div>

            <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-3 mb-2">
                    <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-slate-900 group-hover:text-emerald-700 transition-colors duration-300 truncate">
                            {title}
                        </h3>
                        <p className="text-sm text-slate-500 truncate">{company}</p>
                    </div>
                    <div className="flex items-center gap-2 flex-shrink-0">
                        <span className={`rounded-full px-3 py-1 text-xs font-semibold ring-1 ring-inset ${getBadgeStyle()}`}>
                            {type}
                        </span>
                        {/* Bookmark button */}
                        <button className="p-1.5 rounded-lg text-slate-300 hover:text-emerald-500 hover:bg-emerald-50 transition-all duration-200 opacity-0 group-hover:opacity-100">
                            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                            </svg>
                        </button>
                    </div>
                </div>

                {description && (
                    <div
                        className="text-sm text-slate-600 mb-3 line-clamp-2"
                        dangerouslySetInnerHTML={{ __html: description }}
                    />
                )}

                <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-sm">
                    <span className="flex items-center gap-1.5 text-slate-500">
                        <svg className="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        {location}
                    </span>
                    <span className="flex items-center gap-1.5 text-slate-500">
                        <svg className="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {salary}
                    </span>

                </div>
            </div>
        </div>
    );
}
