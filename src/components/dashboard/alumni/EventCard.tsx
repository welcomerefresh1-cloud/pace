export default function EventCard({
    title,
    date,
    time,
    location,
    attendees,
    type,
}: {
    title: string;
    date: string;
    time: string;
    location: string;
    attendees: number;
    type: string;
}) {
    // Get type styling
    const getTypeStyle = () => {
        switch (type.toLowerCase()) {
            case 'career fair':
                return 'bg-emerald-50 text-emerald-700';
            case 'workshop':
                return 'bg-violet-50 text-violet-700';
            case 'seminar':
                return 'bg-blue-50 text-blue-700';
            default:
                return 'bg-amber-50 text-amber-700';
        }
    };

    return (
        <div className="group relative overflow-hidden rounded-xl border border-slate-400/50 bg-white shadow-lg shadow-slate-300/50 transition-all duration-300 hover:border-emerald-500 hover:shadow-xl hover:shadow-emerald-200/50 hover:scale-[1.01]">
            <div className="flex">
                {/* Date section with enhanced gradient */}
                <div className="relative flex w-20 flex-col items-center justify-center overflow-hidden bg-gradient-to-br from-emerald-500 via-emerald-600 to-emerald-700 px-4 py-4 text-white">
                    {/* Decorative elements */}
                    <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(255,255,255,0.15),transparent_50%)]" />
                    <div className="absolute -bottom-4 -left-4 h-12 w-12 rounded-full bg-white/10 blur-md" />

                    <span className="relative text-2xl font-bold tracking-tight">{date.split(" ")[0]}</span>
                    <span className="relative text-xs font-semibold uppercase tracking-wider opacity-90">{date.split(" ")[1]}</span>

                    {/* Animated shine effect on hover */}
                    <div className="absolute inset-0 -translate-x-full bg-gradient-to-r from-transparent via-white/20 to-transparent group-hover:translate-x-full transition-transform duration-700 ease-out" />
                </div>

                <div className="flex-1 p-4">
                    <div className="flex items-start justify-between gap-2">
                        <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ${getTypeStyle()}`}>
                            {type}
                        </span>
                        {/* Add to calendar hint on hover */}
                        <button className="p-1.5 rounded-lg text-slate-300 hover:text-emerald-500 hover:bg-emerald-50 transition-all duration-200 opacity-0 group-hover:opacity-100">
                            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                        </button>
                    </div>

                    <h3 className="mt-2 font-semibold text-slate-900 group-hover:text-emerald-700 transition-colors duration-300 line-clamp-1">
                        {title}
                    </h3>

                    <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-1.5 text-xs text-slate-500">
                        <span className="flex items-center gap-1.5">
                            <svg className="h-3.5 w-3.5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            {time}
                        </span>
                        <span className="flex items-center gap-1.5">
                            <svg className="h-3.5 w-3.5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                            </svg>
                            {location}
                        </span>
                        <span className="flex items-center gap-1.5">
                            <svg className="h-3.5 w-3.5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                            </svg>
                            <span className="text-emerald-600 font-medium">{attendees}</span> attending
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
}
