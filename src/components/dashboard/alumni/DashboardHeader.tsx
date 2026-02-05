
export default function DashboardHeader() {
    return (
        <div className="relative flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-900 via-slate-800 to-slate-700 bg-clip-text text-transparent">
                    Dashboard Overview
                </h1>
                <p className="mt-1.5 text-slate-500">
                    Track your applications, discover opportunities, and stay updated.
                </p>
            </div>
            <div className="flex gap-3">

            </div>
        </div>
    );
}
