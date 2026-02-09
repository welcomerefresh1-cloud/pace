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
    const getBadgeStyle = () => {
        switch (type.toLowerCase()) {
            case 'full-time':
                return 'bg-emerald-50 text-emerald-700 ring-emerald-200';
            case 'internship':
                return 'bg-blue-50 text-blue-700 ring-blue-200';
            case 'part-time':
                return 'bg-amber-50 text-amber-700 ring-amber-200';
            default:
                return 'bg-gray-50 text-gray-700 ring-gray-200';
        }
    };

    return (
        <div className={`group flex items-start gap-4 rounded-xl border border-gray-100 bg-white p-4 transition-all duration-200 hover:border-gray-200 hover:shadow-sm ${className}`}>
            {/* Logo */}
            <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg bg-gray-100 text-sm font-bold text-gray-600 group-hover:bg-emerald-50 group-hover:text-emerald-600 transition-colors duration-200">
                {logo}
            </div>

            <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-3 mb-1.5">
                    <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-gray-900 group-hover:text-emerald-700 transition-colors duration-200 truncate text-sm">
                            {title}
                        </h3>
                        <p className="text-sm text-gray-500 truncate">{company}</p>
                    </div>
                    <span className={`flex-shrink-0 rounded-full px-2.5 py-0.5 text-[11px] font-semibold ring-1 ring-inset ${getBadgeStyle()}`}>
                        {type}
                    </span>
                </div>

                {description && (
                    <div
                        className="text-sm text-gray-500 mb-2.5 line-clamp-2 leading-relaxed"
                        dangerouslySetInnerHTML={{ __html: description }}
                    />
                )}

                <div className="flex flex-wrap items-center gap-x-3 gap-y-1.5 text-xs text-gray-500">
                    <span className="flex items-center gap-1">
                        <svg className="h-3.5 w-3.5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        {location}
                    </span>
                    <span className="flex items-center gap-1">
                        <svg className="h-3.5 w-3.5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {salary}
                    </span>
                </div>
            </div>
        </div>
    );
}
