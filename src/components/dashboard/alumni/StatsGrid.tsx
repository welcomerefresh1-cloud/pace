import StatCard from "./StatCard";

export default function StatsGrid() {
    return (
        <div className="relative grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            <StatCard
                title="Total Applications"
                value="12"
                change="+3"
                changeType="positive"
                gradient="bg-gradient-to-br from-blue-500 to-blue-600"
                icon={
                    <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                }
            />
            <StatCard
                title="Interviews Scheduled"
                value="3"
                change="+2"
                changeType="positive"
                gradient="bg-gradient-to-br from-emerald-500 to-emerald-600"
                icon={
                    <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                }
            />
            <StatCard
                title="Profile Views"
                value="156"
                change="+23%"
                changeType="positive"
                gradient="bg-gradient-to-br from-violet-500 to-violet-600"
                icon={
                    <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                }
            />
            <StatCard
                title="Saved Jobs"
                value="24"
                change="0"
                changeType="neutral"
                gradient="bg-gradient-to-br from-amber-500 to-amber-600"
                icon={
                    <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                    </svg>
                }
            />
        </div>
    );
}
