export default function ActivityItem({
    icon,
    title,
    description,
    time,
    iconBg,
    isLast = false,
}: {
    icon: React.ReactNode;
    title: string;
    description: string;
    time: string;
    iconBg: string;
    isLast?: boolean;
}) {
    return (
        <div className="group relative flex gap-4 hover:bg-slate-50/50 -mx-2 px-2 py-2 rounded-lg transition-colors duration-200">
            {/* Timeline connector */}
            <div className="relative flex-shrink-0">
                {/* Vertical line */}
                {!isLast && (
                    <div className="absolute left-1/2 top-12 -translate-x-1/2 w-0.5 h-[calc(100%-0.5rem)] bg-gradient-to-b from-slate-200 to-transparent" />
                )}

                {/* Icon container with enhanced styling */}
                <div className="relative">
                    <div className={`absolute inset-0 rounded-full ${iconBg.replace('text-', 'bg-').replace('-600', '-400')} opacity-0 blur-md group-hover:opacity-40 transition-opacity duration-300`} />
                    <div className={`relative flex h-10 w-10 items-center justify-center rounded-full ${iconBg} ring-4 ring-white shadow-sm transition-transform duration-200 group-hover:scale-110`}>
                        {icon}
                    </div>
                </div>
            </div>

            <div className="flex-1 pt-1">
                <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                        <p className="font-medium text-slate-900 group-hover:text-emerald-700 transition-colors duration-200">
                            {title}
                        </p>
                        <p className="mt-0.5 text-sm text-slate-500 line-clamp-1">{description}</p>
                    </div>
                    <span className="flex-shrink-0 text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded-full">
                        {time}
                    </span>
                </div>
            </div>
        </div>
    );
}
