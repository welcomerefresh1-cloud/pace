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
        <div className="group relative rounded-2xl bg-white border border-gray-200/80 p-5 transition-all duration-200 hover:shadow-md hover:border-gray-300/80">
            <div className="flex items-start justify-between">
                <div className="flex-1">
                    <p className="text-sm font-medium text-gray-500">{title}</p>
                    <p className="mt-2 text-3xl font-bold text-gray-900">
                        {value}
                    </p>
                    <div className="mt-2 flex items-center gap-1.5">
                        <span
                            className={`inline-flex items-center gap-0.5 text-xs font-semibold ${changeType === "positive"
                                ? "text-emerald-600"
                                : changeType === "negative"
                                    ? "text-red-500"
                                    : "text-gray-400"
                                }`}
                        >
                            {changeType === "positive" && (
                                <svg className="h-3.5 w-3.5" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
                                </svg>
                            )}
                            {changeType === "negative" && (
                                <svg className="h-3.5 w-3.5" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                </svg>
                            )}
                            {change}
                        </span>
                        <span className="text-xs text-gray-400">vs last month</span>
                    </div>
                </div>

                <div className={`flex h-11 w-11 items-center justify-center rounded-xl ${gradient} text-white`}>
                    {icon}
                </div>
            </div>
        </div>
    );
}
