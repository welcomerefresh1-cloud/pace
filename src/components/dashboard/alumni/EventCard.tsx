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
        <div className="group flex items-stretch rounded-xl border border-gray-100 bg-white transition-all duration-200 hover:border-gray-200 hover:shadow-sm overflow-hidden">
            {/* Date section */}
            <div className="flex w-16 flex-col items-center justify-center bg-emerald-500 px-3 py-3 text-white">
                <span className="text-xl font-bold">{date.split(" ")[0]}</span>
                <span className="text-[10px] font-semibold uppercase tracking-wider opacity-90">{date.split(" ")[1]}</span>
            </div>

            <div className="flex-1 p-3.5">
                <div className="flex items-start justify-between gap-2">
                    <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-[10px] font-semibold ${getTypeStyle()}`}>
                        {type}
                    </span>
                </div>

                <h3 className="mt-1.5 text-sm font-semibold text-gray-900 group-hover:text-emerald-700 transition-colors duration-200 line-clamp-1">
                    {title}
                </h3>

                <div className="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-[11px] text-gray-500">
                    <span className="flex items-center gap-1">
                        <svg className="h-3 w-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {time}
                    </span>
                    <span className="flex items-center gap-1">
                        <svg className="h-3 w-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        </svg>
                        {location}
                    </span>
                    <span className="flex items-center gap-1">
                        <svg className="h-3 w-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                        <span className="text-emerald-600 font-medium">{attendees}</span> attending
                    </span>
                </div>
            </div>
        </div>
    );
}
