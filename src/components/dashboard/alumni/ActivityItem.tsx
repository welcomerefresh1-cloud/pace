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
        <div className="group relative flex gap-3 py-2.5 -mx-1 px-1 rounded-lg hover:bg-gray-50/80 transition-colors duration-150">
            {/* Timeline connector */}
            <div className="relative flex-shrink-0">
                {!isLast && (
                    <div className="absolute left-1/2 top-10 -translate-x-1/2 w-px h-[calc(100%+2px)] bg-gray-200" />
                )}
                <div className={`relative flex h-8 w-8 items-center justify-center rounded-full ${iconBg} ring-2 ring-white`}>
                    <div className="h-4 w-4">{icon}</div>
                </div>
            </div>

            <div className="flex-1 min-w-0 pt-0.5">
                <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900">
                            {title}
                        </p>
                        <p className="mt-0.5 text-xs text-gray-500 line-clamp-1">{description}</p>
                    </div>
                    <span className="flex-shrink-0 text-[10px] text-gray-400 mt-0.5">
                        {time}
                    </span>
                </div>
            </div>
        </div>
    );
}
